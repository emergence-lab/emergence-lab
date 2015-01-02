from django import forms
from django.forms import ModelForm
from django_ace import AceWidget

class NBCellEdit(forms.Form):

    cell = forms.CharField(widget=AceWidget(mode='text',
                                                #theme='twilight',
                                                width="800px",
                                                height="300px",
                                                showprintmargin=True))

    comment = forms.CharField(required=False, max_length=200)
