"""eatplants URL Configuration

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
from django.contrib import admin
from django.urls import path

from accounts.views import (
    login_view,
    logout_view,
    register_view,
    profile_view,
)

from search.views import search_view
from .views import home_view, whyvegan_view

#the order matters for URLS
urlpatterns = [
    path('', home_view), # index / home / root
    path('articles/', article_search_view),
    path('articles/create/', article_create_view, name='article-create'),
    path('articles/<slug:slug>/', article_detail_view, name='article-detail'),
    path('admin/', admin.site.urls),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('pantry/recipes/', include('recipes.urls')),
    # path('profile/', profile_view, name='profile'),
    path('register/', register_view, name='register'),
    path('search/', search_view, name='search'),
    path('profile/', include('users.urls')),
    path('whyvegan/', whyvegan_view, name='whyvegan')
    
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

    # path('articles/', article_search_view, name='articles'),
    # path('articles/create/', article_create_view, name='article-create'),
    # path('articles/<slug:slug>/', article_detail_view, name='article-detail'),
