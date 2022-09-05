from django.urls import path, re_path
from apps.home import views

urlpatterns = [

    # The home page
    path('', views.index, name='home'),

    # TODO: fix html matching
    # Matches any html file
    re_path(r'^login-*.*\.*', views.pages, name='pages'),
    re_path(r'^page-*.*\.*', views.pages, name='pages'),
    re_path(r'^ui-*.*\.*', views.pages, name='pages'),
    re_path(r'^register*.*\.*', views.pages, name='pages'),

]
