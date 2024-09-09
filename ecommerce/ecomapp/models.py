from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Product(models.Model):
    CAT=((1,'Mobile'),(2,'Clothes'),(3,'Footwear'))
    name=models.CharField(max_length=50,verbose_name='Product Name')
    price=models.IntegerField()
    cat=models.IntegerField(verbose_name='Category',choices=CAT)
    pdetail=models.CharField(max_length=200,verbose_name='Product Name')
    is_active=models.BooleanField(default=True)
    image=models.ImageField(upload_to='image')

    def __str__(self):
        return self.name
    
class Cart(models.Model):
    uid=models.ForeignKey('auth.User',on_delete=models.CASCADE,db_column='uid')
    pid=models.ForeignKey('Product',on_delete=models.CASCADE,db_column='pid')
    qty=models.IntegerField(default=1)

class Order(models.Model): 
    uid=models.ForeignKey('auth.User',on_delete=models.CASCADE,db_column='uid')
    pid=models.ForeignKey('Product',on_delete=models.CASCADE,db_column='pid')
    qty=models.IntegerField(default=1)
    amt=models.IntegerField()
    house_no=models.CharField(max_length=200)
    lane=models.CharField(max_length=200)
    area=models.CharField(max_length=200)
    city=models.CharField(max_length=200)
    pin=models.IntegerField()

'''class History(models.model):
    uid=models.ForeignKey('auth.User',on_delete=models.CASCADE,db_column='uid')
    pid=models.ForeignKey('Product',on_delete=models.CASCADE,db_column='pid')
    qty=models.IntegerField(default=1)
    amt=models.IntegerField()'''