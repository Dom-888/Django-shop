from django.conf import settings
from decimal import Decimal # Più preciso di float (no roundign error) e pertanto più adatto alla transazioni monetarie

# Keep track of the item in the shopping bag, la differenza con context nelle views è che questo è stato inserito in setting.py e di conseguenza è disponibile in tutte le apps
# More info in https://youtu.be/2G9j34jz42Q

def bag_contents(request):

    # Variabili iniziali
    bag_items = []
    total = 0
    product_count = 0

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
        'free_delivery_threeshold': settings.FREE_DELIVERY_THREESHOLD, # Nota che questa variabile ha un'origine esterna alla pagina
        'grand_total': grand_total

    }

    return context