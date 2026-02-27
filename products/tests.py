# Standard libary imports
from decimal import Decimal
# Third-party imports
# Django imports
from django.test import TestCase
# Local imports
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

    def test_product_str(self):
        product = Product.objects.create(
            name="Test Product 2",
            price=Decimal('3.50'),
            description="Add Test Product 2",
        )
        self.assertEqual(str(product), "Test Product 2")

    def test_default_stock_level(self):
        product = Product.objects.create(
            name="Test Product 3",
            price=Decimal('2.50'),
            description="Add Test Product 3",
        )
        self.assertEqual(product.stock_level, 75)
