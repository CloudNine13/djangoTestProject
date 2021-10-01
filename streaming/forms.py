from django import forms
from streaming.models import ServiceUser
from django.contrib.auth.forms import UserCreationForm
from django.utils.translation import gettext_lazy as _


class SignUpForm(UserCreationForm):
    error_messages = {
        'password_mismatch': _('Las contraseñas no coinciden. Por favor, introdúzcalas otra vez')
    }

    username = forms.CharField(
        label="username",
        max_length=30,
        help_text='Lo necesitamos para saber como llamarte',
        required=True,
        widget=forms.TextInput(
            attrs={
                'type': 'text',
                'placeholder': 'Username',
            }
        ),
    )

    email = forms.EmailField(
        label="email",
        max_length=60,
        help_text='Lo necesitamos para regitrarte la cuenta',
        required=True,
        widget=forms.TextInput(
            attrs={
                'type': 'text',
                'placeholder': 'Email',
            }
        ),
    )

    password1 = forms.CharField(
        label="password1",
        required=True,
        widget=forms.PasswordInput(
            attrs={
                'type': 'password',
                'placeholder': 'Password',
            }
        ),
    )

    password2 = forms.CharField(
        label="password2",
        required=True,
        widget=forms.PasswordInput(
            attrs={
                'type': 'password',
                'placeholder': 'Confirm Password',
            }
        ),
    )

    class Meta:
        model = ServiceUser
        fields = ('username', 'email', 'password1', 'password2')


class LoginForm(forms.ModelForm):
    username = forms.CharField(label="name", required=True)
    email = forms.EmailField(label="email", required=True)
    password = forms.CharField(label="password1", widget=forms.PasswordInput(), required=True)
