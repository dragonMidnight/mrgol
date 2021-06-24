from django.db import models
from django.contrib.auth import authenticate
from django.utils.translation import gettext_lazy as _

from rest_framework import serializers
from rest_framework.exceptions import ErrorDetail, ValidationError, ErrorDetail

from users.models import User




from rest_framework.fields import empty, SkipField, set_value
from collections.abc import Mapping
from collections import OrderedDict
from django.core.exceptions import ValidationError as DjangoValidationError
from rest_framework.utils.serializer_helpers import BindingDict
from django.utils.functional import cached_property
from app1.models import Test3, Test4
from rest_framework.validators import UniqueValidator
from django.db.models.fields import Field as DjangoModelField

class Test3Serializer(serializers.ModelSerializer):    
    #field_1 = serializers.CharField(error_messages=translated_errors.errore_messages_rest_charfield, max_length=60, validators=[UniqueValidator(message = '%(model_name)s with this %(field_label)s already exists.', queryset=Test3.objects.all())])
    class Meta:
        model = Test3
        fields = '__all__'

class Test4Serializer(serializers.ModelSerializer):    
    #field_1 = serializers.CharField(error_messages=translated_errors.errore_messages_rest_charfield, max_length=60, validators=[UniqueValidator(message = '%(model_name)s with this %(field_label)s already exists.', queryset=Test3.objects.all())])
    #field_1 = serializers.IPAddressField(error_messages={'invalid': 'aaaaaaaaaaaa'})
    class Meta:
        model = Test4
        fields = '__all__'



        
class UserSerializer(serializers.ModelSerializer):    
    class Meta:
        model = User
        fields = '__all__'

    def is_valid(self, raise_exception=False):
        assert hasattr(self, 'initial_data'), (
            'Cannot call `.is_valid()` as no `data=` keyword argument was '
            'passed when instantiating the serializer instance.'
        )

        if not hasattr(self, '_validated_data'):
            try:
                self._validated_data = self.run_validation(self.initial_data)
            except ValidationError as exc:
                self._validated_data = {}
                self._errors = exc.detail

                
                errors_dic = exc.detail.copy()
                for field_name in exc.detail:
                    for i in range(len(exc.detail[field_name])):         
                        details_list = exc.detail[field_name].copy()          #exc.detail[field_name] is list and mutable with details, su we use .copy to stop changing exc.detail
                        details_list[i] = {exc.detail[field_name][i].code: exc.detail[field_name][i]}   #exc.detail[field_name][i] is object of ErrorDetail class
                    errors_dic[field_name] = details_list

                    
            else:
                self._errors = {}

        if self._errors and raise_exception:
            raise ValidationError(errors_dic)

        return not bool(self._errors)

#UserSerializer.serializer_field_mapping[models.EmailField] = serializerfields.EmailFieldCustom

 


    
class UserChangeSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        exclude  = ['password']
        



class UserNameSerializer(serializers.ModelSerializer):         #UserName = NAme of User for shown in site.
    user_shown_name = serializers.SerializerMethodField()
    class Meta:
        model = User
        fields = ['id', 'user_shown_name']
    def get_user_shown_name(self, obj):
        first_name, last_name = obj.first_name, obj.last_name
        if first_name and last_name:
            return f'{first_name} {last_name}'
        else:
            return obj.email
