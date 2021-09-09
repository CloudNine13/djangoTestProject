from django import forms
from django.contrib.auth import get_user_model


class SignUpForm(forms.ModelForm):
    username = forms.CharField(label="name", required=True)
    email = forms.CharField(label="email", required=True)
    password = forms.CharField(label="password", widget=forms.PasswordInput(), required=True)

    class Meta:
        model = get_user_model()
        fields = ('email', 'password')


class LoginForm(forms.ModelForm):
    username = forms.CharField(label="name", required=True)
    email = forms.EmailField(label="email", required=True)
    password = forms.CharField(label="password", widget=forms.PasswordInput(), required=True)
