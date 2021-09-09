from django import forms
from django.contrib.auth import get_user_model


class SignUpForm(forms.ModelForm):
    name = forms.CharField(label="name", required=True)
    email = forms.CharField(label="email", required=True)
    password = forms.CharField(label="password", widget=forms.PasswordInput(), required=True)

    class Meta:
        model = get_user_model()
        fields = ('name', 'email', 'password')
        attrs = {
            'type': 'text',
            'name': 'fancy-text',
            'id': 'fancy-text',
            'autocomplete': 'off'
        }
        widgets = {
            'name': forms.TextInput(attrs=attrs),
            'email': forms.TextInput(attrs=attrs),
            'password': forms.TextInput(attrs=attrs)
        }


class LoginForm(forms.ModelForm):
    username = forms.CharField(label="name", required=True)
    email = forms.EmailField(label="email", required=True)
    password = forms.CharField(label="password", widget=forms.PasswordInput(), required=True)
