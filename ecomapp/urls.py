from ecomapp.views import *
from django.urls import path,include


urlpatterns = [
    path('register/',register,name='register'),
    path('login/',login,name='login'),
    path('',Homepage,name='Homepage'),
    path('cart/',cart,name='cart'),
    path('check-out',checkout,name='check-out'),
    path('orders/',your_orders,name='orders'),
    path('logout/',logout,name='logout'),
    path('profile/',profile,name='profile'),
    path('productdetail/<int:id>',productdetail,name='productdetail'),
    path('allproducts/',allproducts,name='allproducts'),
    path('delete_product/<int:id>',delete_product,name='delete_product'),
    path('add_product/',add_product,name='add_product'),
    path('adminregister/',adminregister,name='adminregister'),
    path('update_product/<int:id>',update_product,name='update_product'),
]
