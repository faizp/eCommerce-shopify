from django.db import models
from django.contrib.auth.models import User
from user.models import Address


class Category(models.Model):
    name = models.CharField(unique=True,max_length=200)
    available = models.BooleanField(default=True)

    def __str__(self):
        return self.name

class Product(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    price = models.FloatField(max_length=10, default=0.00)
    image1 = models.ImageField(default='default_product.jpg', upload_to='products_images')
    image2 = models.ImageField(default='default_product.jpg', upload_to='products_images')
    image3 = models.ImageField(default='default_product.jpg', upload_to='products_images')
    description = models.TextField(blank=False)
    sec_category = models.CharField(max_length=20)
    availability = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)


    def __str__(self):
        return self.name

    @property
    def image1_url(self):
        try:
            url = self.image1.url
        except:
            url = ''
        return url

    @property
    def image2_url(self):
        try:
            url = self.image2.url
        except:
            url = ''
        return url

    @property
    def image3_url(self):
        try:
            url = self.image3.url
        except:
            url = ''
        return url


class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    size = models.CharField(max_length=10, default='SMALL')
    created_date = models.DateTimeField(auto_now_add=True)


class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, default=None)
    quantity = models.IntegerField(default=1)
    price = models.CharField(max_length=7, default=0.0)
    size = models.CharField(max_length=10)
    address = models.ForeignKey(Address, on_delete=models.CASCADE)
    payment_status = models.BooleanField(default=False)
    order_status = models.BooleanField(default=True)
    transaction_id = models.CharField(max_length=256)
    order_date = models.DateTimeField(auto_now_add=True)


