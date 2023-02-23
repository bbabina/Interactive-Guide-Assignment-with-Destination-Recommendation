from django.db.models.signals import post_save, post_delete, pre_save
from django.dispatch import receiver
from .models import Destimages,Place_rating,Places,Comment,Hotel
import os

@receiver(post_save,sender=Places)
def create_hotel_objects(sender,instance,created,**kwargs):
    if created:
        Hotel.objects.create(nearby=instance)
def update_hotel(sender,instance,**kwargs):
    instance.hotel.save()    

@receiver(post_save,sender=Places)
def create_destimages(sender,instance,created,**kwargs):
    if created:
        Destimages.objects.create(place=instance, image= instance.thumbnail_image )
def update_images(sender,instance,**kwargs):
    instance.destimages.save()    


@receiver(post_delete, sender=Destimages)
def auto_delete_image_on_delete(sender, instance, **kwargs):
    """
    Deletes file from filesystem
    when corresponding `MediaFile` object is deleted.
    """
    if (instance.image.path.split('\\')[-1])=='thumbnail_default.jpg':
            return False
    if instance.image:
        if os.path.isfile(instance.image.path):
            os.remove(instance.image.path)

@receiver(pre_save, sender=Destimages)
def auto_delete_image_on_change(sender, instance, **kwargs):
    """
    Deletes old file from filesystem
    when corresponding `MediaFile` object is updated
    with new file.
    """
    if not instance.pk:
        return False

    try:
        old_file = Destimages.objects.get(pk=instance.pk).image
       
    except Destimages.DoesNotExist:
        return False
    
    if (old_file.path.split('\\')[-1])=='thumbnail_default.jpg':
        return False
    new_file = instance.image
    if not old_file == new_file:
        if os.path.isfile(old_file.path):
            os.remove(old_file.path)


@receiver(post_delete, sender=Places)
def auto_delete_image_on_delete(sender, instance, **kwargs):
    """
    Deletes file from filesystem
    when corresponding `MediaFile` object is deleted.
    """
    if (instance.thumbnail_image.path.split('\\')[-1])=='thumbnail_default.jpg':
            return False
    if instance.thumbnail_image:
        if os.path.isfile(instance.thumbnail_image.path):
            os.remove(instance.thumbnail_image.path)

@receiver(pre_save, sender=Places)
def auto_delete_image_on_change(sender, instance, **kwargs):
    """
    Deletes old file from filesystem
    when corresponding `MediaFile` object is updated
    with new file.
    """
    if not instance.pk:
        return False

    try:
        old_file = Places.objects.get(pk=instance.pk).thumbnail_image
       
    except Places.DoesNotExist:
        return False
    if (old_file.path.split('\\')[-1])=='thumbnail_default.jpg':
        return False
    new_file = instance.thumbnail_image 
    if not old_file == new_file:
        if os.path.isfile(old_file.path):
            os.remove(old_file.path)
