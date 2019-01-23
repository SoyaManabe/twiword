from django.contrib import admin
from django.urls import include, path



urlpatterns = [
    path('admin/', admin.site.urls),
    path('collect_words/', include('collect_words.urls', namespace='collect')),
    path('user/', include('user_auth.urls')),
    path('user/', include('social_django.urls', namespace='social')),
]
