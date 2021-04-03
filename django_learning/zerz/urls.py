"""zerz URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
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
from chat import views
from accounts.views import (
    login_view,
    register_view,
    logout_view,
    register_successfully,
    login_successfully,
)
urlpatterns = [
    path('login/',login_view),
    path('register/',register_view),
    path('logout/',logout_view),
    path('loginsuccessfully',login_successfully),
    path('registersuccessfully',register_successfully),
    path('create/view/',views.create_message_view),
    # path('create/view/',views.create_message_view_2),
    path('bad/',views.bad_view),
    path('home/',views.home_view),
    path('messages/<int:pk>/',views.search_message),
    path('message/<int:pk>/',views.details),
    path('messages/json/<int:pk>/',views.try_json_search),
    path('admin/', admin.site.urls),
    path('message/showall/',views.show_all_message),
    # path('notebook/',views.read_notebook),
]
