from django import forms
from . import views
from . models import PDFile
from .views import *
from django.forms import widgets


class get_pdf_multiple(forms.ModelForm):
    class Meta:
        model = PDFile
        fields = ['file']
        widgets = {
            'file': forms.ClearableFileInput(attrs={'multiple': True})
        }


class get_pdf_single(forms.ModelForm):
    class Meta:
        model = PDFile
        fields = ['file']
        widgets = {
            'file': forms.ClearableFileInput()
        }


class merge_form(forms.Form):
    order = forms.IntegerField()


class rotation(forms.Form):
    angle = forms.IntegerField()


class delete_form(forms.Form):
    to_delete = forms.NullBooleanField(required=False)
