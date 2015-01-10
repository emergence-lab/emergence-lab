from django import forms

class GitTokenForm(forms.Form):
    user = forms.CharField(max_length=15)
    password = forms.CharField(max_length=100, widget=forms.PasswordInput(render_value=False))
