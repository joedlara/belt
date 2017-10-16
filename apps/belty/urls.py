from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index),
    url(r'^register$', views.register),
	url(r'^welcome$', views.success),
	url(r'^login$', views.login),
	url(r'^logout$', views.logout),
	url(r'^add$', views.add),
	url(r'^users/(?P<quote_id>\d+)$', views.dashboard),
	url(r'^home$', views.home),
	url(r'^welcome/(?P<fav_id>\d+)/remove_fav$', views.remove_fav),
	url(r'^welcome/(?P<quote_id>\d+)/remove$', views.remove_quote),
	url(r'^welcome/(?P<quote_id>\d+)/favorite$', views.fav_quote),
	
]