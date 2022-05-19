import datetime
from django.forms import ModelForm, DateInput
from .models import YogaClass, YogaClassMember
from django import forms
from .validators import *
from django.core.validators import MaxValueValidator, MinValueValidator

def present_or_future_date(value):
    if value < datetime.date.today():
        raise forms.ValidationError("The date cannot be in the past!")
    return value

class YogaClassForm(ModelForm):
    class Meta:
        model = YogaClass
        fields = ["title", "description", "start_time", "end_time", "attendee"]
        # datetime-local is a HTML5 input type
        widgets = {
            "title": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "Enter class title"}
            ),
            "description": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "placeholder": "Enter class description",
                }
            ),
            "start_time": DateInput(
                attrs={"type": "datetime-local", "class": "form-control"},
                format="%Y-%m-%dT%H:%M",
            ),
            "end_time": DateInput(
                attrs={"type": "datetime-local", "class": "form-control", "minDate": 0, "readonly" : "true"},
                format="%Y-%m-%dT%H:%M",
            ),
            'attendee': forms.NumberInput(attrs={
                            "class": "form-control",                
                            'min' : 1,            
                            'max': '15',                            
                        }),
        }
        exclude = ["owner"]
        
        def clean_start_time(self):
            start_time = self.cleaned_data['start_time']
            if start_time < datetime.date.today():
                raise forms.ValidationError('Date cannot be in the past')
            return start_time


        def __init__(self, *args, **kwargs):
            super(YogaClassForm, self).__init__(*args, **kwargs)
            # input_formats to parse HTML5 datetime-local input to datetime field
            self.fields["start_time"].input_formats = ("%Y-%m-%dT%H:%M",)
            self.fields["end_time"].input_formats = ("%Y-%m-%dT%H:%M",)
