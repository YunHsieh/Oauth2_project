"""website URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
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
from django.conf.urls import url, include
from django.contrib.auth.models import User, Group

from users import views as ue_api
from rest_framework_swagger.views import get_swagger_view

schema_view = get_swagger_view(title='Potpourri')

urlpatterns = [
    url(r'admin/', admin.site.urls),
    url(r'^o/', include('oauth2_provider.urls', namespace='oauth2_provider')),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    url(r'^swagger_ui/$', schema_view),
]

urlpatterns += [
    url(r'^auth/$', ue_api.UserToken.as_view()),
    url(r'^user/$', ue_api.UserAccount.as_view()),
    url(r'^mgr/$', ue_api.AdminMgr.as_view()),
]
