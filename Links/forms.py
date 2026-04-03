from django import forms
from .models import URLMap

class URLForm(forms.ModelForm):
    custom_alias = forms.CharField(
        required=False,
        max_length=50,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Custom name (optional) - hal: google, facebook',
        }),
        help_text="Opsyonal: Kung gusto mo ng specific na pangalan ng short link"
    )
    
    class Meta:
        model = URLMap
        fields = ['original_url', 'custom_alias']
        widgets = {
            'original_url': forms.URLInput(attrs={
                'class': 'form-control',
                'placeholder': 'phase the link here...',
            })
        }
        labels = {
            'original_url': 'Long URL'
        }