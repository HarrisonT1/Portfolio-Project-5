from django.test import TestCase
from django.contrib.auth.models import User
from .models import Review
from accounts.models import UserAccount

# Create your tests here.


class ReviewModelTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="test",
            email="test@test.com",
            password="123",
        )
        self.profile = UserAccount.objects.create(user=self.user)

    def test_review_creation(self):
        review = Review.objects.create(
            user=self.user,
            rating=5,
            review_message="test message",
        )
        self.assertEqual(
            str(review), f"{self.user.username} - {review.review_message}")
