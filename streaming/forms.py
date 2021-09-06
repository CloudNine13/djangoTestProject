from django import forms

class UserForm(forms.Form):
    first_name = forms.CharField(label="first name", max_length=100, required=True)
    surname = forms.CharField(label="surname", max_length=100, required=True)
    password = forms.CharField(label="password", max_length=100, widget=forms.PasswordInput(), required=True)