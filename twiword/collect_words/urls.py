from django.urls import path
from . import views
app_name = 'collect'
#1の人しか入れないよおおおおお
urlpatterns = [
    path('<int:userurl>/', views.userhome, name='userhome'),
    path('<int:userurl>/quiz', views.quiz, name='quiz'),
    path('<int:userurl>/list', views.wordlist, name='list'),
    path('<int:userurl>/result', views.result, name='result'),
    path('top/', views.top_page, name='top'),
]