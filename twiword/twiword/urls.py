from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('admin/', admin.site.urls),
    path('collect_words/', include('collect_words.urls', namespace='collect')),
]
