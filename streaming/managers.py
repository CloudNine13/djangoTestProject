from django.contrib.auth.base_user import BaseUserManager
from django.db import models


class SubscribeManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(subscription='S')  # Subscribed


class UnsubscribeManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(subscription='N')  # Unsubscribed


class CustomUserManager(BaseUserManager):
    use_in_migration = True

    def _create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError('the given email must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password, **extra_fields):
        extra_fields.setdefault('is_superuser', False)
        extra_fields.setdefault('is_staff', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_staff', True)

        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(email, password, **extra_fields)