from django.urls import path, re_path
from  . import views
from . import consumers

urlpatterns = [

    # The home page
    path('platform_specs/', views.platform_specs, name='platform_specs'),
    path('machine_uptime/', views.machine_uptime, name='machine_uptime'),
    # path('machine_uptime/', consumers.UptimeConsumer, name='machine_uptime'),

]
