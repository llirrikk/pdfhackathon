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


class merge_form(forms.Form):
    def order(self, pdf_number):
        for i in range(pdf_number):
            n = f'n{i}'
            exec(f'{n} = forms.IntegerField()')
            self.fields[n].initial = i
