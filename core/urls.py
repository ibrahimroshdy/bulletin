"""bulletin URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
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
from django.urls import include, path  # add this

admin.site.site_header = "Bulletin Admin"
admin.site.site_title = "Bulletin Admin Portal"
admin.site.index_title = "Welcome to Bulletin Project Portal"

urlpatterns = [
    path('admin/', admin.site.urls),  # Django admin route
    path("", include("apps.authentication.urls")),  # Auth routes - login / register

    # ADD NEW Routes HERE

    # Leave `Home.Urls` as last the last line
    path("", include("apps.home.urls")),
    path("", include("apps.system.urls")),
    path("", include("apps.internet_speedtester.urls")),
    path("", include("apps.social.urls")),
]
