from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.contrib import messages
from django.db.models import Q # Generate a search query
from .models import Product

# Create your views here.

# Return a view of all products
def all_products(request):

    products = Product.objects.all()

    context = {
        'products': products,
    }

    return render(request, 'products/products.html', context) 

# Return the details of the selected product
def product_detail(request, product_id):
    product = get_object_or_404(Product, pk=product_id)

    # Handle the search query
    query = None

    if request.GET:
        if 'q' in request.GET:
            query = request.GET['q']
            # Se la query è vuota
            if not query:
                messages.error(request, "You didn't enter any search criteria!")
                return redirect(reverse('products'))

            # Cerca sia nel nome del prodotto, sia nella descrizione
            queries = Q(name__icontains=query) | Q(description__icontains=query)
            products = products.filter(queries)

    context = {
        'product': product,
        'search_term': query
    }

    return render(request, 'products/product_detail.html', context) 

