from django.contrib import admin
from ticketing.models import Offer, Order, Cart

# Register your models here.
admin.site.register(Offer)
admin.site.register(Order)
admin.site.register(Cart)
