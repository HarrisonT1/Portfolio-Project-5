# Standard libary imports
# Third-party imports
# Django imports
from django.test import TestCase
from django.urls import reverse, resolve
# Local imports
from .views import home, privacy_policy
# Create your tests here.


class HomeUrls(TestCase):
    def test_home_url(self):
        """
        Tests home url
        """
        url = reverse('home')
        self.assertEqual(resolve(url).func, home)

    # taken from CI student - link in readme
    def test_wrong_uri_returns_404(self):
        """
        Tests 404 page url
        """
        response = self.client.get('/something/different/')
        self.assertEqual(response.status_code, 404)
        self.assertTemplateUsed(response, 'errors/404.html')

    def test_privacy_policy(self):
        """
        Test privacy policy url
        """
        url = reverse('privacy_policy')
        self.assertEqual(resolve(url).func, privacy_policy)
