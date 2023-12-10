from django.contrib.auth.models import User
from django.db import models

from products.models import Product

# Create your models here.


class Wishlist(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    products = models.ManyToManyField(Product, related_name="wishlists", blank=True)

    def __str__(self):
        return f"{self.user.username}'s Wishlist"
