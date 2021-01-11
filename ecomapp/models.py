from django.db import models
from django.contrib.auth.models import User
import datetime
# Create your models here.


class Product(models.Model):
    title = models.CharField(max_length=200)
    
    image = models.ImageField(upload_to="products")
    
    selling_price = models.PositiveIntegerField()
    description = models.TextField()
    Discount= models.PositiveIntegerField()
    

    def __str__(self):
        return self.title

class Order(models.Model):
    product = models.ForeignKey(Product,
                                on_delete=models.CASCADE)
    customer = models.ForeignKey(User,
                                 on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    price = models.IntegerField()
    address = models.CharField(max_length=50, default='', blank=True)
    phone = models.CharField(max_length=50, default='', blank=True)
    date = models.DateField(default=datetime.datetime.today)
    status = models.BooleanField(default=False)

    def placeOrder(self):
        self.save()
    

    @staticmethod
    def get_orders_by_cutomer(customer_id):
        print(customer_id,"idd")
        return Order.objects.filter(customer=customer_id)
    
