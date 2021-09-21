from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm


class SignUpForm(UserCreationForm):
    email = forms.EmailField(max_length=60, help_text='Lo necesitamos para regitrarte la cuenta')
    confirm_password = forms.PasswordInput()

    def clean(self):
        cleaned_data = super(SignUpForm, self).clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")
        if password != confirm_password:
            self.add_error('confirm_password', "Password and confirm password do not match")
        return cleaned_data

    class Meta:
        model = get_user_model()
        fields = ('username', 'email',)


class LoginForm(forms.ModelForm):
    username = forms.CharField(label="name", required=True)
    email = forms.EmailField(label="email", required=True)
    password = forms.CharField(label="password", widget=forms.PasswordInput(), required=True)
