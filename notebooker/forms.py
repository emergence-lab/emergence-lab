from django import forms
from django.forms import ModelForm
from django_ace import AceWidget

class NBCellEdit(forms.Form):
    def __init__(self, *args, **kwargs):
        self.cell_count = kwargs.pop('cell_count', None)
        #super(NBCellEdit, self).__init__(*args, **kwargs)
        super(NBCellEdit, self).__init__(*args, **kwargs)

        #self.fields['cell'] = []
        #self.fields['cell'] = {}
        for i in range(self.cell_count):
            self.fields['cell_{}'.format(i)] = forms.CharField(widget=AceWidget(mode='text',
                                                        #theme='twilight',
                                                        width="400px",
                                                        height="100px",
                                                        #label="LABEL",
                                                        showprintmargin=True),
                                                     required=False)
            #self.fields['cell'][i].label = 'LABEL'
        #super(NBCellEdit, self).__init__(*args, **kwargs)
    #cell_upd = forms.IntegerField(required=False)
    #comment = forms.CharField(required=False, max_length=200)

#class NBCellEdit(forms.Form):
#
#    cell = forms.CharField(widget=AceWidget(mode='text',
#                                                #theme='twilight',
#                                                width="800px",
#                                                height="300px",
#                                                showprintmargin=True))
#
#    comment = forms.CharField(required=False, max_length=200)
