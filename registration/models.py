from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from destination.models import Places

import os

class Preferences(models.Model):
    
    culture=models.BooleanField(default=False)
    wildlife=models.BooleanField(default=False)
    adventure=models.BooleanField(default=False)
    sightseeing=models.BooleanField(default=False)
    history=models.BooleanField(default=False)
    religious = models.BooleanField(default=False)
    child_friendly = models.BooleanField(default=False)
    user=models.OneToOneField(User,on_delete=models.CASCADE)
    

    def __str__(self):
        return self.user.username

def content_file_name(instance, filename):
        ext = filename.split('.')[-1]
        filename = "%s_%s.%s" % (instance.user.username, 'profilepic', ext)
        return os.path.join('profileimages', filename)

class Profile(models.Model):
    middle_name= models.CharField(max_length=20,null=True,blank=True)
    sex=models.CharField(max_length=10,choices=[('MALE','MALE'),('FEMALE','FEMALE')])
    age=models.IntegerField(null=False,blank=False)
    phone_number=models.CharField(max_length=15, blank=False, null = False)
    nationality=models.CharField(max_length=20,null=False,blank=False)
    user= models.OneToOneField(User,on_delete=models.CASCADE)
    profile_pic=models.ImageField(default = 'defaultpp.jpg', upload_to=content_file_name)
    place = models.ForeignKey(Places, on_delete=models.CASCADE, null=True, blank=True)
    is_guide=models.BooleanField(default=False)
    
    def __str__(self):
        return self.user.username
    
    