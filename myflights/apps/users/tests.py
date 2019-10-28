from django.test import TestCase
from django.contrib.auth import get_user_model
from django.db import IntegrityError


class UserManagerTests(TestCase):
    def test_create_user(self):
        User = get_user_model()

        user = User.objects.create_user(
            email='joe@example.com', password='123'
        )

        self.assertEqual(user.email, 'joe@example.com')
        self.assertTrue(user.check_password('123'))
        self.assertTrue(user.is_active)
        self.assertFalse(user.is_staff)
        self.assertFalse(user.is_superuser)
        self.assertIsNone(user.username)

        with self.assertRaises(IntegrityError):
            User.objects.create_user(email=user.email, password='')

        with self.assertRaises(TypeError):
            User.objects.create_user()

        with self.assertRaises(TypeError):
            User.objects.create_user(email='')

        with self.assertRaises(TypeError):
            User.objects.create_user(password='')

        with self.assertRaises(ValueError):
            User.objects.create_user(email='', password='234')

    def test_create_user_with_unsusable_password(self):
        User = get_user_model()

        user = User.objects.create_user(email='joe@example', password=None)

        self.assertFalse(user.has_usable_password())

    def test_create_superuser(self):
        User = get_user_model()

        user = User.objects.create_superuser(
            email='superuser@example.com', password='123'
        )

        self.assertEqual(user.email, 'superuser@example.com')
        self.assertTrue(user.check_password('123'))
        self.assertTrue(user.is_active)
        self.assertTrue(user.is_staff)
        self.assertTrue(user.is_superuser)
        self.assertIsNone(user.username)

        with self.assertRaises(IntegrityError):
            User.objects.create_user(email=user.email, password='')

        with self.assertRaises(TypeError):
            User.objects.create_superuser()

        with self.assertRaises(TypeError):
            User.objects.create_superuser(email='superuser@example.com')

        with self.assertRaises(TypeError):
            User.objects.create_superuser(password='123')

        with self.assertRaises(ValueError):
            User.objects.create_superuser(email='', password='234')

        with self.assertRaises(ValueError):
            User.objects.create_superuser(
                email='superuser2@example.com', password='123', is_superuser=False
            )
