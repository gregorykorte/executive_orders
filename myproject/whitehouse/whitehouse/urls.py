"""myproject URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
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
from django.contrib import admin
from whitehouse import views

urlpatterns = [
    url(r'^(?i)admin/', admin.site.urls),
    url(r'^(?i)$', views.OrderListView.as_view(), name = 'order_list'),
    url(r'^(?i)orders/$', views.OrderListView.as_view(), name = 'order_list'),
    url(r'^(?P<pk>[0-9]+)/$', views.OrderDetailView.as_view(), name='order_detail'),
    url(r'^([-\w\d]+)/$', views.OrderPresidentView.as_view(), name = 'order_list'), #need to add filters
    url(r'^(?P<short_type>[-\w\d]+)/$', views.OrderTypeView.as_view(), name = 'order_list'), #need to add filters  
]
