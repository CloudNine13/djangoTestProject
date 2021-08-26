from django.db import models
from django.contrib.auth.models import User


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
