from django.shortcuts import render,redirect
from .forms import *
from django.contrib import auth
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.views.decorators.csrf import csrf_exempt
from .models import *
from django.core.paginator import Paginator
import datetime
from django.contrib import messages 
# Create your views here.

@csrf_exempt
def register(request):
    if request.method=='POST':
        username = request.POST["username"]
        password = request.POST["password"]
        email = request.POST["email"]
        first_name = request.POST["first_name"]
        last_name = request.POST["last_name"]
        print((username, email, password))
        user = User.objects.create_user(username=username, email=email, password=password,first_name=first_name,last_name=last_name)
        print(user)
        return redirect('login')
    else:
        form=CustomerRegistrationForm()
        return render(request,'ecomapp/register.html',{'form':form})

@csrf_exempt
def login(request):  
    if request.method=='POST':
        uname = request.POST["username"]
        pword = request.POST["password"]
        print(uname,pword)
        usr = auth.authenticate(username=uname, password=pword)
        if usr is not None:
            auth.login(request, usr)
            print("logged in successfully")
        
            if usr.is_superuser==True:
                return redirect('allproducts')
            if usr.is_staff==True:
                return redirect('allproducts')
            else:
                return redirect('Homepage')
        else:
            messages.error(request, "Username or Password wrong")
        form=CustomerLoginForm()
        return render(request,'ecomapp/login.html',{'form':form})
    else:
        form=CustomerLoginForm()
        return render(request,'ecomapp/login.html',{'form':form})

@csrf_exempt
def Homepage(request):
    if request.method=='POST':
        product = request.POST.get('product')
        remove = request.POST.get('remove')
        cart = request.session.get('cart')
        if cart:
            print("1")
            quantity = cart.get(product)
            if quantity:
                print("2")
                if remove:
                    print("3")
                    if quantity<=1:
                        print("4")
                        cart.pop(product)
                        msg="Product Removed From Cart"
                    else:
                        print("5")
                        msg="Product Removed From Cart"
                        cart[product]  = quantity-1
                else:
                    print("6")
                    msg="Producr Added in cart"

                    cart[product]  = quantity+1

            else:
                msg="Producr Added in cart"
                print("7")
                cart[product] = 1
        else:
            print("8")
            cart = {}
            cart[product] = 1
            msg="Producr Added in cart"
        print("9")
        request.session['cart'] = cart
        print('cart' , request.session['cart'])
        messages.success(request, msg)
        return redirect('Homepage')
    else:
        cart=request.session.get('cart')
        if not cart:
            request.session.cart={}
        all_products = Product.objects.all().order_by("-id")
        # print(all_products)
        paginator = Paginator(all_products, 6)
        page_number = request.GET.get('page')
        # print(page_number)
        product_list = paginator.get_page(page_number)
        # print(product_list)
        return render(request,'ecomapp/home2.html',{'product_list':product_list})

@csrf_exempt
def cart(request):
    cart=request.session.get('cart')
    if cart:
        ids= list(request.session.get('cart').keys())
        products= Product.objects.filter(id__in=ids)
    else:
        cart=request.session.get('cart')
        if not cart:
            request.session.cart={}
        products={}
    return render(request,'ecomapp/cart.html',{'products':products})
   
    
@csrf_exempt
def checkout(request):
    if request.user.is_authenticated:

        if request.method=='POST':
            address = request.POST.get('address')
            phone = request.POST.get('phone')
            cart = request.session.get('cart')
            ids= list(request.session.get('cart').keys())
            products = Product.objects.filter(id__in=ids).order_by('-id')   
            for product in products:
                print(cart.get(str(product.id)))
                order = Order(customer=request.user,
                            product=product,
                            price=product.selling_price,
                            address=address,
                            phone=phone,
                            quantity=cart.get(str(product.id)))
                print(order,"ooooo")
                order.save()
            request.session['cart'] = {}
            messages.success(request,"You have placed order succesfully")
            return redirect('orders')
    else:
        return redirect('login')

def your_orders(request):
    print("in function")
    # customer=request.session.get('cutomer')
    orders=Order.get_orders_by_cutomer(request.user)
    print(orders.values(),"orders")
    return render(request,'ecomapp/orders.html',{"orders":orders}) 

def logout(request):
    print("in logout")
    auth.logout(request)
    return redirect(login)

def profile(request):
    user_data=list(User.objects.filter(username=request.user).values())
    for i in user_data:
        if i['is_active']==True:
            i['is_active']='Active'
        
    return render(request,'ecomapp/profile.html',{"user_data":user_data})

@csrf_exempt
def productdetail(request,id):
    product=Product.objects.filter(id=id).first()
    print(product)
    return render(request,'ecomapp/productdetails.html',{'product':product})
@csrf_exempt
def allproducts(request):
    allproducts=Product.objects.all().order_by('-id')
    return render(request,'ecomapp/allproduct.html',{'allproducts':allproducts})
@csrf_exempt
def delete_product(request,id):
    del_prod=Product.objects.get(id=id)
    del_prod.delete()
    messages.success(request,"Product Deleted Successfully")
    return redirect('allproducts')
@csrf_exempt
def add_product(request):
    if request.method=='GET':
        Product_form=ProductForm()
        return render(request,'ecomapp/addproduct.html',{'form':Product_form})
    else:
        Product_form=ProductForm(request.POST,request.FILES)
        if Product_form.is_valid():
            Product_form.save()
        messages.success(request,"Product Created Successfully")
        return redirect('allproducts')
        
            
@csrf_exempt
def adminregister(request):
    if request.method=='GET':
        form=AdminRegistrationForm()
        return render(request,'ecomapp/adminregister.html',{'form':form})
    if request.method=='POST':
        print(request.POST,"admin data")
        form=AdminRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
        user=User.objects.get(username=request.POST['username'])
        member=request.POST.get('member')
        if member=='Staff':
            user.is_staff=True
            user.set_password(request.POST.get('password'))
            user.save()
        else:
            user.is_superuser=True
            user.is_staff=False
            user.set_password(request.POST.get('password'))
            user.save()
        return redirect('login')
@csrf_exempt
def update_product(request,id=None):
    if request.method=='GET':
        print(id,"iddd")
        product=Product.objects.get(id=id)
        print(product,"product")
        form=ProductForm(instance=product)
        print(request.path,"path")
        # profile_form = ProductForm(instance=request.user.profile)
        return render(request,'ecomapp/addproduct.html',{'form':form,"id":id})
    if request.method=='POST':
        instance=Product.objects.get(id=id)
        Product_form=ProductForm(request.POST,request.FILES,instance=instance)
        print(Product_form.errors)
        if Product_form.is_valid():
            Product_form.save()
        messages.success(request,"Product Updated Successfully")
        return redirect('allproducts')
