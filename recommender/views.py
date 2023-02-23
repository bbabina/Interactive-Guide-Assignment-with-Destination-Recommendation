from django.shortcuts import render, HttpResponse
from django.contrib.auth.models import User
from ratinghome.models import Rateinfo
import pandas as pd
import seaborn as sns
from math import sqrt
import numpy as np
import matplotlib.pyplot as plt
from scipy import spatial
from registration.models import Preferences 
from destination.models import Mf_result, Place_rating
import random



def hybrid_recommender(thisuser):
    queryset = Rateinfo.objects.values_list("pID","pName","genre_bin","params")
    df_user = pd.DataFrame(list(queryset), columns=["pID","pName","genre_bin","profile"]) 
    df_user.set_index(['pID'], inplace=True )
    
    queryset = Place_rating.objects.filter(user=thisuser).values_list("user","place__rateinfo__pID","place__name","place__rateinfo__params", "rate")
    user_rating = pd.DataFrame(list(queryset), columns=["user","pID","pName","profile","rating"]) 
    user_rating = user_rating.dropna()
   
    user_rating.set_index('pID',inplace=True)



    if len(user_rating.index)==0:
        prset = Preferences.objects.filter(user = thisuser).values_list("user","culture","wildlife","adventure","sightseeing","history","religious","child_friendly")
  
        df_preference = pd.DataFrame(list(prset),columns=["user","culture","wildlife","adventure","sightseeing","history","religious","child_friendly"] )
    
        df_preference = df_preference.drop('user',1)
        df_preference = df_preference.astype(int)
        preference = df_preference.values.tolist()[0]
        def Similarity(preference, placeId):
        
            a= df_user.loc[placeId]
            
            
            genresA = a['genre_bin']
            checkzero = [0]*len(preference)
            if checkzero == preference:
                return 0
            else:
                genreDistance = spatial.distance.cosine(preference, genresA)
                return 1-genreDistance 
            
        sim = []
        for index, row in df_user.iterrows():
            sim.append(Similarity(preference,index))
        
        df_user['init']=sim
        sim.clear()
        df_user=df_user.sort_values("init", axis=0, ascending = False, kind='stable')
        initrec = df_user.head(15)
        recommendations = initrec.reset_index()
        initial_recommendation = recommendations['pID'].values.tolist()
        random.shuffle(initial_recommendation)
        return initial_recommendation 
    
    else:

        profile_split = pd.DataFrame(user_rating['profile'].tolist())

        pr_sum = profile_split.sum(axis=0)

        pr_average = pr_sum / len(user_rating.index)

        user_profile = pr_average

        user_rating['rating'] = user_rating['rating']-3

        ratings = user_rating['rating']


        func = lambda x: np.asarray(x) * np.asarray(ratings)

        profile_split = profile_split.apply(func)

        profile_split

        ratepr_sum = profile_split.sum(axis=0)

        ratepr_average = ratepr_sum / pr_sum

        ratepr_average = ratepr_average.fillna(0)

        user_profile = user_profile.tolist()

        user_rec = df_user.profile.apply(pd.Series)

        place_profiles = user_rec*ratepr_average

        pplist = place_profiles.values.tolist()

        place_profiles['weighted_profile']= pplist

        df_user = df_user.join(place_profiles['weighted_profile'], on='pID')

        n = len(user_rating.index)
        sq = sqrt(n)
        sq = round(sq)
        if sq%2==0:
            sq = sq+1
        k = sq

        def knn(placeid):
            a = df_user.loc[placeid]
        
            knn_set = user_rating.copy()
            wt_tmp = df_user['weighted_profile']
            knn_set = pd.merge(knn_set, wt_tmp, left_on="pID", right_on="pID", how="left")
            
            point_a = np.asarray(a['weighted_profile'])
            eucdist=[]
            for index, row in knn_set.iterrows():
                point_b = np.asarray(row["weighted_profile"])
                eucdist.append(np.linalg.norm(point_a - point_b))
                
            
            knn_set['euc_distance']=eucdist
            knn_set=knn_set.sort_values("euc_distance", axis=0, ascending = True, kind='stable')
            return knn_set.head(k)
            
                
            
            

        likeable = df_user[['pName','weighted_profile']].copy()

        for index, row in df_user.iterrows():
            positive = 0
            negative = 0
            mixed = knn(index)
            for i,j in mixed.iterrows():
                if j['rating']<0:
                    negative = negative + 1
                else:
                    positive = positive + 1
            if positive < negative:
                likeable = likeable.drop(index)
            
            
            

        def CosineDistanceAfterKnn(userprofile, placeId):
            
            a= likeable.loc[placeId]
            
            
            placeprofile = a['weighted_profile']
            checkzero = [0]*len(placeprofile)
            if checkzero == placeprofile :
                return 2
            else:
                genreDistance = spatial.distance.cosine(placeprofile,userprofile)
                return (genreDistance)

        profile_dist = []
        for index, row in likeable.iterrows():
            profile_dist.append(CosineDistanceAfterKnn(user_profile,index))

        likeable['profile_distance']=profile_dist
        profile_dist.clear()

        likeable=likeable.sort_values("profile_distance", axis=0, ascending = True, kind='stable')

        recommended = likeable[['pName','profile_distance']]

        a_index = recommended.index
        b_index = user_rating.index
        mask = ~a_index.isin(b_index)
        recommended = recommended.loc[mask]
        recommended = recommended.head(15)

        def CosineDistanceWithoutKnn(userprofile, placeId):
            
            a= df_user.loc[placeId]
            
            
            placeprofile = a['weighted_profile']
            checkzero = [0]*len(placeprofile)
            if checkzero == placeprofile :
                return 2
            else:
                genreDistance = spatial.distance.cosine(placeprofile,userprofile)
                return (genreDistance)

        if len(recommended.index)<5:
            profile_dist = []
            for index, row in df_user.iterrows():
                profile_dist.append(CosineDistanceWithoutKnn(user_profile,index))

            df_user['profile_distance']=profile_dist
            profile_dist.clear()
            df_user=df_user.sort_values("profile_distance", axis=0, ascending = True, kind='stable')
            recommended = df_user[['pName','profile_distance']]
            a_index = recommended.index
            b_index = user_rating.index
            mask = ~a_index.isin(b_index)
            recommended = recommended.loc[mask].head(30)
            recommendations = recommended.reset_index()
            contentbased_recommendation = recommendations['pID'].values.tolist()
            random.shuffle(contentbased_recommendation)
            return contentbased_recommendation
        else:
            recommendations = recommended.reset_index()
            contentbased_recommendation = recommendations['pID'].values.tolist()
            if(len(user_rating.index)>=20):
                collab = collaborative(thisuser)
                collabqueryset = Mf_result.objects.filter(user=thisuser,place__rateinfo__pID__in = collab)
                collabqueryset = sorted(collabqueryset, key=lambda x: collab.index(x.place.rateinfo.pID))
                top= []
                for i in collabqueryset:
                    if i.rate >=4:
                        for j in contentbased_recommendation:
                            if(i.place.rateinfo.pID==j):
                                top.append(j)
                all = contentbased_recommendation + collab

                def unique(seq):
                    seen = set()
                    seen_add = seen.add
                    return [x for x in seq if not (x in seen or seen_add(x))]
                all = unique(all)
                
                for i in all:
                    if i in top:
                        all.remove(i)

                other = all 
                other = random.sample(other,15)
                random.shuffle(top)
                both = [top,other]
            
                return both
            else:
                random.shuffle(contentbased_recommendation)
                return contentbased_recommendation
            #if len(user_rating.index)<50 or len(User.objects.all())<50:
                #return contentbased_recommendation

            #else: 
           
                


                
def collaborative(thisuser):
    queryset = Mf_result.objects.filter(user=thisuser).values_list("user","place__rateinfo__pID","place__name", "rate")
    user_result = pd.DataFrame(list(queryset), columns=["user","pID","pName","rating"]) 
    user_result = user_result.dropna()
    
    user_result.set_index('pID',inplace=True)

    user_result.sort_values("rating", axis=0, ascending = False, kind='stable', inplace=True)

    

    user_result = user_result[user_result['rating']>=3]

    queryset1 = Place_rating.objects.filter(user=thisuser).values_list("place__rateinfo__pID")
    user_rating = pd.DataFrame(list(queryset1), columns=["pID"]) 
    user_rating.set_index('pID',inplace=True)
    a_index = user_result.index
    b_index = user_rating.index
    mask = ~a_index.isin(b_index)
    user_result = user_result.loc[mask].head(15)
    

    

    user_result = user_result.reset_index()

    collab_result = user_result['pID'].values.tolist()



    return collab_result 





