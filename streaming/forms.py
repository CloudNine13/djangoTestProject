from django import forms
from django.contrib.auth import get_user_model


class SignUpForm(forms.ModelForm):
    name = forms.CharField(label="name", required=True, widget=forms.TextInput(attrs={
        'type': 'text',
        'placeholder': 'Username',
    }))

    email = forms.CharField(label="email", required=True, widget=forms.TextInput(attrs={
        'type': 'text',
        'placeholder': 'Email',
    }))

    password = forms.CharField(label="password", widget=forms.PasswordInput(attrs={
        'type': 'password',
        'placeholder': 'Password',
    }), required=True)

    confirm_password = forms.CharField(label="password", widget=forms.PasswordInput(attrs={
        'type': 'password',
        'placeholder': 'Confirm Password',
    }), required=True)

    def clean(self):
        cleaned_data = super(SignUpForm, self).clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")
        if password != confirm_password:
            self.add_error('confirm_password', "Password and confirm password do not match")
        return cleaned_data

    class Meta:
        model = get_user_model()
        fields = ('name', 'email', 'password')


class LoginForm(forms.ModelForm):
    username = forms.CharField(label="name", required=True)
    email = forms.EmailField(label="email", required=True)
    password = forms.CharField(label="password", widget=forms.PasswordInput(), required=True)
