from django.shortcuts import render

from store.models import Product

def frontpage(request):
    products = Product.objects.filter(status=Product.ACTIVE)[0:9]
    return render(request, template_name='core/frontpage.html', context={'products': products})

