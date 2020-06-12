from django import forms
from .models import Account, Video


class NewCompanyForm(forms.ModelForm):
    class Meta:
        model = Account
        fields = ('name', 'enabled')


class VideoCreateForm(forms.ModelForm):
    class Meta:
        model = Video
        fields = ['title', 'description', 'digital_master']
    # title = forms.CharField(max_length=50)
    # description = forms.CharField(max_length=500)
    # digital_master = forms.FileField()
