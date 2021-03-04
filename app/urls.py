"""app URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
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
from django.contrib import admin
from django.urls import path, include
from core import views
from rest_framework.authtoken.views import obtain_auth_token
from rest_framework import routers
from core.views import MrConfig

#router = routers.DefaultRouter()
#router.register('mrconfig', MrconfigViewSet, basename='MrConfig')
#router.register('medicoes', MedicoesViewSet, basename='Medicoes')

urlpatterns = [
    path('admin/', admin.site.urls),
    #path('', include(router.urls)),
    path('api/user/', include('user.urls')),
    path('api/mrconfig', views.MrConfig.as_view(), name='mrconfig')
]
