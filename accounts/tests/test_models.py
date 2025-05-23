from django.test import TestCase

from accounts.models import Customer
from ticketing.models import Offer

class UserTest(TestCase):
    def setUp(self):
        Offer.objects.create(
            name="Offre 3",
            spectator_number = 3,
            price = 175,
            stock = 7000,
            description="Une description."
        )
        self.user = Customer.objects.create_user(
            email="test@gmail.com",
            password="test123"
        )
        
    def test_add_to_empty_cart(self):
        self.user.add_to_cart(slug="offre-3")
        self.assertEqual(self.user.cart.orders.count(), 1)
        self.assertEqual(self.user.cart.orders.first().offer.slug, "offre-3")
        
    def test_add_to_cart_same_article(self):
        self.user.add_to_cart(slug="offre-3")
        self.user.add_to_cart(slug="offre-3")
        self.assertEqual(self.user.cart.orders.count(), 1)
        self.assertEqual(self.user.cart.orders.first().quantity, 2)


