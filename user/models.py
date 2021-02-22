from django.db import models
from django.contrib.auth.models import User


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(default='default.jpg', upload_to='profile_pics')
    phone_num = models.CharField(max_length=12)


    def __str__(self):
        return self.user.username


    @property
    def image_url(self):
        try:
            url = self.image.url
        except:
            url = ''
        return url


class Address(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    house_name = models.CharField(max_length=50)
    town = models.CharField(max_length=20)
    district = models.CharField(max_length=20)
    state = models.CharField(max_length=15)
    pin_code = models.IntegerField(default=000000, null=True)
    type = models.CharField(max_length=6)


