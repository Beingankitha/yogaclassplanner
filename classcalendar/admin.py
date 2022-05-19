from django.contrib import admin
from .models import YogaClass, ClassMember

# Register your models here.

class YogaClassAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'start_time', 'end_time', 'attendee',)
    list_filter = ('title',"owner")
    
class ClassMemberAdmin(admin.ModelAdmin):
    list_display = ('id', 'yoga_class','student','sequence',)
    list_filter = ('yoga_class','student','sequence',)


admin.site.register(YogaClass,YogaClassAdmin)
admin.site.register(ClassMember, ClassMemberAdmin)
