from django.test import TestCase
from django.contrib.auth.models import User
from .models import UserAccount

# Create your tests here.


class UserAccountModelTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="test",
            email="test@test.com",
            password="123",
        )

    def test_user_account_create(self):
        profile = UserAccount.objects.create(user=self.user)
        self.assertEqual(profile.user.username, self.user.username)
