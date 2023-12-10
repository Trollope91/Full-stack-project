from django.contrib import admin

from .models import Category, Product, PromoCodes

# Register your models here.


class ProductAdmin(admin.ModelAdmin):
    list_display = (
        "sku",
        "name",
        "category",
        "price",
        "rating",
        "image",
    )

    ordering = ("sku",)


class CategoryAdmin(admin.ModelAdmin):
    list_display = (
        "friendly_name",
        "name",
    )


class PromoCodeAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "code",
        "discount_percentage",
        "expiry_date",
        "product",
    )


admin.site.register(Product, ProductAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(PromoCodes, PromoCodeAdmin)
