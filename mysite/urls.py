from django.contrib import admin
from django.urls import path
from .views import author,interests,title
urlpatterns = [
    path('admin/', admin.site.urls),
    path('author/',author),
    path('interests/',interests),
    path('title/',title),
]
