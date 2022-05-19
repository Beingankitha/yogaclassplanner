from django.contrib import admin
from .models import Asana, YogaAsanaSequence,YogaImage, YogaPosition, YogaType, YogaDificulty, favouriteAsana

class YogaImageAdmin(admin.StackedInline):
    model = YogaImage
    
# class AsanaImagesAdmin(admin.StackedInline):
#     model = AsanaImages

class favouriteAsanaAdmin(admin.ModelAdmin):
    readonly_fields = ('id',)
    list_display = ('id', 'asan', 'user',)
    list_filter = ('id', 'asan', 'user',)

class AsanaAdmin(admin.ModelAdmin):
    inlines = [YogaImageAdmin]
    readonly_fields = ('id',)
    list_display = ('id', 'asana_name', 'asana_sanscrut_name', 'created_date', 'updated_date', 'created_by')
    list_filter = ("asana_position","asana_type","asana_difficulty")
    
    class Meta:
        model = Asana
        
class YogaImageAdmin(admin.ModelAdmin):
    pass

class AsanaImagesAdmin(admin.ModelAdmin):
    list_display = ('id', 'asana_id',)
    pass
    
admin.site.register(Asana, AsanaAdmin)
admin.site.register(YogaPosition)
admin.site.register(YogaType)
admin.site.register(YogaDificulty)
admin.site.register(favouriteAsana,favouriteAsanaAdmin)
admin.site.register(YogaAsanaSequence)
# admin.site.register(AsanaImages, AsanaImagesAdmin)

