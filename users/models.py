from pickle import TRUE
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
import uuid

class CustomeUser(models.Model):
    uuid = models.CharField(max_length=100,default=uuid.uuid4, editable=False, unique=True)
    email = models.EmailField(max_length=50, unique=True,blank=False, null=False)
    fullname = models.CharField(max_length=20, default=None)    
    gender = models.CharField(max_length=6, default=None)
    address = models.CharField(max_length=150, default=None)
    is_health = models.CharField(max_length=3, default=None)
    health_info = models.CharField(max_length=50, default=None)
    registered_as = models.CharField(max_length=10, default=None)
    password = models.CharField(max_length=150,default=None)
    auth_token = models.CharField(max_length=100, default=None, blank=True, null=True)
    is_active = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.fullname}"
    

class WebsiteUser(models.Model):
    id = models.CharField(max_length=100,default=uuid.uuid4, editable=False, unique=True)
    email = models.EmailField(_('email address'), max_length=50, unique=True, primary_key=True)
    fullname = models.CharField(max_length=20, default=None)
    gender = models.CharField(max_length=6, default=None)
    address = models.CharField(max_length=150, default=None)
    is_health = models.CharField(max_length=3, default=None)
    health_info = models.CharField(max_length=50, default=None)
    registered_as = models.CharField(max_length=10, default=None)
    password = models.CharField(max_length=150,default=None)
    is_active = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    

    def __str__(self):
        return f"{self.fullname}"
    
    
class MedicalInformation(models.Model):
    user_email = models.ForeignKey(WebsiteUser, default=None,on_delete = models.CASCADE)
    abdominal = models.BooleanField(default=False)
    back_pain = models.BooleanField(default=False)
    neck = models.BooleanField(default=False)
    hip = models.BooleanField(default=False)
    heart = models.BooleanField(default=False)
    low_blood_pressure = models.BooleanField(default=False)
    arthritis = models.BooleanField(default=False)
    spine = models.BooleanField(default=False)
    knee = models.BooleanField(default=False)
    shoulder = models.BooleanField(default=False)
    asthma = models.BooleanField(default=False)
    epilepsy_brain = models.BooleanField(default=False)
    anxiety_depression = models.BooleanField(default=False)
    respiratory_issues = models.BooleanField(default=False)
    eye = models.BooleanField(default=False)
    kidney = models.BooleanField(default=False)
    high_blood_pressure = models.BooleanField(default=False)
    other_problems = models.BooleanField(default=False)
    other_information = models.CharField(max_length=150, default=None)
    any_old_injury = models.BooleanField(default=False)
    any_old_injury_info = models.CharField(max_length=150, default=None)
    is_yoga_exp = models.BooleanField(default=False)
    yoga_exp_level = models.CharField(max_length=15, default=None)
    
    def __str__(self):
        return f"{self.user_email.fullname}"
    
    

