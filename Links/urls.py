from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('<str:short_code>', views.redirect_original, name='redirect_original'),
    path('stats/<str:short_code>', views.url_stats, name='url_stats'),
]