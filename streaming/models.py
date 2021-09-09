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
    email = models.EmailField(_('email'))
    name = models.CharField(_('name'), max_length=50, blank=False, unique=True)
    subscription = models.CharField(
        _('subscription'),
        max_length=1,
        choices=[
            ('S', 'Subscribed'), ('N', 'Unsubscribed')
        ]
    )

    is_superuser = models.BooleanField(_('is_superuser'), default=False)
    is_active = models.BooleanField(_('is_active'), default=True)
    is_staff = models.BooleanField(default=False)
    stripeCustomerId = models.CharField(_('stripe user id'), max_length=255)
    stripeSubscriptionId = models.CharField(_('stripe subscription id'), max_length=255)

    objects = CustomUserManager()

    REQUIRED_FIELDS = ['email', 'password']
    USERNAME_FIELD = 'name'

    class Meta:
        db_table = "users"
        verbose_name = _('user')
        verbose_name_plural = _('users')

    def __str__(self):
        """stirng representation"""
        return self.name
