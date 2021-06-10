from django import forms
from django.contrib.auth import (
    authenticate, get_user_model, password_validation,
)

from django.utils.translation import gettext, gettext_lazy as _
from django.core.exceptions import ValidationError

from core.models import Task

User = get_user_model()


class RegisterForm(forms.ModelForm):
    password = forms.CharField(
        label=_("Password"),
        strip=False,
        widget=forms.PasswordInput(attrs={'autocomplete': 'new-password'}),
        help_text=password_validation.password_validators_help_text_html(),
    )
    confirm_password = forms.CharField(
        label=_("Password confirmation"),
        widget=forms.PasswordInput(attrs={'autocomplete': 'new-password'}),
        strip=False,
        help_text=_("Enter the same password as before, for verification."),
    )

    class Meta:
        model = User
        fields = ['username']

    def clean_password(self):
        password = self.cleaned_data.get('password')
        if len(password) < 8:
            raise ValidationError('Password too short')
        return password

    def clean_confirm_password(self):
        password = self.data['password']
        confirm_password = self.cleaned_data.get('confirm_password')

        if password != confirm_password:
            raise forms.ValidationError('Passwords Must Match!')
        return password


class LoginForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(), required=True, label='Username')
    password = forms.CharField(widget=forms.PasswordInput(),
                               help_text=password_validation.password_validators_help_text_html(), required=True,
                               label='Password')

    def clean_username(self):
        username = self.cleaned_data.get('username')

        try:
            User.objects.get(username=username)
        except:
            raise forms.ValidationError('Invalid Username!')

        return username


class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['title', 'description']



class PositionForm(forms.Form):
    position = forms.CharField()
