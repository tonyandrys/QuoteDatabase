from django.conf.urls import patterns, url
from quotedb import views

# URLConfs for the QDB UNCHAINED

urlpatterns = patterns('',
	url(r'^$', views.status, name='status'),
	url(r'^login/$', views.login_page, name='login_page'),
	url(r'^login/process_login/$', views.process_login, name='process_login'),
	url(r'^logout/$', views.logout_user, name='logout'),
	url(r'^register/$', views.register_page, name='register_page'),
	url(r'^register/process_registration/$', views.process_registration, name='process_registration'),
	url(r'^view/$', views.browse, name='browse'),
	url(r'^view/(?P<quote_id>\d+)/$', views.quote, name='quote'),
	url(r'^view/(?P<quote_id>\d+)/v/(?P<vote_tag>\d+)/$', views.vote, name='process_vote'),
	url(r'^view/(?P<quote_id>\d+)/add_comment/$', views.add_comment, name='add_comment'),
	url(r'^add_quote/$', views.new_quote_submit, name='new_quote_submit'),
	url(r'^add_quote/submit/$', views.add_quote, name='add_quote'),
	url(r'^user/(?P<user_id>\d+)/$', views.user, name='user'),
	url(r'^view/random/$', views.random, name='random'),
	url(r'^shop/$', views.shop, name='shop'),
	url(r'^admin/$', views.admin_panel, name='admin_panel'),
	url(r'^admin/ban_user/(?P<user_id>\d+)/$', views.ban_user, name='ban_user'),
	url(r'^admin/ip_ban/(?P<ip_address>\d+)/$', views.ip_ban, name='ip_ban'),
)
