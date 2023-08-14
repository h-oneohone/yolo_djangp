from django import forms
from .models import UpLoadImg

class UpLoadImgForm(forms.ModelForm):
    class Meta:
        model = UpLoadImg
        fields = ['img', 'name']