from django.urls import path
from . import views

urlpatterns = [
    path('', views.login, name='login'),
    path('callback', views.callback, name='callback'),
    path('success', views.success, name='success'),
    path('logout', views.logout, name='logout'),
]