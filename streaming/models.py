from django.db import models
from django.contrib.auth.models import User


class User(models.Model):
    def __str__(self):
        return f"User: name:{self.user.username}, password_length"


def create_user(name, surname, username, phone_number, p, email):
    if username is None:
        username = name + surname
    user = User.objects.create_user(
        username=username,
        email=email,
        password=p,
        extra_fields={"phone_number": phone_number}
    )
    user.save()
