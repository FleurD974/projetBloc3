from django.test import TestCase
from django.urls import reverse

from ticketing.models import Offer


class TicketingTest(TestCase):
    def setUp(self):
        self.offer = Offer.objects.create(
            name="Offre 3",
            spectator_number = 3,
            price = 175,
            stock = 7000,
            description="Une description."
        )
        
    def test_connexion_button_visible_if_not_connected(self):
        response = self.client.get(reverse("index"))
        self.assertIn("Se connecter", str(response.content))
        
    def test_redirect_when_anonymous_user_acces_cart_view(self):
        response = self.client.get(reverse("ticketing:cart"))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, f"{reverse('accounts:login')}?next={reverse('ticketing:cart')}", status_code=302)
        