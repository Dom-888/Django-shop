from django.shortcuts import render
from .models import Product

# Create your views here.

# Return a view of all products
def all_products(request):

    products = Product.objects.all()

    context = {
        'products': products,
    }

    return render(request, 'products/products.html', context) 