from django.contrib import admin
from apps.v1.services.models import ServiceRequestModel,ServiceTypeModel
# Register your models here.
admin.site.register(ServiceTypeModel)
admin.site.register(ServiceRequestModel)
