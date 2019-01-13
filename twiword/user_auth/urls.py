from django.contrib.auth.views import LoginView
from django.contrib.auth.views import LogoutView
from django.urls import path, include
from . import views
app_name='user_auth'

urlpatterns=[
    path('top/', views.top_page, name="top"),
    path('login/',
            LoginView.as_view(template_name='user_auth/login.html'),
            name='login'),
    path('logout/',
            LogoutView.as_view(template_name='user_auth/logout.html'),
            name='logout'),
]