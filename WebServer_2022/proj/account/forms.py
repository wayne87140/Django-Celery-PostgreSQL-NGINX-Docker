from django import forms
from account.models import User


class UserForm(forms.ModelForm):
    username = forms.CharField(label = 'Account')
    password = forms.CharField(label = 'Password', widget=forms.PasswordInput())
    
    class Meta:
        model = User
        fields = ['username', 'password']
        