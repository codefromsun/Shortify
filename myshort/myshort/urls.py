"""
URL configuration for myshort project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
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
from . import views


urlpatterns = [
    path('admin/', admin.site.urls),
    path('guest/',views.Gindex, name='Gindex'),
    path('',views.home, name='home'),

    path('signup/', views.signup, name='signup'),
    path('register/', views.register, name='register'),
    
    path('login/', views.login_page, name='login'),
    path('auth/', views.auth_user, name='auth'),
    
    path('dashboard/', views.dashboard, name='dashboard'),
    path('main/', views.main, name='main'),
    path('shorten/', views.shorten, name='shorten'),
    path('logout/', views.logout_user, name='logout'),
    path('Gshorten/', views.Gshorten, name='Gshorten'),
    path('delete/<str:shortcode>/', views.delete_link, name='delete_link'),
    path('<str:shortcode>/', views.rd, name='rd'),

]
