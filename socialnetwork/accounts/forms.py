from django import forms


class UserRegistrationForm(forms.Form):
    Username = forms.CharField()
    Email =    forms.EmailField()
    Password = forms.CharField()

