from rest_framework.exceptions import ValidationError
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth import get_user_model
from rest_framework import serializers
from django.shortcuts import get_object_or_404

from reviews.models import Title, Review, Comment, Genre, Category

User = get_user_model()


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = ('name', 'slug')


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('name', 'slug')


class TitleGetSerializer(serializers.ModelSerializer):
    rating = serializers.IntegerField(read_only='True', required=False)
    genre = GenreSerializer(many=True)
    category = CategorySerializer()

    class Meta:
        model = Title
        fields = ('__all__')


class TitleModifySerializer(serializers.ModelSerializer):
    genre = serializers.SlugRelatedField(
        many=True, queryset=Genre.objects.all(), slug_field='slug')
    category = serializers.SlugRelatedField(
        slug_field='slug', queryset=Category.objects.all())

    class Meta:
        model = Title
        fields = ('__all__')


class ReviewSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        read_only=True, slug_field='username'
    )

    def validate(self, attrs):
        title = get_object_or_404(
            Title, id=self.context['view'].kwargs.get('title_id'))
        author = self.context['request'].user
        if self.context['request'].method == 'POST':
            if Review.objects.filter(
                    title_id=title, author_id=author).exists():
                raise serializers.ValidationError(
                    'You have already left a review for this title!')
        return attrs

    class Meta:
        model = Review
        fields = ('id', 'text', 'author', 'score', 'pub_date')


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        read_only=True,
        slug_field='username'
    )

    class Meta:
        model = Comment
        fields = ('id', 'text', 'author', 'pub_date')

    def validate(self, attrs):
        get_object_or_404(
            Title, id=self.context['view'].kwargs.get('title_id'))
        get_object_or_404(
            Review, id=self.context['view'].kwargs.get('review_id'))
        return attrs


class UserSerializer(serializers.ModelSerializer):
    """ Serializer to process other users profile management API requests.
    """
    class Meta:
        model = User
        fields = (
            'username',
            'email',
            'first_name',
            'last_name',
            'bio',
            'role'
        )

    def validate_username(self, value):
        if value.lower() == 'me':
            raise ValidationError(
                'Username \'me\' is reserved, please choose another one'
            )
        return value


class UserRoleReadOnlySerializer(UserSerializer):
    """ Serializer to process own user profile management API requests.
    Role field change is restricted.
    """
    class Meta:
        model = User
        fields = (
            'username',
            'email',
            'first_name',
            'last_name',
            'bio',
            'role'
        )
        read_only_fields = ['role']


class AuthSignupSerializer(UserSerializer):

    class Meta:
        model = User
        fields = ('username', 'email')

    def validate(self, attrs):
        if User.objects.filter(
            username=attrs.get('username')
        ).exclude(
            email=attrs.get('email')
        ).exists():
            raise ValidationError(
                'Such user is already registered with different email'
            )
        return super().validate(attrs)


class AuthTokenSerializer(serializers.Serializer):

    username = serializers.RegexField(r'^[\w.@+-]+$', max_length=150)
    confirmation_code = serializers.CharField(max_length=40)

    def validate(self, attrs):
        token = attrs.get('confirmation_code')
        user = get_object_or_404(User, username=attrs.get('username'))
        if not default_token_generator.check_token(user, token):
            raise ValidationError('Invalid token')
        return super().validate(attrs)
