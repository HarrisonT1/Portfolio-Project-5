# Standard libary imports
# Third-party imports
# Django imports
from django.contrib.auth.models import User
from django.db import models
# Local imports

# Create your models here.


class Review(models.Model):
    """
    Stores review details
    """
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='reviews'
    )
    rating = models.PositiveSmallIntegerField()

    name = models.TextField(max_length=100)
    review_message = models.TextField()

    created_at = models.DateTimeField(auto_now_add=True)
    approved = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.user.username} - {self.review_message[:20]}'
