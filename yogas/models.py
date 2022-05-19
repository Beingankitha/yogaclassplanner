import os
import uuid
from django.db import models
from django.utils import timezone
from PIL import Image
from django.utils.text import slugify
from users.models import WebsiteUser

class YogaDificulty(models.Model):
    difficulty_name = models.CharField(max_length=200, db_index=True, unique=True)
    slug = models.SlugField(max_length=200, db_index=True)

    def __str__(self):
        return f"{self.difficulty_name}"

class YogaPosition(models.Model):
    position_name = models.CharField(max_length=200, db_index=True, unique=True)
    slug = models.SlugField(max_length=200, db_index=True)

    class Meta:
        ordering = ('position_name',)
        verbose_name = 'Position'
        verbose_name_plural = 'Positions'

    def __str__(self):
        return f"{self.position_name}"
    
class YogaType(models.Model):
    type_name = models.CharField(max_length=200, db_index=True)
    slug = models.SlugField(max_length=200, db_index=True)

    def __str__(self):
        return f"{self.type_name}"
    
def content_thumbfile_name(instance, filename):
    ext = filename.split('.')[-1]
    filename = instance.asana_name + "-thumbnail" + "." + ext
    return "%s/%s" %(instance.asana_name, filename)

class Asana(models.Model):
    asana_name = models.CharField(max_length=50, default=None)
    asana_sanscrut_name = models.CharField(max_length=50, default=None)
    asana_english_name = models.CharField(max_length=50, default=None)
    asana_position = models.ForeignKey(YogaPosition, default=None, related_name='position', on_delete = models.CASCADE)
    asana_type = models.ForeignKey(YogaType, default=None, related_name='type',on_delete = models.CASCADE)
    asana_difficulty = models.ForeignKey(YogaDificulty, default=None, related_name='type',on_delete = models.CASCADE)
    how_to_do = models.TextField(max_length=5000, default=None)
    benifit = models.TextField(max_length=500, default=None)
    caution = models.TextField(max_length=500, default=None)
    start_position = models.CharField(max_length=100, default=None)
    concentration = models.CharField(max_length=200, default=None)
    breath = models.CharField(max_length=100, default=None)
    repetitions = models.CharField(max_length=200, default=None)
    image_thumbnail = models.ImageField(upload_to=content_thumbfile_name,null=False, blank=False, default=None)
    created_by = models.CharField(max_length=200, default="system")
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)
    slug = models.SlugField(max_length=50, default=None)
    
    def save(self, *args, **kwargs):
        self.slug = slugify(self.asana_name)
        super(Asana, self).save(*args, **kwargs)  # saving image first
        img = Image.open(self.image_thumbnail.path) # Open image using self
        if img.height > 500 or img.width > 400:
            new_img = (400, 300)
            img.thumbnail(new_img)
            img.save(self.image_thumbnail.path) 
    
    class Meta:
        ordering = ['id','asana_name',]

    def __str__(self):
        return f"{self.asana_name}"

class AsanaImages(models.Model):
    asana_id = models.ForeignKey(Asana, on_delete=models.CASCADE)
    asana_large_image = models.CharField(max_length=200)
    asana_small_image = models.CharField(max_length=200)

    class Meta:
        ordering = ['asana_id']

    def __str__(self):
        return f"{self.asana_id}"
    
def content_file_name(instance, filename):
    ext = filename.split('.')[-1]
    # filename = instance.asana.asana_name + "." + ext
    return "%s/%s" %(instance.asana.asana_name, filename)

class YogaImage(models.Model):
    asana = models.ForeignKey(Asana, default=None, on_delete=models.CASCADE)    
    images = models.FileField(upload_to=content_file_name, null = False, blank = False)
    
    def add(request):
        file = request.POST['images']
        file._name = request.asana.asana_name +"."+ file._name.split('.')[1]
        
    
    class Meta:
        ordering = ['asana_id']

    def __str__(self):
        return f"{self.asana.asana_name}"
    
class YogaAsanaSequence(models.Model):
    seq_name = models.CharField(max_length=50,null=False, blank=False)
    seq_type = models.ForeignKey(YogaType,on_delete=models.CASCADE,default=None,null=True)
    seq_position = models.ForeignKey(YogaPosition,on_delete=models.CASCADE,default=None, null=True)
    seq_difficulty = models.ForeignKey(YogaDificulty,on_delete=models.CASCADE,default=None, null=True)
    seq_asana = models.ForeignKey(Asana, on_delete=models.CASCADE,default=None, null=False,blank=False, related_name="Yoga")
    seq_asana_num = models.IntegerField(default=None, null=False,blank=False)
    
    class Meta:
        ordering = ['id','seq_name',]
    
    def __str__(self):
        return f"{self.seq_name}"
    
class favouriteAsana(models.Model):
    asan = models.ForeignKey(Asana, on_delete=models.CASCADE,default=None, null=False,blank=False)
    user = models.ForeignKey(WebsiteUser, on_delete=models.CASCADE,default=None, null=False,blank=False)
    class Meta:
        unique_together = ['asan','user']