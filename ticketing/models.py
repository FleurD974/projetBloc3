from django.db import models
from django.urls import reverse
from django.utils import timezone
from django.utils.text import slugify

from billeterieJO.settings import AUTH_USER_MODEL


# Model for the different offers
class Offer(models.Model):
    name = models.CharField(max_length=50)
    slug = models.SlugField(max_length=50, blank=True)
    spectator_number = models.IntegerField(default=0)
    price = models.FloatField(default=0.0)
    stock = models.IntegerField(default=0)
    description = models.TextField(blank=True)
    
    def __str__(self):
        return f"{self.name} ({self.stock})"
    
    def get_absolute_url(self):
        return reverse("ticketing:offer", kwargs={"slug": self.slug})
    
    def save(self, *args, **kwargs):
        self.slug = self.slug or slugify(self.name)
        super().save(*args, **kwargs)
        

# Model for order
class Order(models.Model):
    user = models.ForeignKey(AUTH_USER_MODEL, on_delete=models.CASCADE)
    offer = models.ForeignKey(Offer, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    ordered = models.BooleanField(default=False)
    ordered_date = models.DateTimeField(blank=True, null=True)
    
    def __str__(self):
        return f"{self.offer.name} ({self.quantity})"


# Model for cart containing orders
class Cart(models.Model):
    user = models.OneToOneField(AUTH_USER_MODEL, on_delete=models.CASCADE)
    orders = models.ManyToManyField(Order)
    total = models.FloatField(default=0.0)
    ordered = models.BooleanField(default=False)
    ordered_date = models.DateTimeField(blank=True,null=True)
    generated_key =models.CharField(max_length=255, default="")
    
    def __str__(self):
        return f"{self.user.email} ({self.total})"
    
    def delete(self, *args, **kwargs):
        for order in self.orders.all():
            order.ordered = True
            order.ordered_date = timezone.now()
            order.save()
            
        self.orders.clear()
        super().delete(*args, **kwargs)