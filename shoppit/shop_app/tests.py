from django.test import TestCase
from .models import Product, Cart, CartItem

class ProductModelTest(TestCase):
    def test_slug_is_unique(self):
        p1 = Product.objects.create(name="Test Product", price=10)
        p2 = Product.objects.create(name="Test Product", price=20)
        self.assertNotEqual(p1.slug, p2.slug)

class CartItemTest(TestCase):
    def test_cartitem_str(self):
        product = Product.objects.create(name="Test", price=5)
        cart = Cart.objects.create(cart_code="12345")
        item = CartItem.objects.create(cart=cart, product=product, quantity=2)
        self.assertIn("2 x Test", str(item))

# Add more tests for views and serializers as needed
