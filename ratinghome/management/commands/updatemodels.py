from django.core.management.base import BaseCommand
import pandas as pd
import numpy as np
from ratinghome.models import Rateinfo


class Command(BaseCommand):
    help= 'command to update rateinfo table'
    def add_arguments(self, parser):
        pass
    def handle(self, *args, **options):
        df= pd.read_csv('New_dataset.csv')
        df = df.dropna()
        df[['pID','culture','adventure','sightseeing','history','religious','child_friendly']] = df[['pID','culture','adventure','sightseeing','history','religious','child_friendly']].astype(int)
        df["tags"]=df["tags"].values.astype(str)
        genre_df = df[['culture', 'adventure', 'wildlife', 'sightseeing', 'history', 'religious','child_friendly']]

        genrelist = genre_df.values.tolist()

        df['genre_bin']= genrelist

        df['tags'] = df['tags'].str.strip().str.replace(' ','')
        df['tags'] = df['tags'].str.lower().str.split(',')
        wordList = []
        for index, row in df.iterrows():
            words = row["tags"]
            
            for word in words:
                if word not in wordList:
                    wordList.append(word)
        def binary(word_list):
            binaryList = []
            
            for word in wordList:
                if word in word_list:
                    binaryList.append(1)
                else:
                    binaryList.append(0)
            
            return binaryList   
        df['words_bin'] = df['tags'].apply(lambda x: binary(x))  
        df['params']=df['genre_bin']+df['words_bin']


        for pid,pname,culture,adventure,wildlife,sightseeing,history,religious,child_friendly,tag,province,genre_bin,words_bin,params in zip(df.pID,df.pName,df.culture,df.adventure,df.wildlife,df.sightseeing,df.history,df.religious,df.child_friendly,df.tags,df.province,df.genre_bin,df.words_bin,df.params):
            models=Rateinfo(pID=pid,pName=pname,culture=culture,adventure=adventure,wildlife=wildlife,sightseeing=sightseeing,history=history,religious=religious,child_friendly=child_friendly,tags=tag,province=province,genre_bin=genre_bin, words_bin=words_bin, params=params)
            models.save()



