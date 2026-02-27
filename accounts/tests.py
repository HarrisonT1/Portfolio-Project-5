# Standard libary imports
# Third-party imports
# Django imports
from django.contrib.auth.models import User
from django.test import TestCase
# Local imports
from .models import UserAccount

# Create your tests here.


class UserAccountModelTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="test",
            email="test@test.com",
            password="123",
        )
        self.profile = UserAccount.objects.create(user=self.user)

    def test_user_account_create(self):
        self.assertEqual(self.profile.user.username, self.user.username)

    def test_user_edit_account(self):
        self.profile.default_email = 'testchange@test.com'
        self.profile.save()
        self.profile.refresh_from_db()
        self.assertEqual(self.profile.default_email, "testchange@test.com")
