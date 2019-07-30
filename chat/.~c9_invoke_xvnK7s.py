# chat/urls.py
from django.urls import path
from .views import chat

urlpatterns = [
    url(r'^$', views.chat, name='chat'),
]