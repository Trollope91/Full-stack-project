from django.shortcuts import render, redirect, reverse
from django.contrib import messages

from.forms import OrderForm

def checkout(request):
    bag = request.session.get('bag', {})
    if not bag:
        messages.error(request, "There's nothing in your bag at this moment")
        return redirect (reverse('products'))

    order_form = OrderForm()
    template = 'checkout/checkout.html'
    context = {
        'order_form': order_form,
        'stripe_public_key': 'pk_test_51ODRSNJ3mQeiS05JwIv15H2VwIXr4v7ifFPDUO712Oq0BrwT99D9eCtMBuwmOvFaTzTCuD38fVpsTB8QkevtToRs00aG3xExQo',
        'client_secret': 'test client secret',
    }

    return render(request, template, context)
