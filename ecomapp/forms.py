from .models import *
from django.contrib.auth.models import User
from django import forms
# from django.core  import validators


class CustomerRegistrationForm(forms.ModelForm):
    username = forms.CharField(widget=forms.TextInput())
    first_name = forms.CharField(widget=forms.TextInput())
    last_name = forms.CharField(widget=forms.TextInput())
    password = forms.CharField(widget=forms.PasswordInput())
    email = forms.CharField(widget=forms.EmailInput())

    class Meta:
        model = User
        fields = ["first_name","last_name","username", "password", "email"]

class AdminRegistrationForm(forms.ModelForm):
    statuss=[('Admin','Admin'),
        ('Staff','Staff')]
    username = forms.CharField(widget=forms.TextInput())
    first_name = forms.CharField(widget=forms.TextInput())
    last_name = forms.CharField(widget=forms.TextInput())
    password = forms.CharField(widget=forms.PasswordInput())
    email = forms.CharField(widget=forms.EmailInput())

    member=forms.ChoiceField(choices=statuss)
    class Meta:
        model = User
        fields = ["first_name","last_name","username", "password", "email",'member']

class CustomerLoginForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput())
    password = forms.CharField(widget=forms.PasswordInput())

class ProductForm(forms.ModelForm):
   
    class Meta:
        model = Product
        fields = ["title",  "image",
                  "selling_price", "description","Discount"]
        widgets = {
            "title": forms.TextInput( attrs={
                "class": "form-control",
                "placeholder": "Enter the product title here...",
                "required":"True"
            }),
            
            
            "image": forms.ClearableFileInput(attrs={
                "class": "form-control",
                "id":"image_product"
            }),
            
            "selling_price": forms.NumberInput(attrs={
                "class": "form-control",
                "placeholder": "Selling price of the product..."
            }),
            "description": forms.Textarea(attrs={
                "class": "form-control",
                "placeholder": "Description of the product...",
                "rows": 5
            }),
            "Discount": forms.NumberInput(attrs={
                "class": "form-control",
                "placeholder": "Selling price of the product..."
            }),
           
            

        }

