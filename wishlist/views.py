from django.shortcuts import render

def view_wishlist(request):
    """A view to return the wishlist page"""

    return render(request, '/workspace/Full-stack-project/wishlist/templates/wishlist/wishlist.html')
