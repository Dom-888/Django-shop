from django.shortcuts import render, redirect

# Create your views here.

def view_bag(request):
    return render(request, 'bag/bag.html') 

# Raccoglie dati products/product_detail.html
def add_to_bag(request, item_id):
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

    request.session['bag'] = bag
    print(request.session['bag'])
    return redirect(redirect_url)
