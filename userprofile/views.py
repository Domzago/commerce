from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.utils.text import slugify

from .models import Userprofile
from store.forms import ProductForm
from store.models import Product, Order, OrderItem


def vendor_detail(request, pk):
    user = User.objects.get(pk=pk)
    products = user.products.filter(status= Product.ACTIVE)
    return render(request, template_name='userprofile/vendor_detail.html', context={'user':user, 'products': products})

@login_required
def my_store(request):
    products = request.user.products.exclude(status= Product.DELETED)
    order_items = OrderItem.objects.filter(product__user=request.user)

    return render(request, template_name='userprofile/my_store.html', context={'products': products, 'orderitems': order_items})


@login_required
def my_store_order_detail(request, pk):
    order = get_object_or_404(Order, pk=pk)

    return render(request, template_name='userprofile/my_store_order_detail.html', context={'order': order})

@login_required
def edit_product(request, pk):
    product = Product.objects.filter(user= request.user).get(pk=pk)

    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=product)

        if form.is_valid():
            form.save()

            messages.success(request, 'Product Edited Successfully')

            return redirect('userprofile:my_store')

    else:
        form = ProductForm(instance=product)
    return render(request, template_name='userprofile/product_form.html', context={'title': 'Edit Product', 'product': product,  'form': form})


@login_required
def delete_product(request, pk):
    product = Product.objects.filter(user= request.user).get(pk=pk)
    product.status = product.DELETED
    product.save()

    messages.success(request, 'Product Deleted Successfully')

    return redirect('userprofile:my_store')
    

@login_required
def myaccount(request):
    return render(request, template_name='userprofile/myaccount.html')

@login_required
def add_product(request):
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)

        if form.is_valid():
            title = request.POST.get('title')

            product = form.save(commit=False)
            product.user = request.user
            product.slug = slugify(title)
            product.save()

            messages.success(request, 'Product Added Successfully')

            return redirect('userprofile:my_store')

    else:
        form = ProductForm()
    return render(request, template_name='userprofile/product_form.html', context={'title': 'Add Product','form': form})


def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)

        if form.is_valid():
            user= form.save()

            login(request, user)

            userprofile = Userprofile.objects.create(user=user)

            return redirect('/')
        
    else:
        form = UserCreationForm()

    return render(request, template_name='userprofile/signup.html', context={'form': form})



