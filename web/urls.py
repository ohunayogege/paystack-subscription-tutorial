from django.conf.urls import url
from . import views
from .views import Register, Login

urlpatterns = [
	url(r'^$', views.home, name='index'),
	url(r'^login/$', views.signin, name='login'),
	url(r'^home/$', views.index, name='home'),
    url(r'^check-mail-ajax/$', views.check_mail_ajax, name='check_mail_ajax'),
    url(r'^register/$', Register.as_view(), name='register'),
    url(r'login-req', Login.as_view(), name='login_ajax'),

    url(r'^subscription/', views.subscription, name='subscription'),
    url(r'^subscribe/', views.subscribe, name='subscribe'),
    url(r'^subscribed/', views.subscribed, name='subscribed'),
    url(r'^sub/', views.end_sub, name='sub'),

    url(r'^payment/$', views.call_back_url, name='payment'),
]