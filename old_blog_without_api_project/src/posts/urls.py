from django.conf.urls import url
from django.contrib import admin

from .views import (
	post_list,
	post_create,
	post_detail,
	post_update,
	post_delete,
	PostDetailView
	)

urlpatterns = [
	url(r'^$', post_list, name='list'),     #default view when loclhost:127.0.0.1:port/posts/ is opened ,then this view will be opened
    url(r'^create/$', post_create),  #post_create function must be opened of this app


    #url(r'^details/$', post_details),
    #url(r'^list/$', post_list),
    #url(r'^update/$', post_update),



    #dynamic routing an url patterns ==>> see below urls with regex
    #url(r'^(?P<slug>[\w-]+)/$', post_detail, name='detail'),
    url(r'^(?P<slug>[\w-]+)/$', PostDetailView.as_view(), name='detail'),# ==>> name is used so that in template(html) (see post_list.html for more info) link is not harcoded .
    url(r'^(?P<slug>[\w-]+)/edit/$', post_update, name='update'),
    url(r'^(?P<slug>[\w-]+)/delete/$', post_delete),
    #url(r'^posts/$', "<appname>.views.<function_name>"),
]
