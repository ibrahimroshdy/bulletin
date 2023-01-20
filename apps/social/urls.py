from django.urls import path

from . import views

urlpatterns = [
    path('twt_get_trends/', views.twt_get_trends, name='twt_get_trends'),
    path('twt_get_tweeting_status/', views.twt_get_tweeting_status, name='twt_get_tweeting_status'),
]
