from django.test import TestCase
from django.urls import reverse, resolve
from .views import home
# Create your tests here.


class CheckoutUrls(TestCase):
    def test_checkout_url(self):
        url = reverse('home')
        self.assertEqual(resolve(url).func, home)

    def test_wrong_uri_returns_404(self):
        # taken from CI student - link in readme
        response = self.client.get('/something/different/')
        self.assertEqual(response.status_code, 404)
        self.assertTemplateUsed(response, 'errors/404.html')
