from pyexpat import model
from django.contrib import admin
from .models import WebsiteUser, MedicalInformation

class MedicalInformationAdmin(admin.StackedInline):
    model = MedicalInformation
    
class MedicalInformationShowAdmin(admin.StackedInline):
    list_display = ('user_email.fullname', 'user_email')
    
class WebsiteUserAdmin(admin.ModelAdmin):
    inlines = [MedicalInformationAdmin]
    list_display = ('fullname', 'email', 'is_active')
    list_filter = ("registered_as","is_health")
    
    class Meta:
        model = WebsiteUser

admin.site.register(MedicalInformation)
admin.site.register(WebsiteUser, WebsiteUserAdmin)
