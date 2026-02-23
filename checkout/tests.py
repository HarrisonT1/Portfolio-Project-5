from django.test import TestCase
from django.conf import settings
from django.urls import reverse, resolve
from decimal import Decimal
from checkout.models import Order
from checkout.utils import create_line_items
from products.models import Product
from .views import checkout

# Create your tests here.


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

    def test_calculate_order_item_total(self):
        bag = {
            "test-product": 3
        }

        _, order_total = create_line_items(bag)

        self.assertEqual(order_total, Decimal("9.00"))

    def test_order_totals_are_updated(self):
        quantity = 3
        bag = {
            "test-product": quantity
        }

        create_line_items(bag, order=self.order)

        self.order.refresh_from_db()

        expected_order_total = self.product.price * quantity
        expected_grand_total = expected_order_total + self.order.delivery_cost

        self.assertEqual(self.order.order_total, expected_order_total)
        self.assertEqual(self.order.grand_total, expected_grand_total)

    def test_raise_error_when_stock_unavailable(self):
        bag = {
            "test-product": 80
        }

        with self.assertRaises(ValueError):
            create_line_items(bag, order=self.order)

    def test_line_item_is_created(self):
        bag = {
            "test-product": 3
        }

        create_line_items(bag, order=self.order)

        self.assertEqual(self.order.lineitems.count(), 1)

    def test_free_delivery_cost_threshold(self):
        quantity = 75
        bag = {
            "test-product": quantity
        }

        create_line_items(bag, order=self.order)

        self.order.refresh_from_db()
        self.assertGreaterEqual(
            self.order.order_total,
            settings.FREE_DELIVERY_THRESHOLD
        )

        self.assertEqual(self.order.delivery_cost, Decimal("0.00"))

    def test_premium_delivery_cost_applied(self):
        self.order.delivery_method = "premium"
        bag = {
            "test-product": 3
        }

        create_line_items(bag, order=self.order)

        self.order.refresh_from_db()
        self.assertLess(
            self.order.order_total,
            settings.FREE_DELIVERY_THRESHOLD
        )
        self.assertEqual(self.order.delivery_cost, Decimal("10.00"))

    def test_standard_delivery_cost_applied(self):
        bag = {
            "test-product": 3
        }
        create_line_items(bag, order=self.order)
        self.order.refresh_from_db()
        self.assertLess(
            self.order.order_total,
            settings.FREE_DELIVERY_THRESHOLD
        )
        self.assertEqual(self.order.delivery_cost, Decimal("5.00"))


class CheckoutUrls(TestCase):
    def test_checkout_url(self):
        url = reverse('checkout')
        self.assertEqual(resolve(url).func, checkout)

    def test_checkout_redirects_if_bag_empty(self):
        response = self.client.get(reverse('checkout'))
        self.assertRedirects(response, reverse('products'))

    def test_checkout_renders_template(self):
        session = self.client.session
        session['bag'] = {'test-product': {'quantity': 1}}
        session.save()

        response = self.client.get(reverse('checkout'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'checkout/checkout.html')
        self.assertIn('form', response.context)
        self.assertIn('bag_items', response.context)
