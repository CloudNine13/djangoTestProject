import uuid

from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin

from streaming.managers import CustomUserManager


class Video(models.Model):
    objects: models.Manager()
    ID = models.CharField(primary_key=True, max_length=50)
    FileName = models.CharField(max_length=50)
    FileSize = models.CharField(max_length=50)
    FileUrl = models.CharField(max_length=50)

    class Meta:
        db_table = "videos"


class ServiceUser(AbstractBaseUser, PermissionsMixin):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )
    email = models.EmailField(verbose_name="email", max_length=60, unique=True)
    username = models.CharField(verbose_name='username', max_length=30, unique=True)
    password = models.CharField(verbose_name='password', max_length=120)
    created_at = models.DateTimeField(verbose_name='created at', auto_now_add=True)
    last_login = models.DateTimeField(verbose_name='last login', auto_now=True)
    is_admin = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    subscription = models.CharField(
        _('subscription'),
        max_length=1,
        choices=[
            ('S', 'Subscribed'), ('N', 'Unsubscribed')
        ],
        default='N'
    )

    stripeCustomerId = models.CharField(_('stripe user id'), max_length=255)
    stripeSubscriptionId = models.CharField(_('stripe subscription id'), max_length=255)

    objects = CustomUserManager()

    EMAIL_FIELD = 'email'
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email',]

    class Meta:
        db_table = "users"
        verbose_name = _('user')
        verbose_name_plural = _('users')

    def __str__(self):
        """stirng representation"""
        return self.username
