from django.test import TestCase
from decimal import Decimal
from checkout.models import Order
from checkout.utils import create_line_items


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


class CreateLineItemsTest(TestCase):
    def setUp(self):
        self.product = Product.objects.create(
            name="Test Product",
            slug="test-product",
            price=Decimal("3.00"),
            description="Add Test Product",
            stock_level=75,
        )

        self.order = Order.objects.create(
            user=None,
            full_name="test test",
            email="test@test.com",
            phone_number="123456789",
            country="GB",
            postcode="test",
            city="test",
            town="test",
            street_address1="test",
            delivery_method="standard",
            stripe_pid="test",
        )

    def test_calculate_stock_total(self):
        bag = {
            "test-product": 3
        }

        initial_stock = self.product.stock_level

        create_line_items(bag, order=self.order)

        self.product.refresh_from_db()

        self.assertEqual(
            self.product.stock_level, initial_stock - 3
        )

    def test_calculate_order_grand_total(self):
        bag = {
            "test-product": 3
        }

        _, order_total = create_line_items(bag)

        self.assertEqual(order_total, Decimal("9.00"))
