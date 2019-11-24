from django import forms


class VideoCreateForm(forms.Form):
    title = forms.CharField(max_length=50)
    description = forms.CharField(max_length=500)
    digital_master = forms.FileField()
