from django.db import models

# Create your models here.

class chatbox(models.Model):
    name=models.CharField(max_length=100,null=True,blank=True)
    address=models.CharField(max_length=30)
    descrption=models.TextField(default="")
    # thumbnail_image=models.ImageField(upload_to=content_file_name,default = 'thumbnail_default.jpg')
    # ispopular = models.BooleanField(default=False)
    # rateinfo = models.OneToOneField(Rateinfo, on_delete=models.CASCADE)