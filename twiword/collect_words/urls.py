from django.urls import path
from . import views
app_name = 'collect'
#1の人しか入れないよおおおおお
urlpatterns = [
    path('1/', views.userhome, name='userhome'),
    path('1/quiz/', views.quiz, name='quiz'),
    path('1/list', views.wordlist, name='list'),
    path('1/result', views.result, name='result'),
    path('', views.index, name='index'),
]