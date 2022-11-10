import uuid
import json
import requests

# from email import message
# import imp
from django.shortcuts import redirect, render, HttpResponse
from django.contrib.auth import logout, login, authenticate
from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
from django.views.generic import View

from . forms import *
from . models import *

# Create your views here.
def index(request):
    latest = Product.objects.filter(latest=True)
    trending = Product.objects.filter(trending=True)
    food = Product.objects.all()
   # profile = Profile.objects.get(user__username= request.user.username)

    context = {
        # 'vic':latest,
        'food':food,
        'math':trending,
        'profile':profile,
    }
    return render(request,'index.html', context)

def contact(request):
    form = ContactForm()#instatiate the contactform for a get request
    if request.method == 'POST': #make a POST REQUEST
        form = ContactForm(request.POST)#instatiate the ContactForm for a POST request
        if form.is_valid():#Django will validate the form
            form.save()#if valid save the data to the DB
            messages.success(request, 'message sent.')
            return redirect('index')#return to index once the post action is carried out
    return render(request, 'index.html')

# def product(request):
#     product = Product.objects.all()

#     context = {
#         'product':product,
#     }
#     return render(request, 'product.html', context)


# authentication
def signout(request):
    logout(request)
    return redirect('signin')


def signin(request):
    if request.method == 'POST':
        usernamee = request.POST['username']
        passwrodd = request.POST['password']
        user = authenticate(request,username= usernamee, password=passwrodd)
        if user is not None:
            login(request, user)
            messages.success(request, 'Signin successfull')
            return redirect('index')
        else:
            messages.warning(request, 'Username/Password incorrect.')
            return redirect('index')
    return render(request, 'signin.html')

def signup(request):
    form = SignupForm()
    if request.method == 'POST':
        phone = request.POST['phone']
        form = SignupForm(request.POST)
        if form.is_valid():
            newuser = form.save()
            newprofile = Profile(user= newuser)
            newprofile.first_name= newuser.first_name
            newprofile.last_name= newuser.last_name
            newprofile.email= newuser.email
            newprofile.phone= phone
            newprofile.save()
            login(request, newuser)
            messages.success(request, 'Signup succesful')
            return redirect('index')
        else:
            messages.error(request, form.errors)
            return redirect('signup')

    return render(request, 'signup.html')
# authentication done

# profile
@login_required(login_url='signin')
def profile(request):
    profile = Profile.objects.get(user__username = request.user.username)

    context = {
        'profile':profile
    }
    return render(request, 'profile.html', context)


@login_required(login_url='signin')
def profile_update(request):
    profile = Profile.objects.get(user__username = request.user.username)
    update = ProfileUpdate(instance=request.user.profile)
    if request.method == 'POST':
        update = ProfileUpdate(request.POST, request.FILES,  instance=request.user.profile)
        if update.is_valid:
            update.save()
            messages.success(request, 'profile updated successfully')
            return redirect('profile')
        else:
            messages.error(request, 'incorrect details')
            return redirect('profile_update')

    context = {
        'profile':profile,
        'update':update,
    }
    return render(request, 'profile_update.html', context)


# profile done

def product(request):
    breakfast = Product.objects.filter(breakfast=True)
    lunch = Product.objects.filter(lunch=True)
    dinner = Product.objects.filter(dinner=True)
    dessert = Product.objects.filter(dessert=True)

    context = {
        'breakfast':breakfast,
        'lunch':lunch,
        'dinner':dinner,
        'dessert':dessert,
    }
    return render(request, 'product.html', context)


def detail(request, id):
    detail = Product.objects.get(pk=id)
    context = {
        'detail':detail,
    }
    return render(request, 'detail.html', context)


# shopcart
@login_required(login_url='signin')
def shopcart(request):
    if request.method == 'POST':
        quant = int(request.POST['quantity'])
        item_id = request.POST['product']
        item = Product.objects.get(pk=item_id)
        profile = Profile.objects.get(user__username = request.user.username)
        cart_no = profile.id

        cart = Shopcart.objects.filter(user__username = request.user.username, paid= False)#Shopper with unpaid items
        if cart:# existing order(object) with a selected item quantity to be incremented
            basket = Shopcart.objects.filter(product_id = item.id, user__username = request.user.username).first()
            if basket:
                basket.quantity += quant 
                basket.amount = item.price * quant
                basket.save()
                messages.success(request, 'Item added to cart.')
                return redirect('product')
            else:
                newitem = Shopcart()
                newitem.user = request.user
                newitem.product = item
                newitem.quantity = quant
                newitem.price = item.price 
                newitem.amount = item.price * quant
                newitem.order_no = cart_no 
                newitem.paid = False
                newitem.save()
                messages.success(request, 'Item added to cart.')
                return redirect('index')
            
        else:
            newcart = Shopcart() #create an order for the first time
            newcart.user = request.user
            newcart.product = item
            newcart.quantity = quant
            newcart.price = item.price
            newcart.amount = item.price * quant
            newcart.order_no = cart_no 
            newcart.paid = False
            newcart.save()
            messages.success(request, 'Item added to Shopcart.')
            return redirect('index')

    return redirect('index')



def about(request):
    return render(request, 'about.html')

def displaycart(request):
    trolley = Shopcart.objects.filter(user__username = request.user.username, paid=False)
    profile = Profile.objects.get(user__username = request.user.username)

    subtotal = 0
    vat = 0
    total = 0

    for cart in trolley:
        subtotal += cart.price * cart.quantity

    vat = 0.075 * subtotal

    total = vat + subtotal


    context = {
        'trolley':trolley,
        'subtotal':subtotal,
        'vat':vat,
        'total':total,
        'profile':profile,
    }
    return render(request, 'displaycart.html',context)


def deleteitem(request):
    if request.method == 'POST':
        item_id = request.POST['item_id']
        item_delete = Shopcart.objects.get(pk=item_id)
        item_delete.delete()
        messages.success(request, 'Item deleted succesfully.')
        return redirect('displaycart')

def increase(request):
    if request.method == 'POST':
        the_item = request.POST['itemid']
        the_quant = int(request.POST['quant'])
        modify = Shopcart.objects.get(pk=the_item)
        modify.quantity += the_quant
        modify.amount = modify.price * modify.quantity
        modify.save()
        messages.success(request, 'Quantity modified')
        return redirect('displaycart')


class CheckoutView(View):
    def get(self, request, *args, **kwargs):
        summary = Shopcart.objects.filter(user__username = request.user.username, paid=False)

        subtotal = 0
        vat = 0
        total = 0

        for cart in summary:
            subtotal += cart.price * cart.quantity

        vat = 0.075 * subtotal

        total = vat + subtotal

        context = {
            'summary':summary,
            'total':total,
        }
        return render(request, 'checkout.html', context)

#checkout using class based view and axios get request done


def pay(request):
  if request.method == 'POST':
    # collect data to sendout to paystack
    api_key = 'sk_test_be6ec1bb91a445f556403cce62354e38ea76ed1a'
    curl = 'https://api.paystack.co/transaction/initialize'
    cburl = 'https://34.207.234.114/callback'
    # cburl = 'https://localhost:8000/callback'
    user = User.objects.get(username = request.user.username)
    email = user.email
    total = float(request.POST['total']) * 100
    cart_no = user.profile.id 
    transac_code = str(uuid.uuid4())

    headers = {'Authorization': f'Bearer {api_key}'}
    data = {'reference':transac_code, 'amount':int(total),'email':email,
     'order_number':cart_no, 'callback_url':cburl, 'currency':'NGN'}

    # integrating to paystack
    try:
        r = requests.post(curl, headers=headers, json=data)
    except Exception:
        messages.error(request, 'Network busy, refresh and try again')
    else:
        transback = json.loads(r.text)
        rdurl = transback['data']['authorization.url']
        return redirect(rdurl)
    return redirect('displaycart')


def callback(request):
    profile = Profile.objects.get(user_username = request.user.username)
    cart =Shopcart.objects.filter(user_username = request.user.username, paid=False)

    for pro in cart:
        pro.paid = True
        pro.save()

        stock = Product.objects.get(pk=pro.product.id)
        stock.max_quantity -= pro.quantity
        stock.save()

    context = {
        'profile':profile
    }
    return render(request, 'callback.html', context)



    
