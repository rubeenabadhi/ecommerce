from django.shortcuts import render,redirect,get_object_or_404
from django.http import HttpResponse
from .models import *
from home.models import *
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.decorators import login_required
import razorpay
from django.conf import settings

# Create your views here.

def cartDetails(request,tot=0,count=0,disc=0,grand_total=0,cart_item=None,ct_items=None):
    try:
        user=request.user
        if user.is_authenticated:
            ct=cartlist.objects.filter(user=user)

        else:
            cart_id=request.session.get('cart_id')
            ct=cartlist.objects.filter(cart_id=cart_id)
        ct_items=items.objects.filter(cart__in=ct,active=True)
        for i in ct_items:
            tot +=(i.prod.price * i.quantity)
            count += i.quantity
            disc=tot*(10/100)
            grand_total=tot-disc

    except ObjectDoesNotExist:
        return HttpResponse("<script> alert('Empty Cart');window.location='/';</script>")


    return render(request,'cart.html',{'ci':ct_items,'t':tot,'cn':count,'dsc':disc,'gt':grand_total})

def c_id(request):
    ct_id=request.session.session_key
    if not ct_id:
        ct_id=request.session.create()
    return ct_id

@login_required(login_url='login')
def add_cart(request,product_id):
    prod=product.objects.get(id=product_id)
    user=request.user

    try:
        ct=cartlist.objects.get(user=user)
    except cartlist.DoesNotExist:
        ct=cartlist.objects.create(cart_id=c_id(request),user=user)
        ct.save()

    try:
        c_items=items.objects.get(prod=prod,cart=ct)
        if c_items.quantity < c_items.prod.stock:
            c_items.quantity +=1
            prod.stock -=1
            prod.save()
        c_items.save()
    except items.DoesNotExist:
        c_items=items.objects.create(prod=prod,quantity=1,cart=ct)
        prod.stock -=1
        prod.save()
        c_items.save()
    return redirect('cartDetails')

@login_required(login_url='login')
def min_cart(request,product_id):
    user=request.user
    try:
        if user.is_authenticated:
            ct_list=cartlist.objects.filter(user=user)
        else:
            cart_id=request.session.get('cart_id')
            ct_list=cartlist.objects.filter(cart_id=cart_id)
    #ct=cartlist.objects.get(user=user,cart_id=c_id(request))
        if ct_list.exists:
            for ct in ct_list:
                prod=get_object_or_404(product,id=product_id)
                try:
                    c_items=items.objects.get(prod=prod,cart=ct)
                    if c_items.quantity>1:
                        c_items.quantity-=1
                        c_items.save()
                    else:
                        c_items.delete()
                except items.DoesNotExist:
                    pass
    except cartlist.DoesNotExist:
        pass
    return redirect('cartDetails')


@login_required(login_url='login')
def remove_cart(request,product_id):
    user=request.user
    try:
        if user.is_authenticated:
            ct_list=cartlist.objects.filter(user=user)
        else:
            cart_id=request.session.get('cart_id')
            ct_list=cartlist.objects.filter(cart_id=cart_id)
    #ct=cartlist.objects.get(user=user,cart_id=c_id(request))
        if ct_list.exists:
            for ct in ct_list:
                prod=get_object_or_404(product,id=product_id)
                try:
                    c_items=items.objects.get(prod=prod,cart=ct)

                    c_items.delete()
                except items.DoesNotExist:
                    pass
    except cartlist.DoesNotExist:
        pass
    return redirect('cartDetails')

def checkout(request):
    if request.method== 'POST':
        firstname=request.POST['fname']
        lastname=request.POST['lname']
        country=request.POST['country']
        address=request.POST['address']
        towncity=request.POST['city']
        postcodezip=request.POST['pin']
        phone=request.POST['phone']
        email=request.POST['email']
        cart=cartlist.objects.filter(user=request.user).first()
        check_out=Checkout(
            user=request.user,
            cart=cart,
            firstname=firstname,
            lastname=lastname,
            country=country,
            address=address,
            towncity=towncity,
            postcodezip=postcodezip,
            phone=phone,
            email=email)
        check_out.save()
        return redirect('payment')

    return render(request,'checkout.html')
def payments(request):
    if request.method=='POST':
        account_number=request.POST.get('account_number')
        name=request.POST.get('name')
        expiry_month=request.POST.get('expiry_month')
        expiry_year=request.POST.get('expiry_rear')
        cvv=request.POST.get('cvv')

        pay=payment(
            user=request.user,
            account_number=account_number,
            name=name,
            expiry_month=expiry_month,
            expiry_year=expiry_year,
            cvv=cvv

        )
        pay.save()
        user=request.user
        ct=cartlist.objects.get(user=user)
        items.objects.filter(cart=ct).delete()
        return redirect('success')
    return render(request,'payment.html')

def success(request):
    return render(request,'success.html')



