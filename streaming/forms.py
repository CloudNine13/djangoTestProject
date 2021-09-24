from django import forms
from streaming.models import ServiceUser
from django.contrib.auth.forms import UserCreationForm


class SignUpForm(UserCreationForm):
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
        widget=forms.PasswordInput(
            attrs={
                'type': 'password',
                'placeholder': 'Confirm Password',
            }
        ),
    )


    def clean(self):
        print("ENTERED IN CLEAN")
        cleaned_data = super(SignUpForm, self).clean()
        print("CLEANED DATA", cleaned_data)
        password = cleaned_data["password1"]
        print("CLEANED PASSWORD", password)
        confirm_password = cleaned_data["password2"]
        print("CLEANED CONFIRM PASSWORD", confirm_password)
        if password != confirm_password:
            self.add_error('confirm_password', "Password and confirm password do not match")
            print("ERROR OCCURED")
        print("RETURNING CLEANED DATA", cleaned_data)
        # breakpoint()
        return cleaned_data

    class Meta:
        model = ServiceUser
        fields = ('username', 'email', 'password1', 'password2')


class LoginForm(forms.ModelForm):
    username = forms.CharField(label="name", required=True)
    email = forms.EmailField(label="email", required=True)
    password = forms.CharField(label="password1", widget=forms.PasswordInput(), required=True)
