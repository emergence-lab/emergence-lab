from django import forms
from django.forms import ModelForm
from django_ace import AceWidget
from .models import Simulation


class SimInlineForm(forms.ModelForm):

    document = forms.CharField(widget=AceWidget(mode='text',
                                                theme='twilight',
                                                width="400px",
                                                height="300px",
                                                showprintmargin=True))

    doc_test = forms.CharField(widget=AceWidget(mode='text',
                                                theme='twilight',
                                                width="400px",
                                                height="300px",
                                                showprintmargin=True))

    class Meta:
        model = Simulation
        fields = ['priority', 'execution_node']
