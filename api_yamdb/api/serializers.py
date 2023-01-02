from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import default_token_generator
from rest_framework import serializers
from rest_framework.exceptions import ValidationError


User = get_user_model()


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('username', 'email', 'first_name',
                  'last_name', 'bio', 'role')

    def validate_username(self, value):
        if value.lower() == 'me':
            raise ValidationError(
                f'Username \'me\' is reserved, please chose another one'
            )
        return value


class UserRoleReadOnlySerializer(UserSerializer):

    class Meta:
        model = User
        fields = ('username', 'email', 'first_name',
                  'last_name', 'bio', 'role')
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
                'Such user is already registered with different email')
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
