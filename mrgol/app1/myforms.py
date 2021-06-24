from django import forms
from django.conf import settings
from django.contrib.admin.widgets import AdminTextInputWidget

import json

from . import myserializers
from .mywidgets import filter_attributes_widget, root_widget
from .models import Product, Filter, Filter_Attribute, Rating, Root
from .myfields import CustomChoiceField




class ProductForm(forms.ModelForm):
    filter_attributes = CustomChoiceField(choices=(), widget=filter_attributes_widget, required=True, label='آيتم هاي فيلتر' if settings.ERROR_LANGUAGE=='pr' else 'Filter Attributes')
    #root = CustomChoiceField(choices=(), widget=root_widget, required=True, label='ريشه' if settings.ERROR_LANGUAGE=='pr' else 'root')
    class Meta:
        model = Product
        fields = '__all__'

class C(forms.CharField):
    def clean(self, value):
        pass

from django.core import validators
class RatingForm(forms.ModelForm):
    slug = C()
    class Meta:
        model = Root
        fields = '__all__'

    def clean_slug(self):
        pass
