from django.http import HttpResponse
from django.forms import modelformset_factory
from django.shortcuts import redirect, render, get_object_or_404
from django.urls import reverse
from accounts.models import Customer
from ticketing.forms import OrderForm
from ticketing.models import Offer, Cart, Order
from django.utils import timezone
from django.contrib.auth.decorators import login_required

def index(request):
    offers = Offer.objects.all()
    
    return render(request, 'ticketing/index.html', context={"offers": offers})

def all_offers(request):
    offers = Offer.objects.all()
    return render(request, 'ticketing/offers.html', context={"offers": offers})

def add_to_cart(request, slug):
    user: Customer = request.user
    user.add_to_cart(slug=slug)
    
    return redirect(reverse("ticketing:all-offers"))

@login_required
def cart(request):
    orders = Order.objects.filter(user=request.user)
    if orders.count() == 0:
        return redirect('index')
    # extra = 0 to prevent adding new form for new product
    OrderFormSet = modelformset_factory(Order, form=OrderForm, extra=0)
    formset = OrderFormSet(queryset=orders)
    
    return render(request, 'ticketing/cart.html', context={"forms":formset})

def update_quantities(request):
    OrderFormSet = modelformset_factory(Order, form=OrderForm, extra=0)
    formset = OrderFormSet(request.POST, queryset=Order.objects.filter(user=request.user))
    if formset.is_valid():
        formset.save()
        
    return redirect('ticketing:cart')
    
def create_checkout_session(request):
    # renomme avec payed
    cart = get_object_or_404(Cart, user=request.user)
    cart.ordered = True
    cart.ordered_date = timezone.now()
    cart.save()
    
    return render(request, 'ticketing/payment.html')
