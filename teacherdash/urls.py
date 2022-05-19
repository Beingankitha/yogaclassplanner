from django.contrib import admin
from django.urls import path
from .import views
	
urlpatterns = [
	path('teacher/dashboard',views.teacherdash,name="teacher/dashboard"),
	path('teacher/profile',views.teacherprofile,name="teacher/profile"),
	path('teacher/editprofile',views.edituserprofile,name="teacher/editprofile"),
	path('teacher/saveuserprofile',views.saveuserprofile, name="teacher/saveuserprofile"),
	path('teacher/profile',views.bypassurl,name="bypassurl"),
	path('teacher/yogadictionary',views.tyogadictionary, name="tyogadictionary"),
	path('teacher/yogadictionary/yoga_detail/<int:id>',views.yoga_detail, name="yoga_detail"),
	path('teacher/yogadictionary/addyogaasana',views.addyogaasana, name="teacher/yogadictionary/addyogaasana"),
	path('teacher/yogadictionary/edit/<int:id>',views.edit_data, name="edit_data"),
	path('teacher/yogadictionary/fav/<int:id>',views.fav_asan, name="fav_asan"),
	path('teacher/favourite',views.fav_asan_display, name="fav_asan_display"),
	path('teacher/yogadictionary/create/yogasequences',views.tyogasequences, name="tyogasequences"),
 
]

