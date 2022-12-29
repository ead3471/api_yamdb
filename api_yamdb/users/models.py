from django.contrib.auth.models import AbstractUser
from django.db import models


USER_ROLES = (
    ('user', 'user'),
    ('moderator', 'moderator'),
    ('admin', 'admin')
)
DEFAULT_USER_ROLE = 'user'

class User(AbstractUser):
    email = models.EmailField(
        'email address',
        unique=True,
        blank=False
    )
    bio = models.TextField(
        'Biography',
        blank=True
    )
    role = models.CharField(
        'Role',
        max_length=20,
        default=DEFAULT_USER_ROLE,
        choices=USER_ROLES,
    )