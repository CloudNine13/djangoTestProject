from django.db import models
from django.contrib.auth.models import User


class Video(models.Model):
    objects: models.Manager()
    ID = models.CharField(primary_key=True, max_length=50)
    FileName = models.CharField(max_length=50)
    FileSize = models.CharField(max_length=50)
    FileUrl = models.CharField(max_length=50)

    class Meta:
        db_table = "videos"


class ServiceUser(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        primary_key=True,
    )
    stripeCustomerId = models.CharField(max_length=255)
    stripeSubscriptionId = models.CharField(max_length=255)

    class Meta:
        db_table = "users"
