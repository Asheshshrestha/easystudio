from django.db import models
from apps.v1.accounts.models import User,UserProfile
from django.conf import settings
from django.db.models import Avg
from django.core.validators import MinValueValidator, MaxValueValidator
# Create your models here.


class StudioRating(models.Model):
    studio = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.SET_NULL, null=True)
    rated_user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL,null=True,related_name="rater")
    stars = models.IntegerField(null=True,blank=True,validators=[MinValueValidator(0),MaxValueValidator(5)])

class StudioProfile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,related_name="studio_profile")
    studio_name = models.CharField(max_length=255)
    longitude = models.CharField(max_length=100)
    latitude = models.CharField(max_length=100)
    marker_icon = models.ImageField(upload_to='studio/marker',null=True)
    address = models.CharField(max_length=50)
    phone= models.CharField(null=True,max_length=20)
    profile_image = models.ImageField(upload_to='studio/profile',null=True)
    cover_image = models.ImageField(upload_to='studio/cover',null= True)


    def __str__(self):
        return self.studio_name
    @property
    def get_cover_image(self):
        if self.cover_image and hasattr(self.cover_image,'url'):
            return self.cover_image.url
    @property
    def get_profile_image(self):
        if self.profile_image and hasattr(self.profile_image,'url'):
            return self.profile_image.url
    @property
    def get_marker_icon(self):
        if self.marker_icon and hasattr(self.marker_icon,'url'):
            return self.marker_icon.url
    @property
    def average_rating(self):
        rating = StudioRating.objects.filter(studio = self.user)
        avg_rating = rating.aggregate(Avg('stars'))
        return avg_rating

