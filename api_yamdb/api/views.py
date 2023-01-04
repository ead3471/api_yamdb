from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import default_token_generator
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.filters import SearchFilter
from rest_framework.permissions import IsAuthenticated, IsAdminUser, AllowAny
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.permissions import IsAuthenticated, IsAdminUser, AllowAny
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.response import Response
from django.db.models import Avg
import django_filters
from django_filters import rest_framework as filters
from rest_framework.viewsets import (
    GenericViewSet,
    ModelViewSet
)
from rest_framework.mixins import (ListModelMixin,
                                   CreateModelMixin,
                                   DestroyModelMixin)
from rest_framework.mixins import (ListModelMixin,
                                   CreateModelMixin,
                                   DestroyModelMixin)
from rest_framework_simplejwt.tokens import RefreshToken
from reviews.models import Title, Review, Comment, Genre, Category
from api.permissions import IsAdmin, IsModerator, IsAuthor, ReadOnly
from reviews.models import Title, Review, Comment, Genre, Category
from api.permissions import IsAdmin, IsModerator, IsAuthor, ReadOnly
from api.serializers import (
    AuthSignupSerializer, AuthTokenSerializer,
    UserSerializer, UserRoleReadOnlySerializer,
    TitleGetSerializer, TitleModifySerializer,
    GenreSerializer, CategorySerializer,
    ReviewSerializer,
    CommentSerializer
    UserSerializer, UserRoleReadOnlySerializer,
    TitleGetSerializer, TitleModifySerializer,
    GenreSerializer, CategorySerializer,
    ReviewSerializer,
    CommentSerializer
)

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
        """ Function to process API requests with users/me/ URI.
        """
        self.kwargs['username'] = request.user
        if request.method == "GET":
            return self.retrieve(request)
        elif request.method == "PATCH":
            return self.partial_update(request)


class AuthViewSet(GenericViewSet):
    queryset = User.objects.all()
    serializer_class = AuthSignupSerializer
    permission_classes = [AllowAny]

    @action(["post"], detail=False)
    def signup(self, request):
        """ Function to process API requests with auth/signup/ URI.
        """
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
        """Function to process API requests with auth/token/
        """
        serializer = AuthTokenSerializer(data=request.data)
        if serializer.is_valid():
            user = get_object_or_404(
                User, username=serializer.validated_data.get('username'))
            tokens = RefreshToken.for_user(user)
            return Response(
                data={'token': str(tokens.access_token)},
                status=status.HTTP_200_OK
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class TitleFilter(django_filters.FilterSet):
    category = filters.CharFilter(
        field_name='category__slug', lookup_expr='exact')
    genre = filters.CharFilter(field_name='genre__slug', lookup_expr='exact')

    class Meta():
        model = Title
        fields = ['name', 'year']


class TitleViewSet(ModelViewSet):
    queryset = (
        Title.objects.all().
        annotate(rating=Avg('reviews__score')).
        order_by('id')
    )
    permission_classes = [ReadOnly | IsAdmin | IsAdminUser]

    filter_backends = (DjangoFilterBackend,)
    filterset_class = TitleFilter

    action_serializers = {
        'list': TitleGetSerializer,
        'retrieve': TitleGetSerializer,
        'create': TitleModifySerializer,
        'update': TitleModifySerializer,
        'partial_update': TitleModifySerializer,
        'destroy': TitleModifySerializer
    }

    def get_serializer_class(self):
        return self.action_serializers.get(self.action)
    def get_serializer_class(self):
        return self.action_serializers.get(self.action)


class GenreViewSet(GenericViewSet,
                   ListModelMixin,
                   CreateModelMixin,
                   DestroyModelMixin):
    serializer_class = GenreSerializer
    permission_classes = [ReadOnly | IsAdmin | IsAdminUser]
    filter_backends = (SearchFilter,)
    search_fields = ('name',)
    lookup_field = 'slug'
    queryset = Genre.objects.all()

class GenreViewSet(GenericViewSet,
                   ListModelMixin,
                   CreateModelMixin,
                   DestroyModelMixin):
    serializer_class = GenreSerializer
    permission_classes = [ReadOnly | IsAdmin | IsAdminUser]
    filter_backends = (SearchFilter,)
    search_fields = ('name',)
    lookup_field = 'slug'
    queryset = Genre.objects.all()


class CategoryViewSet(GenericViewSet,
                      ListModelMixin,
                      CreateModelMixin,
                      DestroyModelMixin):
    serializer_class = CategorySerializer
    permission_classes = [ReadOnly | IsAdmin | IsAdminUser]
    filter_backends = (SearchFilter,)
    search_fields = ('name',)
    lookup_field = 'slug'
    queryset = Category.objects.all()
class CategoryViewSet(GenericViewSet,
                      ListModelMixin,
                      CreateModelMixin,
                      DestroyModelMixin):
    serializer_class = CategorySerializer
    permission_classes = [ReadOnly | IsAdmin | IsAdminUser]
    filter_backends = (SearchFilter,)
    search_fields = ('name',)
    lookup_field = 'slug'
    queryset = Category.objects.all()


class ReviewViewSet(ModelViewSet):
class ReviewViewSet(ModelViewSet):
    serializer_class = ReviewSerializer
    permission_classes = [IsAuthor | IsModerator | IsAdmin | ReadOnly]

    def get_queryset(self):
        title_id = self.kwargs.get('title_id')
        return Review.objects.filter(title_id=title_id).order_by('pub_date')

    def perform_create(self, serializer):
        title_id = self.kwargs.get('title_id')
        serializer.save(author=self.request.user, title_id=title_id)
        serializer.save(author=self.request.user)


class CommentViewSet(ModelViewSet):
class CommentViewSet(ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = [IsAuthor | IsModerator | IsAdmin | ReadOnly]

    def get_queryset(self):
        review_id = self.kwargs.get('review_id')
        return Comment.objects.filter(review_id=review_id).order_by('pub_date')

    def perform_create(self, serializer):
        review_id = self.kwargs.get('review_id')
        serializer.save(author=self.request.user, review_id=review_id)
