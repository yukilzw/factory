"""Test URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from .modules import view,mock

viewPath = [
    url(r'^pipe', view.pipe),
    url(r'^home$', view.home),
    url(r'^vue-app', view.vueDemo),
    url(r'^wxToken$', view.wxToken),
    url(r'^wx_JSSDK_check$', view.wx_JSSDK_check),
    url(r'^wxOpenId$', view.wxOpenId),
    url(r'^wxMsgPush$',view.wxMsgPush),
    url(r'^savePhotoImg$', view.savePhotoImg),
    url(r'^binaryPipe$', view.binaryPipe),
    url(r'favicon.ico',view.is404 )
]

mockPath = [
    url(r'^H5/Outdoorsrank', mock.activityConfig)
]

urlpatterns = viewPath + mockPath
