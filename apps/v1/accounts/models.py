from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _
from django.conf import settings
# Create your models here.

class User(AbstractUser):
    ROLES = (("0","User"),("1","Studio"),("2","Admin"))
    role = models.CharField(max_length=1, choices= ROLES)
    email = models.EmailField(_('email address'),blank=False,unique=True)

    USERNAME_FIELD = 'username'
    REQUIERED_FIELDS = "email","role"


class UserProfile(models.Model):
        user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,related_name="profile")
        address = models.CharField(max_length=50)
        phone= models.CharField(null=True,max_length=20)
        profile_image = models.ImageField(upload_to='accounts/profile',null=True)

        def __str__(self):
            return self.user.email