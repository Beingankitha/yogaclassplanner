from django.contrib import admin
from django.urls import path,include
from .import views
	
urlpatterns = [
	path('',views.index,name="index"),
    path('userregister',views.userregister,name="userregister"),
    path('save_data',views.save_data,name="save_data"),
    path('userlogin',views.userlogin,name="userlogin"),
    path('login_check',views.login_check,name="login_check"),
    path('studentdash',views.studentdash,name="studentdash"),
    path('teacherdash',views.teacherdash,name="teacherdash"),    
    path('logout1',views.logout1,name="logout1"),
    path('membership',views.membership,name="membership"),
    path(r'^activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        views.activate, name='activate'),
]