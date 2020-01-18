from django.urls import path, re_path
from . import views
from django.conf.urls import url

urlpatterns = [
    path('', views.index, name="index_page" ),
    path("faq/", views.faq, name="faq_page") ,   
    path("about/", views.about, name="about_page") , 
    path("terms_n_conditions/", views.terms_n_conditions, name="terms_n_conditions_page"),
    path("winner/", views.WinnersListView.as_view(), name="winner_page"),
    path("livebid/", views.LivebidListView.as_view(), name="livebid_page"),
    path("selection/<int:p_id>", views.selection_get, name="selection_page"),
    path(r'selection/(?P<data>\w+)/$', views.redirect_view_to_selection, name="redirect_view_to_selection"),
    path("buybid/", views.buybid, name="buybid_page"),
    path(r'(?P<status>\w+)/$', views.redirect_view_to_buyBid, name='redirect_view_to_buyBid'),
    
    path('paytm/payment/<int:amount>', views.payment, name='payment_page'),
    re_path(r'paytm/response/(?P<user_id>\w+)/$', views.response, name='response_page'),
    re_path(r'paytm/response/(?P<user_id>([A-Za-z0-9._@+-])+@gmail\.com)/$', views.response, name='response_page'),

    path("registration/signup_page/", views.signup_page, name='signup_page'),
    url(r'^activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$', views.activate, name='activate'),
]
