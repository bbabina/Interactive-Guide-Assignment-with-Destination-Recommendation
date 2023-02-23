from django.db import models

# Create your models here.
class Rateinfo(models.Model):
    pID=models.IntegerField()
    pName=models.CharField(max_length=100)
    
    culture=models.BooleanField(default=False)
    adventure =models.BooleanField(default=False)
    wildlife =models.BooleanField(default=False)
    sightseeing=models.BooleanField(default=False)
    history=models.BooleanField(default=False)
    religious = models.BooleanField(default=False)
    child_friendly = models.BooleanField(default=False)
    tags=models.JSONField()
    province_choices=[(1,1),(2,2),(3,3),(4,4),(5,5),(6,6),(7,7)]
    province=models.IntegerField(choices=province_choices)
    genre_bin = models.JSONField()
    words_bin = models.JSONField()
    params = models.JSONField()
    genres =models.JSONField()
    def __str__(self):
        return self.pName
    class meta:
        ordering=['-pID']
        




