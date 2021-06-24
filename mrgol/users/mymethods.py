from django.contrib.auth import authenticate
from django.utils.translation import gettext_lazy as _

from rest_framework import serializers




def login_validate(request):
    email = request.data.get('email')
    password = request.data.get('password')
    if email and password:
        user = authenticate(request=request, email=email, password=password)          #The authenticate call simply returns None for is_active=False
        if not user:
            msg = _('Unable to log in with provided credentials.')
            raise serializers.ValidationError(msg, code='authorization')
        return user
            
    else:
        msg = _('Must include "email" and "password".')
        raise serializers.ValidationError(msg, code='authorization')

