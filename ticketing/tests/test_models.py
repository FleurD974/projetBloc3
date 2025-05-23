from django.test import TestCase
from django.urls import reverse
from accounts.models import Customer
from ticketing.models import Cart, Offer, Order


class ProductTest(TestCase):
    def setUp(self):
        self.offer = Offer.objects.create(
            name="Offre 3",
            spectator_number = 3,
            price = 175,
            stock = 7000,
            description="Une description."
        )
    
    def test_offer_slug_is_automatically_generated(self):
        self.assertEqual(self.offer.slug, "offre-3")

class CartTest(TestCase):
    def setUp(self):
        user = Customer.objects.create_user(
            email="test@gmail.com",
            password="test123"
        )
        offer = Offer.objects.create(name="Offre test")
        self.cart = Cart.objects.create(user=user)
        order = Order.objects.create(
            user=user,
            offer=offer
        )
        self.cart.orders.add(order)
        self.cart.save()
        
    def test_orders_changed_when__cart_is_deleted(self):
        orders_pk = [order.pk for order in self.cart.orders.all()]
        self.cart.delete()
        for order_pk in orders_pk:
            order = Order.objects.get(pk=order_pk)
            self.assertIsNotNone(order.ordered_date)
            self.assertTrue(order.ordered)