from django.db import models
from destination.models import Places
from django.contrib.auth.models import User
import datetime
import os 
# Create your models here.

def th_file_name(instance, filename):
    ext = filename.split('.')[-1]
    filename = "%s_%s.%s" % (instance.title, 'blogthumbnail', ext)
    return os.path.join('blogthumbnails', filename)


class Blog(models.Model):
    title=models.CharField(max_length=50, blank=False, null = False )
    author=models.ForeignKey( User , on_delete=models.CASCADE)
    description=models.TextField(blank= False, null=False)
    thumbnail=models.ImageField(upload_to=th_file_name , null=False )
    created_date=models.DateField(auto_now_add=True)
    related_place=models.ForeignKey(Places,on_delete=models.CASCADE)
    def __str__(self):
        return self.title
    class Meta:
        ordering=['-created_date']

def img_file_name(instance, filename):
    ext = filename.split('.')[-1]
    filename = "%s_%s.%s" % (instance.bg.title, 'blogimage', ext)
    return os.path.join('blogimages', filename)


class Blogimages(models.Model):
    bg=models.ForeignKey(Blog,on_delete=models.CASCADE)
    image=models.FileField(null=True,blank=True,upload_to=img_file_name)

    def __str__(self):
        return self.bg.title


 
