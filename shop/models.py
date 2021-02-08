from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=200)
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