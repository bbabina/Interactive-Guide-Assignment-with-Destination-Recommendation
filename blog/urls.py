from django.urls import path
from . import views

urlpatterns = [
    path('',views.bloglistview.as_view(), name='bloglist'),
    path('<int:pk>', views.blogdetailview.as_view(), name='blogview'),
    
]