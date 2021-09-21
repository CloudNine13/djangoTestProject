from django import forms
from streaming.models import ServiceUser
from django.contrib.auth.forms import UserCreationForm


class SignUpForm(UserCreationForm):
    username = forms.CharField(
        label="name",
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

    password = forms.CharField(
        label="password",
        required=True,
        widget=forms.PasswordInput(
            attrs={
                'type': 'password',
                'placeholder': 'Password',
            }
        ),
    )

    confirm_password = forms.CharField(
        label="password",
        widget=forms.PasswordInput(
            attrs={
                'type': 'password',
                'placeholder': 'Confirm Password',
            }
        ),
    )

    def clean(self):
        cleaned_data = super(SignUpForm, self).clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")
        if password != confirm_password:
            self.add_error('confirm_password', "Password and confirm password do not match")
        return cleaned_data

    class Meta:
        model = ServiceUser
        fields = ('username', 'email', 'password', 'confirm_password')


class LoginForm(forms.ModelForm):
    username = forms.CharField(label="name", required=True)
    email = forms.EmailField(label="email", required=True)
    password = forms.CharField(label="password", widget=forms.PasswordInput(), required=True)
