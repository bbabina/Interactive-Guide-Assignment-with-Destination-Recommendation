"""ourproject URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from atexit import register
from xml.dom.minidom import Document
from django.contrib import admin
from django.urls import path,include
from login.views import loginpage,logoutpage
from registration.views import registerpage,accountsetting

from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('075bct/', admin.site.urls),
    path('',loginpage,name='login'),
    path('registerpage/', registerpage,name="registerpage"),
    path('ac/',accountsetting,name='as'),
   ## path('',include('home.urls')),
    path('mainpage/',include('main.urls')),
       
    
]
urlpatterns += static(settings.MEDIA_URL,document_root = settings.MEDIA_ROOT)
