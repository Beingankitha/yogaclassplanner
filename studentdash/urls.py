from django.contrib import admin
from django.urls import path
from .import views
	
urlpatterns = [
    path('studentdash',views.studentdash,name="studentdash"),
    path('studentprofile',views.studentprofile,name="studentprofile"),
    path('editprofile',views.editprofile,name="editprofile"),
    path('studentprofile',views.bypass,name="bypass"),
    path('save_profile',views.save_profile,name="save_profile"),
    path('studenthealth',views.studenthealth,name="studenthealth"),
    path('addpaymentinfo',views.addpaymentinfo,name="addpaymentinfo"),
    path('resetpwd',views.resetpwd,name="resetpwd"),
    path('deleteacc',views.deleteacc,name="deleteacc"),
    path('yogadictionary/',views.yogadictionary,name="yogadictionary"),
    path('search/',views.search,name="search"),
    path('studentclasses',views.studentclasses,name="studentclasses"),
    path('studentbookclass',views.studentbookclass,name="studentbookclass"),
    path('studentbookclass/class_detail/<int:id>',views.class_detail,name="class_detail"),
    path('classbooked/<int:id>/',views.classbooked,name="classbooked"),
    path('classbooked/delete/<int:id>/',views.classbookeddeleted,name="classbookeddeleted"),
    path('yogadictionary/<int:id>/',views.yogaasan_detail, name="yogaasan_detail"),
]