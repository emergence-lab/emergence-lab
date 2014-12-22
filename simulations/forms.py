from django import forms
from django.forms import ModelForm
from django_ace import AceWidget
from .models import Simulation


class SimInlineForm(forms.ModelForm):

    device_upload = forms.FileField(required=False, allow_empty_file=True)
    device = forms.CharField(widget=AceWidget(mode='text',
                                                #theme='twilight',
                                                width="800px",
                                                height="300px",
                                                showprintmargin=True))

    materials_upload = forms.FileField(required=False, allow_empty_file=True)
    materials = forms.CharField(widget=AceWidget(mode='text',
                                                #theme='twilight',
                                                width="800px",
                                                height="300px",
                                                showprintmargin=True))

    physics_upload = forms.FileField(required=False, allow_empty_file=True)
    physics = forms.CharField(widget=AceWidget(mode='text',
                                                #theme='twilight',
                                                width="800px",
                                                height="300px",
                                                showprintmargin=True))

    class Meta:
        model = Simulation
        fields = ['priority', 'execution_node', 'investigations']
