from django.contrib import admin
from django.urls import path
from pannel_7660 import views


urlpatterns = [
    path(r'config', views.main_page),
    path(r'MSIM', views.msim),
    path(r'SSIM', views.ssim),
    path(r'Linux_PC', views.mac),
    # path('test', views.test),
]
