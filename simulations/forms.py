from django import forms
from django.forms import ModelForm
from django_ace import AceWidget
from .models import Simulation


class SimInlineForm(forms.ModelForm):

    device = forms.CharField(widget=AceWidget(mode='text',
                                                theme='twilight',
                                                width="700px",
                                                height="300px",
                                                showprintmargin=True))

    materials = forms.CharField(widget=AceWidget(mode='text',
                                                theme='twilight',
                                                width="700px",
                                                height="300px",
                                                showprintmargin=True))

    physics = forms.CharField(widget=AceWidget(mode='text',
                                                theme='twilight',
                                                width="700px",
                                                height="300px",
                                                showprintmargin=True))

    class Meta:
        model = Simulation
        fields = ['priority', 'execution_node']
