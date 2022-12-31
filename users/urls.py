from django.urls import path
from .views import (
    login_view,
    logout_view,
    register_view,
    profile_view,
)

# the order matters for URLS

app_name = 'users'
urlpatterns = [
    # path('', profile_view, name='profile'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('register/', register_view, name='register'),
]