"""djangobuhalteria URL Configuration

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

from django.urls import path
from django.conf.urls import include, url
from django.contrib import admin
from buhal import views
from django.contrib.auth import login, logout

urlpatterns = [
    path('admin/', admin.site.urls),
    # ex: /accounts/login/
    url(r'^accounts/login/$', login),
    # ex: /accounts/logout/
    url(r'^accounts/logout/$', logout),
    url(r'^buhalteriya/', include('buhal.urls')),
    #url(r'^admin/', include(admin.site.urls)),
    url(r'^login/', views.logins, name='logins'),
    url(r'^logout/', views.logouts, name='logouts'),
    url(r'^', views.wellcome, name='wellcome'),
]
