from django.contrib import admin
from django.urls import path
from .import views
	
urlpatterns = [
    path('teacher/calendar',views.calendar_view,name="calendar_view"),
    path('teachcer/calendar/classlist',views.classlist,name="classlist"),
    path('teachcer/calendar/allclasslist',views.allclasslist,name="classlist"),
    path('teacher/calendar/classview/<int:id>/',views.classeview,name="classeview"),
    path('teacher/calendar/classedit/<int:id>/',views.class_edit,name="class_edit"),
    path('teacher/calendar/classdelete/<int:id>/',views.classdelete,name="classdelete"),
    path('teacher/calendar/classattendee/<int:id>/',views.classattendee,name="classattendee"),
    path('teacher/calendar/classattendee/studentmedsinfo/<slug:id>',views.studentmedsinfo,name="studentmedsinfo"),
]