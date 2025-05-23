"""Module managing the urls."""
from django.urls import path
from ticketing.views import add_to_cart, cart, create_checkout_session, update_quantities, all_offers

app_name = 'ticketing'

urlpatterns = [
    path('cart/', cart, name="cart"),
    path('cart/update-quantities', update_quantities, name="update-quantities"),
    path('cart/create-checkout-session', create_checkout_session, name="create-checkout-session"),
    path('offers', all_offers, name="all-offers"),
    path('offer/<str:slug>/add-to-cart', add_to_cart, name="add-to-cart"),
]
