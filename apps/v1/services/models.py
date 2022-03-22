from django.db import models
from django.conf import settings
# Create your models here.

class ServiceTypeModel(models.Model):

    service_type_name = models.CharField(max_length=255)
    studio = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.SET_NULL, null=True)
    rate = models.CharField(max_length=100,null=True)
    in_effect = models.BooleanField(default=True)
    def __str__(self):
        return self.service_type_name


class ServiceRequestModel(models.Model):

    PRINT_STATUS = (("0","Pending"),("1","Received"),("2","Printed"),("3","Cancelled"))
    request_user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL,null=True,related_name="client")
    studio = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.SET_NULL, null=True, related_name='studio')
    service_type = models.ForeignKey(ServiceTypeModel,on_delete=models.SET_NULL, null=True)
    receive_date = models.DateField(null=True)
    note = models.TextField(max_length=2024,null=True)
    image = models.ImageField(upload_to='studio/requests',null=True)
    print_status = models.CharField(max_length=1, choices= PRINT_STATUS,default="0")
    cancel_reason = models.CharField(max_length=1024,null=True)