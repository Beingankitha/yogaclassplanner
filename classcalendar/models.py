from django.db import models
from users.models import WebsiteUser
from yogas.models import YogaAsanaSequence
from django.core.validators import MaxValueValidator, MinValueValidator

def content_thumbfile_name(instance, filename):
    ext = filename.split('.')[-1]
    filename = instance.title + "-thumb" + "." + ext
    return "%s/%s" %(instance.title, filename)

class YogaClass(models.Model):
    owner = models.ForeignKey(WebsiteUser, on_delete=models.CASCADE)
    title = models.CharField(max_length=200, unique=True)
    description = models.TextField()
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    is_active = models.BooleanField(default=True)
    is_deleted = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    attendee = models.IntegerField(default=1, validators=[ MaxValueValidator(20),MinValueValidator(1)])
    image_thumbnail = models.ImageField(upload_to=content_thumbfile_name,null=False, blank=False, default=None)
    asanasequence = models.ForeignKey(YogaAsanaSequence, on_delete=models.CASCADE ,null=True, blank=True)
    
    class Meta:
        ordering = ['id','title', 'start_time', 'end_time']
    
    def __str__(self):
        return self.title
    
class ClassMember(models.Model):
    
    yoga_class = models.ForeignKey(YogaClass, on_delete=models.CASCADE)
    student = models.ForeignKey(WebsiteUser, on_delete=models.CASCADE)
    sequence = models.ForeignKey(YogaAsanaSequence,on_delete=models.CASCADE, null = True, blank=True)
    
    class Meta:
        unique_together = ["yoga_class", "student", ]
        ordering = ['id',]

    def __str__(self):
        return str(self.yoga_class)
    

