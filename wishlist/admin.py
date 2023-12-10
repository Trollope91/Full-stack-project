from django.contrib import admin

from .models import Wishlist


class WishlistAdmin(admin.ModelAdmin):
    list_display = (
        "user",
        "display_products",
    )

    def display_products(self, obj):
        return ", ".join([product.name for product in obj.products.all()])

    display_products.short_description = "Products in Wishlist"


admin.site.register(Wishlist, WishlistAdmin)
