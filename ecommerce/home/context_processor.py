from .views import *
from cart.views import *

def cate(request): #create new function
    cate=categ.objects.all() #same variable from views.py
    return {'ct':cate} #same context in view

def cart_total(request):
    tot=0
    count=0
    disc=0
    grand_total=0
    user = request.user
    if user.is_authenticated:
        ct=cartlist.objects.filter(user=user)
    else:
        cart_id=request.session.get('cart_id')
        ct=cartlist.objects.filter(cart_id=cart_id)

    ct_items=items.objects.filter(cart__in=ct,active=True)
    for i in ct_items:
        tot += (i.prod.price * i.quantity)
        count += i.quantity
        disc = tot * (10 / 100)
        grand_total = tot - disc
    return {'ci':ct_items,'t':tot,'cn':count,'dsc':disc,'gt':grand_total}
