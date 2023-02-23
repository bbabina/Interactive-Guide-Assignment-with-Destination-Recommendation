from django.urls import path
from . import views
from blog.views import add_blogview
from destination.views import Rateview

urlpatterns = [
    path('',views.placelistview.as_view(), name='placelist'),
    path('<int:pk>/', views.placedetailview, name='placeview'),
    path('addblog/<int:p_id>/',add_blogview,name='blogadd'),
    path('rate/<int:r_id>/',Rateview,name='rate-place'),
   # path('celery/', test , name='celery'),
    
]