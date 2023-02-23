from email.headerregistry import Address
from destination.models import Places
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Rateinfo 

@receiver(post_save, sender=Rateinfo)
def takevalue_pushtoplaces (sender, instance, created, **kwargs):
    if created:
        Places.objects.create(Rateinfo=instance,name= instance.pName, address= "province no. "+ str(instance.province))