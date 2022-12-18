from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http.response import JsonResponse
from django.shortcuts import redirect, render
from django.views import View
from .models import Customer, Cart, OrderPlaced, Product, Category, ProductImage
from .forms import CustomerProfileForm, CustomerRegistrationForm
from django.contrib import messages
from django.utils.decorators import method_decorator
from django.utils.safestring import mark_safe
from django.db.models import Q
from django.contrib.auth.decorators import login_required

from app import forms


class ProductView(View):
    def get(self, request):
        first_cat_product = Product.objects.filter(
            category_name=Category.objects.filter()[0])
        second_cat_product = Product.objects.filter(
            category_name=Category.objects.filter()[1])
        third_cat_product = Product.objects.filter(
            category_name=Category.objects.filter()[2])

        context = {'first_cat_product': first_cat_product,
                   'second_cat_product': second_cat_product, 'third_cat_product': third_cat_product}
        return render(request, 'app/home.html', context)


class ProductDetailView(View):
    def get(self, request, id):
        product = Product.objects.get(id=id)
        images = ProductImage.objects.filter(product=product)
        item_in_cart = False
        if request.user.is_authenticated:
            item_in_cart = Cart.objects.filter(
                Q(product=product.id) & Q(user=request.user)).exists()
        return render(request, 'app/productdetail.html', {'product': product, 'images': images, 'item_in_cart': item_in_cart})


def product(request, cats):
    if cats == None:
        search = request.GEt.get('search')
        print(search)
        cat_item = product.objects.filter(body_text__search=search)
    else:
        cat_item = Product.objects.filter(category_name=cats)
    return render(request, 'app/product.html', {'cat_item': cat_item})


@login_required
def cart(request):
    if request.user.is_authenticated:
        user = request.user
        cart = Cart.objects.filter(user=user)

        amount = 0.0
        total_amount = 0.0
        shipping_amount = 70.0
        cart_product = [p for p in Cart.objects.all() if p.user == user]
        if cart_product:
            for p in cart_product:
                tempamount = (p.quantity * p.product.discounted_price)
                amount += tempamount
                total_amount = amount + shipping_amount
        else:
            messages.info(request, mark_safe(
                'Your Cart is Empty! Start Shopping <a href="/">Start</a>'))
        context = {'carts': cart, 'amount': amount,
                   'total_amount': total_amount}
        return render(request, 'app/cart.html', context)


@login_required
def AddToCart(request, prod_id):
    product = Product.objects.get(id=prod_id)
    Cart(user=request.user, product=product).save()
    messages.success(
        request,
        'Product added in your Cart.')
    return redirect('/')


@login_required
def UpdateItem(request):
    if request.method == 'GET':
        prod_id = request.GET['prod_id']
        action = request.GET['action']
        c = Cart.objects.get(Q(product=prod_id) & Q(user=request.user))

        if action == 'add':
            c.quantity += 1
        elif action == 'minus':
            c.quantity -= 1
        c.save()
        if c.quantity == 0 or action == 'delete':
            c.delete()

        amount = 0.0
        total_amount = 0.0
        shipping_amount = 70.0
        cart_product = [p for p in Cart.objects.all() if p.user ==
                        request.user]
        if cart_product:
            for p in cart_product:
                tempamount = (p.quantity * p.product.discounted_price)
                amount += tempamount

        data = {

            'quantity': c.quantity,
            'amount': amount,
            'total_amount': amount + shipping_amount
        }
        return JsonResponse(data)


def buy_now(request):
    return render(request, 'app/buynow.html')


@method_decorator(login_required, name='dispatch')
class CustomerProfileViews(View):
    def get(self, request):
        form = CustomerProfileForm()
        return render(request, 'app/profile.html', {'form': form, 'active': 'btn-primary'})

    def post(self, request):
        form = CustomerProfileForm(request.POST)
        if form.is_valid():
            usr = request.user
            name = form.cleaned_data['name']
            locality = form.cleaned_data['locality']
            city = form.cleaned_data['city']
            state = form.cleaned_data['state']
            zipcode = form.cleaned_data['zipcode']
            data = Customer(user=usr, name=name, locality=locality,
                            city=city, state=state, zipcode=zipcode)
            data.save()
            messages.success(
                request, 'Congratulation !! Profile Updated Successfully')
            form = CustomerProfileForm()
            return render(request, 'app/profile.html', {'form': form, 'active': 'btn-primary'})


@login_required
def address(request):
    add = Customer.objects.filter(user=request.user)
    return render(request, 'app/address.html', {'add': add, 'active': 'btn-primary'})


@login_required
def orders(request):
    item = OrderPlaced.objects.filter(user=request.user)

    return render(request, 'app/orders.html', {'items': item})


class CustomerRegistrationView(View):
    def get(self, request):
        if request.user.is_authenticated:
            return redirect('/')
        else:
            form = CustomerRegistrationForm()
            return render(request, 'app/customerregistration.html', {'form': form})

    def post(self, request):
        if request.user.is_authenticated:
            return redirect('/')
        else:
            form = CustomerRegistrationForm(request.POST)
            if form.is_valid():
                messages.success(
                    request, 'Congratulations !! Registered Successfully')
                form.save()
            return render(request, 'app/customerregistration.html', {'form': form})


@ login_required
def checkout(request):
    user = request.user
    items = Cart.objects.filter(user=user)
    address = Customer.objects.filter(user=user)
    amount = 0.0
    total_amount = 0.0
    shipping_amount = 70.0
    cart_product = [p for p in Cart.objects.all() if p.user ==
                    request.user]
    if cart_product:
        for p in cart_product:
            tempamount = (p.quantity * p.product.discounted_price)
            amount += tempamount
            total_amount = amount + shipping_amount
    context = {'address': address, 'items': items,
               'total_amount': total_amount}
    return render(request, 'app/checkout.html', context)


@ login_required
def PaymentDone(request):
    user = request.user
    id = request.GET.get('custid')
    if id != None:
        customer = Customer.objects.get(id=id)
        cart = Cart.objects.filter(user=user)
        for c in cart:
            OrderPlaced(user=user, customer=customer,
                        product=c.product, quantity=c.quantity).save()
            c.delete()
        return redirect("orders")
    else:
        messages.info(
            request, 'Add Address')
        return redirect('profile')
