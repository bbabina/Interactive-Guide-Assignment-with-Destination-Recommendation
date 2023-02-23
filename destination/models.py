
from django.urls import reverse 
from django.db import models
import datetime
from django.contrib.auth.models import User
from ratinghome.models import Rateinfo 
from django.utils import timezone
import os

def content_file_name(instance, filename):
    ext = filename.split('.')[-1]
    filename = "%s_%s.%s" % (instance.name, 'thumbnail', ext)
    return os.path.join('thumbnails', filename)

# Create your models here.
class Places(models.Model):
    name=models.CharField(max_length=100,null=True,blank=True)
    address=models.CharField(max_length=30)
    descrption=models.TextField(default="")
    thumbnail_image=models.ImageField(upload_to=content_file_name,default = 'thumbnail_default.jpg')
    ispopular = models.BooleanField(default=False)
    rateinfo = models.OneToOneField(Rateinfo, on_delete=models.CASCADE)
    def get_absolute_url(self):      
        return reverse('placeview', args=[str(self.id)])
    def __str__(self):
        return self.name
    
class Place_rating(models.Model):
    rate=models.PositiveSmallIntegerField(choices=[(1,1),(2,2),(3,3),(4,4),(5,5)],default=0) 
    place=models.ForeignKey(Places,on_delete=models.CASCADE)
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    def __str__(self):
        return "%s-%s" % (self.user.username,self.place.name)


class Comment(models.Model):
    place=models.ForeignKey(Places,on_delete=models.CASCADE)
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    comment_body= models.TextField()
    created_date=models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering=['-created_date']
    
    def __str__(self):
        return '%s -  %s' %(self.place.name,self.user.username)

def img_file_name(instance, filename):
    ext = filename.split('.')[-1]
    filename = "%s_%s.%s" % (instance.place.name, 'image', ext)
    return os.path.join('thumbnails', filename)


class Destimages(models.Model):
    place=models.ForeignKey(Places,on_delete=models.CASCADE)
    image=models.ImageField(upload_to=img_file_name )

    def __str__(self):
        return self.place.name



class Hotel(models.Model):
    title=models.CharField(max_length=20)
    contact_info=models.CharField(max_length=15)
    nearby=models.ForeignKey(Places,on_delete=models.CASCADE)

    def __str__(self):
        return self.nearby.name



class Mf_result(models.Model):
    rate=models.FloatField() 
    place=models.ForeignKey(Places,on_delete=models.CASCADE)
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    def __str__(self):
        return "%s-%s" % (self.user.username,self.place.name)
   




        





