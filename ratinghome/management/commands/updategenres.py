
from django.core.management.base import BaseCommand
import pandas as pd
import numpy as np
from ratinghome.models import Rateinfo

class Command(BaseCommand):
    help= 'command to update genres and keywords'
    def add_arguments(self, parser):
        pass
    def handle(self, *args, **options):
        places = Rateinfo.objects.all()
        
        for place in places:
            genre_word=[]
            if(place.culture==True):
                genre_word += ['culture','cultural']
            if(place.wildlife==True):
                genre_word += ['wildlife','animals']
            if(place.adventure==True):
                genre_word += ['adventure','adventurous']
            if(place.sightseeing==True):
                genre_word += ['beautiful','natural beauty']
            if(place.history==True):
                genre_word += ['historical','history']
            if(place.child_friendly == True):
                genre_word += ['children', 'child','child friendly']
            if(place.religious == True):
                genre_word += ['religious','religion','spiritual']
            if('datingspot' in place.tags):
                genre_word += ['romantic']
            place.genres = genre_word
            place.save()
        
            