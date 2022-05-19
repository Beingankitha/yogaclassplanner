from django import forms
from django.forms import ModelForm
from yogas.models import Asana, AsanaImages, YogaImage, YogaDificulty, YogaPosition, YogaType


# position_choice = [ (yogaposition.id, yogaposition.position_name()) for yogaposition in YogaPosition.objects.all() ]

class AsanaForm(forms.ModelForm):
    
    asana_position = forms.ModelChoiceField(queryset=YogaPosition.objects.all())
    # asana_position = forms.ChoiceField(choices=[(pos.id, pos.position_name) for pos in YogaPosition.objects.all()])
    asana_type = forms.ModelChoiceField(queryset=YogaType.objects.all())
    asana_difficulty = forms.ModelChoiceField(queryset=YogaDificulty.objects.all())
    class Meta:
        model = Asana
        fields = ["asana_name", 
                "asana_sanscrut_name",
                "asana_english_name",
                "asana_position",
                "asana_type",
                "asana_difficulty", 
                "how_to_do",
                "benifit", 
                "caution",
                "start_position",
                "concentration",
                "breath",
                "repetitions",
                "image_thumbnail"]
        labels= {"asana_name" : 'Yoga Asana Name', 
                "asana_sanscrut_name" : 'Yoga Asana Sanscrut Name',
                "asana_english_name" : 'Yoga Asana Pose Name:',
                "asana_position" : 'Yoga Asana Position',
                "asana_type" : 'Yoga Asana Type',
                "asana_difficulty" : 'Yoga Asana Difficulty', 
                "how_to_do" : 'Description(With steps)',
                "benifit" : 'Benifit', 
                "caution" : 'Caution',
                "start_position" : 'Starting position',
                "concentration" : 'Enter it concentrate on which body part',
                "breath" : 'Breathing while doing this yoga',
                "repetitions" : 'Repetitions',
                "image_thumbnail" : 'Image Thumbnail'}
        widgets = {"asana_name" : forms.TextInput(attrs={'class':'form-control'}), 
                "asana_sanscrut_name" : forms.TextInput(attrs={'class':'form-control'}),
                "asana_english_name" : forms.TextInput(attrs={'class':'form-control'}),
                "asana_position" :forms.Select(attrs={'class':'form-select'}),
                "asana_type" :forms.Select(attrs={'class':'form-select'}),
                "asana_difficulty" : forms.Select(attrs={'class':'form-select'}), 
                "how_to_do" : forms.Textarea(attrs={'class':'form-control'}),
                "benifit" : forms.TextInput(attrs={'class':'form-control'}), 
                "caution" : forms.TextInput(attrs={'class':'form-control'}),
                "start_position" : forms.TextInput(attrs={'class':'form-control'}),
                "concentration" : forms.TextInput(attrs={'class':'form-control'}),
                "breath" : forms.TextInput(attrs={'class':'form-control'}),
                "repetitions" : forms.TextInput(attrs={'class':'form-control'}),
                "image_thumbnail" : forms.TextInput(attrs={'class':'form-control'})}
        
    
        
        # def __init__(self, *args, **kwargs):
        #     super(AsanaForm, self).__init__(*args, **kwargs)
        #     for visible in self.visible_fields():
        #         visible.field.widget.attrs['class'] = 'form-control'
        
class YogaImageForm(AsanaForm):
    image = forms.ImageField(label="Image",widget=forms.ClearableFileInput(attrs={'multiple': True}))
    class Meta(AsanaForm.Meta):
        fields = AsanaForm.Meta.fields + ['image']