from django import template

register = template.Library()

@register.filter(name = 'is_in_cart')
def is_in_cart(prd, cart):
    keys = cart.keys()
    # print(prd, cart)
    for id in keys:
        # print(type(id), type(prd.Product_ID))
        if id == prd.Product_ID:
            return True
    return False

@register.filter(name = 'cart_quantity')
def cart_quantity(prd, cart):
    keys = cart.keys()
    # print(prd, cart)
    for id in keys:
        # print(type(id), type(prd.Product_ID))
        if id == prd.Product_ID:
            return cart.get(id)
    return 0

@register.filter(name = 'price_total')
def price_total(prd, cart):
    return prd.Product_Price * cart_quantity(prd, cart)


@register.filter(name = 'total_cart_price')
def total_cart_price(products, cart):
    sum = 0;
    for p in products:
        sum += price_total(p, cart)

    return sum