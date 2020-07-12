from django.shortcuts import render, redirect

# Create your views here.

def views_bag(request):
    return render(request, 'bag/bag.html') 

# Raccoglie dati products > product_detail.html
def add_to_bag(request, item_id):
    quantity = int(request.POST.get('quantity'))

    # Necessario per ritornare alla stessa pagina una volta che l'oggetto è stato inserito nel carrello
    redirect_url = request.POST.get('redirect_url')

    # Crea una session variable per conservare le informazioni del carrello
    bag = request.session.get('bag', {})

    if item_id in list(bag.keys()):
        bag[item_id] += quantity
    else:
        bag[item_id] = quantity

    request.session['bag'] = bag
    print(request.session['bag'])
    return redirect(redirect_url)
