from decimal import Decimal

from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import get_object_or_404

from products.models import Product, PromoCodes


def bag_contents(request):
    bag_items = []
    total = 0
    product_count = 0
    bag = request.session.get("bag", {})
    discount_code = request.session.get("discount_code", None)
    # request.session['discount_code'] = ''

    # request.session['total_discount'] = 0
    request.session["total_discount"] = "0"

    for item_id, item_data in bag.items():
        if isinstance(item_data, int):
            product = get_object_or_404(Product, pk=item_id)
            total += item_data * product.price
            total = apply_discount_to_product(
                request=request,
                product=product,
                total=total,
                discount_code=discount_code,
                quantity=item_data,
            )
            product_count += item_data
            bag_items.append(
                {
                    "item_id": item_id,
                    "quantity": item_data,
                    "product": product,
                }
            )
        else:
            product = get_object_or_404(Product, pk=item_id)

            if getattr(product, "has_weight", False):
                for (
                    weight,
                    quantity,
                ) in item_data["items_by_weight"].items():
                    total += quantity * product.price
                    product_count += quantity
                    total = apply_discount_to_product(
                        request=request,
                        product=product,
                        total=total,
                        discount_code=discount_code,
                        quantity=quantity,
                    )

                    bag_items.append(
                        {
                            "item_id": item_id,
                            "quantity": quantity,
                            "product": product,
                            "weight": weight,
                        }
                    )
            elif getattr(product, "has_sizes", False):
                for (
                    size,
                    quantity,
                ) in item_data["items_by_size"].items():
                    total += quantity * product.price
                    total = apply_discount_to_product(
                        request=request,
                        product=product,
                        total=total,
                        discount_code=discount_code,
                        quantity=quantity,
                    )

                    product_count += quantity
                    bag_items.append(
                        {
                            "item_id": item_id,
                            "quantity": quantity,
                            "product": product,
                            "size": size,
                        }
                    )

    if total < settings.FREE_DELIVERY_THRESHOLD:
        delivery = total * Decimal(settings.STANDARD_DELIVERY_PERCENTAGE / 100)
        free_delivery_delta = settings.FREE_DELIVERY_THRESHOLD - total
    else:
        delivery = 0
        free_delivery_delta = 0

    grand_total = delivery + total

    context = {
        "bag_items": bag_items,
        "total": total,
        "product_count": product_count,
        "delivery": delivery,
        "free_delivery_delta": free_delivery_delta,
        "free_delivery_threshold": settings.FREE_DELIVERY_THRESHOLD,
        "grand_total": grand_total,
    }

    return context


def apply_discount_to_product(request, product, total, discount_code, quantity):
    if discount_code:
        try:
            """
            Retrieve the discount code from the database
            """

            discount = PromoCodes.objects.get(code=discount_code)

            if discount.product.id == product.id:
                """
                Calculate the discounted total
                """
                discountValue = round(
                    (((product.price * quantity) / 100) * discount.discount_percentage),
                    2,
                )

                """
                Retrieve the current total from the session
                """
                original_total_discount = Decimal(
                    request.session.get("total_discount", "0")
                )

                """
                 Update the session with the new discounted total
                """

                request.session["total_discount"] = str(
                    original_total_discount + discountValue
                )

                """
                Calculate the updated total after applying the discount
                """
                discounted_total = total - discountValue

                """
                If you need to use the original total elsewhere, you can keep it in the session
                """

                request.session["original_total"] = str(total)

                """ 
                Return the discounted total
                """
                return discounted_total
        except PromoCodes.DoesNotExist:
            """
            Handle the case where the discount code is not valid
            """
            pass

    """
    Return the original total if no discount is applied or an exception occurs
    """
    return total
