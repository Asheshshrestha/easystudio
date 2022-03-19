from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _
from django.conf import settings
# Create your models here.

class PackageModel(models.Model):
    studio = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.SET_NULL, null=True)
    package_name = models.CharField(max_length=255)
    package_image = models.ImageField(upload_to='studio/package',null=True)
    package_price = models.CharField(max_length=100,null=True)
    package_disc = models.TextField(max_length=2040,null=True)
    in_effect = models.BooleanField(default=True)

    def __str__(self):
        return self.package_name
