from django.shortcuts import render, redirect
from django.views import View
from .models import *
from .forms import CustomerRegistrationForm, CustomerProfileForm
from django.contrib import messages
from django.db.models import Q
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator


################## Functions for code optimization ###################

def cart_items_count(request):
    total_items = 0
    if request.user.is_authenticated:
        total_items = len(Cart.objects.filter(user=request.user))
    return total_items

def product_brands(request,category,data=None,price=10000):
    brands = Product.objects.filter(category=category).values_list('brand',flat=True).distinct()
    if data == None:
        products = Product.objects.filter(category=category)
    
    elif data == "below":
        products = Product.objects.filter(category=category).filter(
            discounted_price__lt=price
        )
    elif data == "above":
        products = Product.objects.filter(category=category).filter(
            discounted_price__gt=price
        )
    
    else:
        products = Product.objects.filter(category=category).filter(brand=data)

    detailed_prod = {"products": products,"brands_list":brands,'cart_items_count':cart_items_count(request)}
    
    return detailed_prod



##################-----------------------------------  APIs ------------------------------#####################



############## Authentication Pages (password Reset done directly via URL unsing inbuilt functionality) ###########

def login(request):
    return render(request, "app/login.html")

class CustomerRegistrationView(View):
    def get(self, request):
        form = CustomerRegistrationForm()
        return render(request, "app/customerregistration.html", {"form": form})

    def post(self, request):
        form = CustomerRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "congratulations! Registred successfully!!")
        return render(request, "app/customerregistration.html", {"form": form})


############## Home Page ######################

class home(View):
    def get(self, request):
        topwears = Product.objects.filter(category="TW")
        bottomwears = Product.objects.filter(category="BW")
        mobile = Product.objects.filter(category="M")
        laptop = Product.objects.filter(category="L")
        Watch = Product.objects.filter(category="WW")
        return render(
            request,
            "app/home.html",
            {
                "topwears": topwears,
                "bottomwears": bottomwears,
                "laptop": laptop,
                "mobile": mobile,
                "Watch": Watch,
                "cart_items_count":cart_items_count(request)
            },
        )


def search(request):
    query = request.GET['query']
    if len(query) > 78:
        allprods = Product.objects.none()
    else:
        allprodtitle = Product.objects.filter(title__icontains=query)
        allprodcat = Product.objects.filter(category__icontains=query)
        allprodbrand = Product.objects.filter(brand__icontains=query)
        allprods = allprodtitle.union(allprodcat, allprodbrand)
    if allprods.count() == 0:
        messages.warning(request, "No search results found. Please refine your query.")
    params = {'allprods': allprods, 'query': query}
    return render(request, 'app/search.html', params)

################ product Detail Page ###########

class product_detail(View):
    def get(self, request, pk):
        product = Product.objects.get(pk=pk)
        item_in_cart = Cart.objects.filter(product=product.id, user=request.user).exists()
        print(item_in_cart)
        return render(request, "app/productdetail.html", {"product": product,"item_in_cart":item_in_cart,
                "cart_items_count":cart_items_count(request)})

@login_required
def add_to_cart(request):
    user = request.user
    product_id = request.GET.get("prod_id")
    product = Product.objects.get(id=product_id)
    Cart(user=user, product=product).save()
    return redirect("/product-detail/"+product_id)

def buy_now(request):
    user = request.user
    product_id = request.GET.get("prod_id")
    product = Product.objects.get(id=product_id)
    Cart(user=user, product=product).save()

    return redirect("/checkout")


############### Profile Page ############

@method_decorator(login_required,name='dispatch')
class ProfileView(View):
    def get(self, request):
        form = CustomerProfileForm()
        return render(request, "app/profile.html", {"form": form,"cart_items_count":cart_items_count(request)})

    def post(self, request):
        form = CustomerProfileForm(request.POST)
        if form.is_valid():
            usr = request.user
            name = form.cleaned_data["name"]
            locality = form.cleaned_data["locality"]
            city = form.cleaned_data["city"]
            state = form.cleaned_data["state"]
            zipcode = form.cleaned_data["zipcode"]
            pf_data = Customer(
                user=usr,
                name=name,
                locality=locality,
                city=city,
                state=state,
                zipcode=zipcode,
            )
            pf_data.save()
            messages.success(request, "Profile Updated successfully!!")
        return render(request, "app/profile.html", {"form": form,"cart_items_count":cart_items_count(request)})

@login_required
def address(request):
    addr = Customer.objects.filter(user=request.user)
    return render(request, "app/address.html", {"addr": addr,"cart_items_count":cart_items_count(request)})


################ Cart Page ###############

@login_required
def show_cart(request):
    if request.user.is_authenticated:
        user = request.user
        cart = Cart.objects.filter(user=user)
        amount = 0.0
        shipping_amount = 0.0
        total_amount = 0.0
        cart_product = [p for p in cart]

        if cart_product:
            shipping_amount = 70.0
            for p in cart_product:
                tempamount = p.quantity * p.product.discounted_price
                amount += tempamount
                total_amount = amount + shipping_amount
        return render(
            request,
            "app/addtocart.html",
            {
                "carts": cart,
                "amount": amount,
                "total_amount": total_amount,
                "shipping_amount": shipping_amount,
                "cart_items_count":cart_items_count(request)
            },
        )

def plus_cart(request):
    if request.method == "GET":
        prod_id = request.GET["prod_id"]
        c = Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
        c.quantity += 1
        c.save()
        amount = 0.0
        shipping_amount = 70.0
        cart_product = [p for p in Cart.objects.all() if p.user == request.user]

        for p in cart_product:
            tempamount = p.quantity * p.product.discounted_price
            amount += tempamount
        total_amount = amount + shipping_amount
        data = {"quantity": c.quantity, "total_amount": total_amount, "amount": amount}
        return JsonResponse(data)

def minus_cart(request):
    if request.method == "GET":
        prod_id = request.GET["prod_id"]
        c = Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
        if c.quantity != 0:
            c.quantity -= 1
            c.save()
        else:
            c.delete()
        amount = 0.0
        shipping_amount = 0.0
        total_amount = 0.0
        cart_product = [p for p in Cart.objects.all() if p.user == request.user]
        for p in cart_product:
            tempamount = p.quantity * p.product.discounted_price
            amount += tempamount
        total_amount = amount + shipping_amount
        data = {"quantity": c.quantity, "total_amount": total_amount, "amount": amount}
        return JsonResponse(data)

def remove_cart(request):
    if request.method == "GET":
        prod_id = request.GET["prod_id"]
        c = Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
        c.delete()
        amount = 0.0
        shipping_amount = 0.0
        total_amount = 0.0
        cart_product = [p for p in Cart.objects.all() if p.user == request.user]
        for p in cart_product:
            tempamount = p.quantity * p.product.discounted_price
            amount += tempamount
        total_amount = amount + shipping_amount
        data = {"total_amount": total_amount, "amount": amount}
        return JsonResponse(data)

############### CheckOut Page ############

@login_required
def checkout(request):
    user = request.user
    add = Customer.objects.filter(user=user)
    cart = Cart.objects.filter(user=user)

    amount = 0.0
    shipping_amount = 70.0
    total_amount = 0.0
    cart_product = [p for p in cart]

    if cart_product:
        for p in cart_product:
            tempamount = p.quantity * p.product.discounted_price
            amount += tempamount
        total_amount = amount + shipping_amount
    return render(
        request,
        "app/checkout.html",
        {"carts": cart, "amount": amount, "total_amount": total_amount,'add':add},
    )

def payment_done(request):
    user = request.user
    custid = request.GET.get('custid')
    customer = Customer.objects.get(id=custid)
    cart = Cart.objects.filter(user=user)
    for c in cart:
        PlacedOrder(user=user, customer=customer, product=c.product, quantity=c.quantity).save()
        c.delete()
    return redirect("orders")

############# Ordered Products Page ##########

@login_required
def orders(request):
    op = PlacedOrder.objects.filter(user=request.user)
    return render(request, "app/orders.html",{'order_placed': op})


############# Product Wise different Pages with Filtering ##########

def mobile(request, data=None):
    context_prod = product_brands(request,'M',data)
    return render(request, "app/mobile.html",context_prod)

def laptop(request,data=None):
    context_prod = product_brands(request,'L',data,25000)
    return render(request, "app/laptop.html",context_prod)

def top_wear(request,data=None):
    context_prod = product_brands(request,'TW',data,500)
    return render(request, "app/top_wear.html",context_prod)

def bottom_wear(request,data=None):
    context_prod = product_brands(request,'BW',data,500)
    return render(request, "app/bottom_wear.html",context_prod)

def wrist_watch(request,data=None):
    context_prod = product_brands(request,'WW',data,1000)
    return render(request, "app/watch.html",context_prod)

def foot_wear(request,data=None):
    context_prod = product_brands(request,'FW',data,1000)
    return render(request, "app/foot_wear.html",context_prod)

