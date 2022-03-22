from cmath import isnan
from urllib.request import parse_keqv_list
from drf_writable_nested import WritableNestedModelSerializer
from rest_framework import serializers 
from apps.v1.package.models import PackageModel
from django.forms.models import model_to_dict
from common.serializers import Base64ImageField

class PackageSerializers(serializers.ModelSerializer):

    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        context = kwargs.get('context')
        if context:
            self.request = context.get('request')
    package_image = Base64ImageField(max_length=None,use_url = True,)
    class Meta:
        model = PackageModel
        fields = ('pk','in_effect','package_name','package_image','package_price','package_disc')

    def create(self,validate_data):
        package = PackageModel(**validate_data)
        package.studio = self.request.user
        package.save()
        return package

class ActiveDeactivePackageSerializer(WritableNestedModelSerializer):
    class Meta:
        model = PackageModel
        fields = ()
    
    def update(self,instance,validated_data):
        print(instance)
        if instance.in_effect:
            instance.in_effect = False
        else:
            instance.in_effect = True
        instance.save()
        return model_to_dict(instance)