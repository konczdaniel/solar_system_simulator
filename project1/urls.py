"""
URL configuration for project1 project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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
from django.urls import path
from api import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('solar/', views.homePage),
    path("get-update/", views.loadUpdate, name="get_slider_value"),
    path('gridStatus/', views.saveGridValue, name="gridStatus"),
    path('grid-update/', views.gridUpdate, name= "grid-update"),
    path('save-load/', views.saveLoadValue, name="load_status"),
    path('save-solar', views.saveSolarValue, name="save-solar"),
    path('update-solar', views.solarUpdate, name="update-solar"),
    path("battery-charge", views.calculateSolarOutput, name="battery-charge"),
    path("register/", views.registerPage, name="register"),
    path("update-config", views.updateProduct, name="update_config"),
    path("login/", views.loginPage, name="login"),
    path('logout/', views.logoutUser, name='logout'),
]
