from cmath import isnan
from dataclasses import field
from urllib.request import parse_keqv_list
from drf_writable_nested import WritableNestedModelSerializer
from rest_framework import serializers 
from apps.v1.services.models import ServiceTypeModel,ServiceRequestModel
from apps.v1.accounts.models import User
from django.forms.models import model_to_dict
from common.serializers import Base64ImageField

class ServiceTypeSerializer(serializers.ModelSerializer):
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        context = kwargs.get('context')
        if context:
            self.request = context.get('request')
    class Meta:
        model = ServiceTypeModel
        fields = ('pk','service_type_name','rate')

    def create(self,validate_data):
        package = ServiceTypeModel(**validate_data)
        package.studio = self.request.user
        package.save()
        return package

class ServiceRequestSerializer(serializers.ModelSerializer):
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        context = kwargs.get('context')
        if context:
            self.request = context.get('request')
    image = Base64ImageField(max_length=None,use_url = True,)
    class Meta:
        model = ServiceRequestModel
        fields = ('pk','service_type','receive_date','note','image','studio')

    def create(self,validate_data):
        package = ServiceRequestModel(**validate_data)
        package.request_user = self.request.user
        package.studio = validate_data.pop('studio')
        package.save()
        return package


class ActiveDeactiveServiceTypeSerializer(WritableNestedModelSerializer):
    class Meta:
        model = ServiceTypeModel
        fields = ()
    
    def update(self,instance,validated_data):
        if instance.in_effect:
            instance.in_effect = False
        else:
            instance.in_effect = True
        instance.save()
        return model_to_dict(instance)
class ReceivedServiceRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = ServiceRequestModel
        fields = ()
    def update(self, instance, validated_data):
        instance.print_status = '1'
        instance.save()
        return super().update(instance, validated_data)
class PrintedServiceRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = ServiceRequestModel
        fields = ()
    def update(self, instance, validated_data):
        instance.print_status = '2'
        instance.save()
        return super().update(instance, validated_data)
class CancelServiceRequestSerializer(serializers.ModelSerializer):
    cancel_reason = serializers.CharField(max_length= 1024)
    class Meta:
        model = ServiceRequestModel
        fields = ('cancel_reason',)
    def update(self, instance, validated_data):
        instance.print_status = '3'
        instance.cancel_reason = validated_data.pop('cancel_reason')
        instance.save()
        return super().update(instance, validated_data)