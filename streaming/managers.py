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

    def create_user(self, username, email, password, **extra_fields):
        if not email:
            raise ValueError("User must have an email")
        if not username:
            raise ValueError("User must have an username")
        if not password:
            raise ValueError("User must have a password")

        user = self.model(
            email=self.normalize_email(email),
            username=username,
            **extra_fields
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email, password, **extra_fields):
        user = self.create_user(
            email=self.normalize_email(email),
            password=password,
            username=username,
            **extra_fields
        )
        user.is_admin = True
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user
