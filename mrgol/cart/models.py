from users.models import User
from django.db import models
from django.db.models.signals import post_save
from django.contrib.sessions.backends.db import SessionStore

class SesKey(models.Model):
    user = models.ForeignKey(User, on_delete = models.CASCADE, blank=True, null=True)
    ses_key = models.CharField(max_length=60, default='', blank=True)



def save_seskey(sender, **kwargs):
    if kwargs['created']:                                                       #may one family create 5 account but just one of them use, so we dont create session and assign ses_key here.
        cartsession = SessionStore()                                            #we create session here becase: main optimizing done for carts(creating/or not creating session  is not so important for optimizing specialy for shoping websites that user willl use its cart 99.9%), we want all projects be same structue as possible (this is more important)
        cartsession.create()
        save_seskey = SesKey.objects.create(user=kwargs['instance'], ses_key=cartsession.session_key)      

post_save.connect(save_seskey, sender=User)


