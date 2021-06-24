from django import forms

from customed_files.django.django_customed_classes.custom_BoundField import CustomBoundField




class CustomChoiceField(forms.ChoiceField):
    def get_bound_field(self, form, field_name):
        """
        Return a BoundField instance that will be used when accessing the form
        field in a template.
        """
        return CustomBoundField(form, self, field_name)

    
