from django import forms
from .models import Account


class NewCompanyForm(forms.ModelForm):
    class Meta:
        model = Account
        fields = ('name', 'enabled')

class VideoCreateForm(forms.Form):
    title = forms.CharField(max_length=50)
    description = forms.CharField(max_length=500)
    digital_master = forms.FileField()
