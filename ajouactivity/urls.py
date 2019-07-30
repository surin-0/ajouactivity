"""ajouactivity URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
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
from django.urls import path, include
import board.views
# from django.contrib.auth import views as auth_views # 잠시 주석처리 했습니다. 이 코드 주석하면 circular 에러 안나요

urlpatterns = [
    path('admin/', admin.site.urls),
    path('chat/', include('chat.urls')),
    path('', include('board.urls',namespace="board")),

]

''' 잠시 주석처리 했습니다.
    url(
        r'^acclogin/',
        auth_views.login,
        name='login',
        kwargs={
            'template_name': 'login.html'
        }
    ),
    url(
        r'^accounts/logout/',
        auth_views.logout,
        name='logout',
        kwargs={
            'next_page': settings.LOGIN_URL,
        }
    ),
'''
