from django.contrib.auth import get_user_model
from django.test import TestCase


class UsersManagerTests(TestCase):
    def test_create_user(self):
        username = "John Doe"
        email = 'normal@mail.com'
        password = '123456789'
        User = get_user_model()
        user = User.objects.create_user(username=username, email=email, password=password)
        self.assertEqual(user.email, email)
        self.assertTrue(user.is_active)
        self.assertFalse(user.is_superuser)
        self.assertFalse(user.is_staff)
        with self.assertRaises(TypeError):
            User.objects.create_user()
        with self.assertRaises(TypeError):
            User.objects.create_user(email='')
        with self.assertRaises(ValueError):
            User.objects.create_user(username='', password="foo")

