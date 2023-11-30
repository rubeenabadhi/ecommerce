from django.core.paginator import Paginator,EmptyPage,InvalidPage
from django.shortcuts import render, get_object_or_404
from django.db.models import Q
from django.http import HttpResponse
from .models import *

# Create your views here.
def home(request,c_slug=None):
    if c_slug !=None:
        c_page=get_object_or_404(categ,slug=c_slug)
        prod = product.objects.filter(category=c_page,available=True)
    else:
        prod = product.objects.all().filter(available=True)

    cate=categ.objects.all()

    #  .........paginator start..................

    p=Paginator(prod,2)

    pageNum=int(request.GET.get('page',1))

    try:
        proe=p.page(pageNum)
        print(proe)
    except(EmptyPage,InvalidPage):
        proe=p.page(p.num_pages)

#           ..........end paginator...............

    return render(request,'index.html',{'ct':cate,'pro':prod,'pr':proe})

def contact(request):
    return render(request,'contact.html')

def detail(request,c_slug,product_slug):
    prod=product.objects.get(category__slug=c_slug,slug=product_slug)
    return render(request,'product-single.html',{'pro':prod})

def searching(request,):
    if 'q' in request.GET:
        query=request.GET.get('q')
        prod=product.objects.all().filter(Q(name__icontains=query)|Q(descrip__icontains=query),available=True)
    if not prod:
        return HttpResponse('<h1>not available</h1>')

    return render(request,'search.html',{'pr':prod})


def about(request):
    return render(request,'about.html')

