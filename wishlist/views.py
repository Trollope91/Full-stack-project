from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.shortcuts import HttpResponse, get_object_or_404, redirect, render

from django.conf import settings
from django.core.mail import BadHeaderError, send_mail
from django.http import HttpResponse

from .models import Product, Wishlist


@login_required
def view_wishlist(request):
    """A view to return the wishlist page"""
    user = request.user
    existing_wishlist = Wishlist.objects.filter(user=user).first()

    try:
        send_mail(
            "Subject Test",
            "Body test",
            "platinumsupps@example.com",
            ["ljt91@gmail.com"],
        )
    except BadHeaderError as e:
        return HttpResponse("Invalid header found.")
    except Exception as e:
        print(f"An error occurred: {e}")

    context = {"wishlist": existing_wishlist}

    return render(request, "wishlist/wishlist.html", context)


@login_required
def add_to_wishlist(request, item_id):
    product = get_object_or_404(Product, pk=item_id)
    user = request.user
    redirect_url = request.POST.get("redirect_url")
    existing_wishlist = Wishlist.objects.filter(user=user).first()

    if existing_wishlist:
        if product not in existing_wishlist.products.all():
            existing_wishlist.products.add(product)
            existing_wishlist.save()
            messages.info(request, f"{product.name} has been added to the wishlist")
        else:
            messages.warning(request, f"{product.name} is already in the wishlist")
    else:
        wishlist = Wishlist(user=user)
        wishlist.save()
        wishlist.products.add(product)
        wishlist.save()
        messages.info(request, f"{product.name} has been added to the wishlist")

    return redirect(redirect_url)


@login_required
def remove_from_wishlist(request, item_id):
    product = get_object_or_404(Product, pk=item_id)
    user = request.user

    wishlist = Wishlist.objects.filter(user=user).first()

    if wishlist:
        if product in wishlist.products.all():
            wishlist.products.remove(product)
            wishlist.save()
            messages.success(
                request, f"{product.name} has been removed from the wishlist"
            )
        else:
            messages.info(request, f"{product.name} is not in the wishlist")
    else:
        messages.info(request, "Your wishlist is empty")

    return HttpResponse(status=200)
