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
        """
        Tests that product slugs are automatically generated
        """
        product = Product.objects.create(
            name="Test Product",
            price=Decimal("3.00"),
            description="Add Test Product",
            stock_level=50
        )

        self.assertEqual(product.slug, "test-product")

    def test_product_str(self):
        """
        Test that the product model returns its name
        when converted to a string
        """
        product = Product.objects.create(
            name="Test Product 2",
            price=Decimal('3.50'),
            description="Add Test Product 2",
        )
        self.assertEqual(str(product), "Test Product 2")

    def test_default_stock_level(self):
        """
        Test that the default stock level is 75
        """
        product = Product.objects.create(
            name="Test Product 3",
            price=Decimal('2.50'),
            description="Add Test Product 3",
        )
        self.assertEqual(product.stock_level, 75)
