
from django.dispatch import receiver
from .models import Blog,Blogimages
from django.db.models.signals import post_save, post_delete, pre_save
import os 

@receiver(post_delete, sender=Blogimages)
def auto_delete_image_on_delete(sender, instance, **kwargs):
    """
    Deletes file from filesystem
    when corresponding `MediaFile` object is deleted.
    """
    if instance.image:
        if os.path.isfile(instance.image.path):
            os.remove(instance.image.path)

@receiver(pre_save, sender=Blogimages)
def auto_delete_image_on_change(sender, instance, **kwargs):
    """
    Deletes old file from filesystem
    when corresponding `MediaFile` object is updated
    with new file.
    """
    if not instance.pk:
        return False

    try:
        old_file = Blogimages.objects.get(pk=instance.pk).image
    except Blogimages.DoesNotExist:
        return False

    new_file = instance.image
    if not old_file == new_file:
        if os.path.isfile(old_file.path):
            os.remove(old_file.path)


@receiver(post_delete, sender=Blog)
def auto_delete_image_on_delete(sender, instance, **kwargs):
    """
    Deletes file from filesystem
    when corresponding `MediaFile` object is deleted.
    """
    if instance.thumbnail:
        if os.path.isfile(instance.thumbnail.path):
            os.remove(instance.thumbnail.path)

@receiver(pre_save, sender=Blog)
def auto_delete_image_on_change(sender, instance, **kwargs):
    """
    Deletes old file from filesystem
    when corresponding `MediaFile` object is updated
    with new file.
    """
    if not instance.pk:
        return False

    try:
        old_file = Blog.objects.get(pk=instance.pk).thumbnail
    except Blog.DoesNotExist:
        return False

    new_file = instance.thumbnail 
    if not old_file == new_file:
        if os.path.isfile(old_file.path):
            os.remove(old_file.path)
