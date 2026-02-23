from django.test import TestCase
from decimal import Decimal


from .models import Product


# Create your tests here.


class ProductModelTest(TestCase):
    def test_automatic_generated_slug(self):
        product = Product.objects.create(
            name="Test Product",
            price=Decimal("3.00"),
            description="Add Test Product",
            stock_level=50
        )

        self.assertEqual(product.slug, "test-product")
