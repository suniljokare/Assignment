from django import template

register=template.Library()
#fucntion to check product present in cart or not

@register.filter(name='is_in_cart')
def is_in_cart(p, cart):
    
    print(p,cart)
    keys= cart.keys()
    for id in keys:
        if int(id)==p.id:
            print("in cart")
            return True
    return False

@register.filter(name='cart_quantity')
def cart_quantity(p  , cart):
    keys = cart.keys()
    for id in keys:
        if int(id) == p.id:
            print("in qua")
            return cart.get(id)

    return 0;

@register.filter(name='price_total')
def price_total(product  , cart):
    
    return product.Discount * cart_quantity(product , cart)

@register.filter(name='total_price_total')
def total_price_total(product  , cart):
    return product.selling_price * cart_quantity(product , cart)

@register.filter(name='total_cart_price')
def total_cart_price(products , cart):
    sum = 0 ;
    for p in products:
        sum += total_price_total(p , cart)

    return sum

@register.filter(name='dis_total_cart_price')
def dis_total_cart_price(products , cart):
    sum = 0 ;
    for p in products:
        sum += price_total(p , cart)

    return sum