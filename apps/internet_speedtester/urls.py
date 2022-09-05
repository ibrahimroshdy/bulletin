from django.urls import path

from . import views

urlpatterns = [

    # The home page
    path('latest_speedtest/', views.get_latest_speedtest, name='latest_speedtest'),
    path('latest_week_internet_speedtests/', views.get_lastest_week_internet_speedtests,
         name='latest_week_internet_speedtests'),
    path('latest_week_internet_speedtests_agg/', views.get_week_internet_speedtest_agg,
         name='latest_week_internet_speedtests_agg'),

]
