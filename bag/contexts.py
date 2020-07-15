from django.conf import settings
from django.shortcuts import get_object_or_404
from products.models import Product
from decimal import Decimal # Più preciso di float (no roundign error) e pertanto più adatto alla transazioni monetarie

# Keep track of the item in the shopping bag, la differenza con context nelle views è che questo è stato inserito in setting.py e di conseguenza è disponibile in tutte le apps
# More info in https://youtu.be/2G9j34jz42Q

def bag_contents(request):

    # Variabili iniziali
    bag_items = [] # Lista di dizionari, ogniuno dei quali contiene i dettagli di un prodotto nella bag
    total = 0
    product_count = 0
    bag = request.session.get('bag', {})

    # item_data = nel caso di un oggetto senza taglia, è uguale al numero di oggetti,
    # nel caso di un oggetto con taglia, è un dizionario di tutti gli oggetti e la loro taglia

    for item_id, item_data in bag.items(): # Questa è la bag from the session
        if isinstance(item_data, int): # Esegue il codice sottostante solo se per gli oggetti senza taglia, in pratica controlla che item_data sia un integrale (e non un dict)
            product = get_object_or_404(Product, pk=item_id) # pk sta per Primary Key
            total += item_data * product.price
            product_count += item_data
            # Dict del prodotto da aggiungere/aggiornare
            bag_items.append({
                'item_id':item_id,
                'quantity': item_data,
                'product': product,
            })
        else: # Items Con taglia
            product = get_object_or_404(Product, pk=item_id) # pk sta per Primary Key
            for size, quantity in item_data['items_by_size'].items():
                total += quantity * product.price
                product_count += quantity
                # Dict del prodotto da aggiungere/aggiornare
                bag_items.append({
                    'item_id':item_id,
                    'quantity': item_data,
                    'product': product,
                    'size': size,
                })


    # Se il totale è inferiore alla soglia, le spedizioni sono uguali al 10% del totale
    if total < settings.FREE_DELIVERY_THREESHOLD:
        delivery = total * Decimal(settings.STANDARD_DELIVERY_PERCENTAGE)
        # l'ammontare necessario per ragiungere il free delivery
        free_delivery_delta = settings.FREE_DELIVERY_THREESHOLD - total
    # Altrimenti è gratis
    else: 
        delivery = 0
        free_delivery_delta = 0
    
    grand_total = delivery + total

    # Tutte queste variabili sono disponibili in ogni templates, in ogni app
    context = {
        'bag_items': bag_items,
        'total': total,
        'product_count': product_count,
        'delivery': delivery,
        'free_delivery_threeshold': settings.FREE_DELIVERY_THREESHOLD, # Nota che questa variabile ha un'origine esterna al file
        'grand_total': grand_total

    }

    return context
