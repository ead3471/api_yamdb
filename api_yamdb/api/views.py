from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import default_token_generator
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import get_object_or_404
from django.db.models import Avg
from rest_framework import status
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.filters import SearchFilter
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from rest_framework.viewsets import (
    GenericViewSet,
    ModelViewSet
)
from rest_framework_simplejwt.tokens import RefreshToken

from api.permissions import IsAdmin, IsAuthorModerAdmin

from api.serializers import (
    AuthSignupSerializer, AuthTokenSerializer,
    UserSerializer, UserRoleReadOnlySerializer,
    TitleSerializer, ReviewSerializer, CommentSerializer
)

from artworks.models import Title, Review, Comment

REGISTRATION_EMAIL_SUBJECT = 'YAMDB registration.'
REGISTRATION_EMAIL_FROM = 'team15@yamdb.fake'


User = get_user_model()


class UserViewSet(ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    lookup_field = 'username'
    http_method_names = ['get', 'post', 'patch', 'delete']
    filter_backends = (SearchFilter,)
    search_fields = ('username',)
    permission_classes = [IsAdmin | IsAdminUser]

    @action(
        ["get", "patch"],
        detail=False,
        permission_classes=[IsAuthenticated],
        serializer_class=UserRoleReadOnlySerializer
    )
    def me(self, request):
        self.kwargs['username'] = request.user
        if request.method == "GET":
            return self.retrieve(request)
        elif request.method == "PATCH":
            return self.partial_update(request)


class AuthViewSet(GenericViewSet):

    queryset = User.objects.all()
    serializer_class = AuthSignupSerializer

    @action(["post"], detail=False)
    def signup(self, request):
        try:
            user = User.objects.get(username=request.data.get('username'))
        except ObjectDoesNotExist:
            serializer = AuthSignupSerializer(data=request.data)
        else:
            serializer = AuthSignupSerializer(user, data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            confirmation_code = default_token_generator.make_token(user)
            email_text = (
                f'To confirm user {user} registration '
                f'please use {confirmation_code} code.'
            )
            user.email_user(
                REGISTRATION_EMAIL_SUBJECT,
                email_text,
                REGISTRATION_EMAIL_FROM,
                fail_silently=False,
            )
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(["post"], detail=False)
    def token(self, request):
        serializer = AuthTokenSerializer(data=request.data)
        if serializer.is_valid():
            user = get_object_or_404(User, username=serializer.validated_data.get('username'))
            tokens = RefreshToken.for_user(user)
            return Response(
                data={'token': str(tokens.access_token)},
                status=status.HTTP_200_OK
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class TitleViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.all().annotate(rating=Avg('reviews__score'))
    serializer_class = TitleSerializer

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class ReviewViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewSerializer
    permission_classes = (IsAuthorModerAdmin,)

    def get_queryset(self):
        title_id = self.kwargs.get('title_id')
        return Review.objects.filter(title_id=title_id)

    def perform_create(self, serializer):
        title_id = self.kwargs.get('title_id')
        serializer.save(author=self.request.user, title_id=title_id)


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = (IsAuthorModerAdmin,)

    def get_queryset(self):
        review_id = self.kwargs.get('review_id')
        return Comment.objects.filter(review_id=review_id)

    def perform_create(self, serializer):
        review_id = self.kwargs.get('review_id')
        serializer.save(author=self.request.user, review_id=review_id)
