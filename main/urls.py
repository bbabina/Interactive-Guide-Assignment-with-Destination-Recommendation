from django.urls import path
from django.urls import include
from . import views

from registration.views import profile_editpage 

urlpatterns = [
     path('contactUs', views.contactusview, name="contactus"),
     path('', views.mainpageview, name="mainpage"),
     path('blogs/', include('blog.urls')),

     path('', include('destination.urls')),
path('profile/', views.profilepage, name='profilepage'),
path('aboutUs/',views.aboutus,name='aboutus'),
path('map/',views.maps,name='maps'),
path('profile/user_profile_edit/', profile_editpage ,name='edit_profile'),
path('places/', views.Searchplace.as_view() ,name='places'),

# path("Login_guide/", views.guideLogin, name='guideLogin'),
# path("Register_guide/", views.guideRegister, name='guideRegister'),

path('chatbox/', include('chatbox.urls')),

]
