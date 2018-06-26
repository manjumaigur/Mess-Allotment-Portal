from django.conf.urls import url
from . import views

app_name = 'mess'

urlpatterns = [
	url(r'^$', views.MessIndex.as_view(), name='index'),
	url(r'^(?P<pk>\d+)/$', views.mess_detail, name='mess_detail'),
	url(r'^create/$', views.mess_create, name='mess_create'),
	url(r'^edit/(?P<pk>\d+)/$', views.mess_edit, name='mess_edit'),
	url(r'^members/(?P<pk>\d+)/$', views.mess_members, name='mess_members'),
	url(r'^choose/$', views.mess_choose, name='mess_choose'),
	url(r'^allot/(?P<pk>\d+)/$', views.mess_allot, name='mess_allot'),
	url(r'^card/$', views.mess_card, name='mess_card'),
	url(r'^pay-fees/$', views.pay_fees, name='pay_fees'),
	url(r'^edit-fees/(?P<pk>\d+)/$', views.edit_fees, name='edit_fees'),
	url(r'^fee-details/(?P<pk>\d+)/$', views.fee_details, name='fee_details'),
	url(r'^fee-verify/(?P<pk>\d+)/$', views.fee_verify, name='fee_verify'),
	url(r'^fee-reject/(?P<pk>\d+)/$', views.fee_reject, name='fee_reject'),
]