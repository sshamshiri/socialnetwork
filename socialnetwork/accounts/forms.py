from django import forms


class UserRegistrationForm(forms.Form):
    Username = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}))
    Email =    forms.EmailField(widget=forms.EmailInput(attrs={'class':'form-control'}))
    Password = forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control','placeholder':'Your password'}))

