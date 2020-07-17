from django.shortcuts import render, redirect, reverse, HttpResponse
from django.contrib import messages # Necessario per i toasts
from products.models import Product

# Create your views here.

def view_bag(request):
    return render(request, 'bag/bag.html') 

# Raccoglie dati products/product_detail.html
def add_to_bag(request, item_id):

    product = Product .objects.get(pk=item_id)

    quantity = int(request.POST.get('quantity'))

    # Necessario per ritornare alla stessa pagina una volta che l'oggetto è stato inserito nel carrello
    redirect_url = request.POST.get('redirect_url')

    size = None
    if 'product_size' in request.POST:
        size = request.POST['product_size']

    # Crea una session variable per conservare le informazioni del carrello
    bag = request.session.get('bag', {})

    if size:
        # Se l'oggetto è già nella bag, controlla se c'è già in quella misura e ne modifica la quantità
        if item_id in list(bag.keys()):
            if size in bag[item_id]['items_by_size'].keys():
                bag[item_id]['items_by_size'][size] += quantity
            else: 
                # Se l'oggetto esiste già ma ha una taglia diversa
                bag[item_id]['items_by_size'][size] = quantity
        else:
            # Se l'oggetto non è nella bag, viene semplicemente aggiunto
            bag[item_id] = {'items_by_size': {size: quantity}}

    else: # No size
        if item_id in list(bag.keys()):
            bag[item_id] += quantity
        else:
            bag[item_id] = quantity
            messages.success(request, f'Added{product.name} to your bag')

    request.session['bag'] = bag
    return redirect(redirect_url)


def adjust_bag(request, item_id):
    """Adjust the quantity of the specified product to the specified amount"""

    quantity = int(request.POST.get('quantity'))
    size = None
    if 'product_size' in request.POST:
        size = request.POST['product_size']
    bag = request.session.get('bag', {})

    if size:
        if quantity > 0:
            bag[item_id]['items_by_size'][size] = quantity
        else:
            del bag[item_id]['items_by_size'][size]
            if not bag[item_id]['items_by_size']:
                bag.pop(item_id)
    else:
        if quantity > 0:
            bag[item_id] = quantity
        else:
            bag.pop(item_id)

    request.session['bag'] = bag
    return redirect(reverse('view_bag'))


def remove_from_bag(request, item_id):
    """Remove the item from the shopping bag"""

    try:
        size = None
        if 'product_size' in request.POST:
            size = request.POST['product_size']
        bag = request.session.get('bag', {})

        if size:
            del bag[item_id]['items_by_size'][size]
            if not bag[item_id]['items_by_size']:
                bag.pop(item_id)
        else:
            bag.pop(item_id)

        request.session['bag'] = bag
        return HttpResponse(status=200)

    except Exception as e:
        return HttpResponse(status=500)