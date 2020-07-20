from django import template


register = template.Library()

# This is template filter (django decorator)
@register.filter(name='calc_subtotal')
def calc_subtotal(price, quantity):
    return price * quantity

# Deve essere inserito in bag.html con la keyword "load"