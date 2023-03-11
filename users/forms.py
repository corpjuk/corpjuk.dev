# users/forms.py
from audioop import reverse
from dataclasses import field
from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.urls import reverse_lazy

from .models import CustomUser


class RegisterForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ("username", "email")


class LogInForm(forms.ModelForm):

    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.form_id = "login-form"
        self.helper.attrs = {
            # I probably want to create a profile/update url. and this POST will not be a login
            "hx-post": reverse_lazy("users:login"),
            "hx-target": "#login-form",
            "hx-swap": "outerHTML",
        }
        self.helper.add_input(Submit("submit", "Submit"))

    def clean_username(self):
        username = self.cleaned_data["username"]
        if len(username) <= 3:
            raise forms.ValidationError("Username is too short")
        return username

    def save(self, commit=True):
        """Hash user's password on save"""
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
        return user

    class Meta:
        model = CustomUser
        fields = ("username", "password")
        # fields = ("username", "email", )
        widgets = {
            "password": forms.PasswordInput(),
            "username": forms.TextInput(
                attrs={
                    "hx-get": reverse_lazy("check-username"),
                    "hx-target": "#div_id_username",
                    "hx-trigger": "keyup[target.value.length > 3]",
                }
            ),
        }


class ProfileForm(forms.Form):

    username = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "hx-get": reverse_lazy("login"),
                "hx-trigger": "keyup changed",
            }
        )
    )
    password = forms.CharField(widget=forms.PasswordInput)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.form_id = "profile-form"
        self.helper.attrs = {
            # I probably want to create a profile/update url. and this POST will not be a login
            "hx-post": reverse_lazy("login"),
            "hx-target": "#profile-form",
            "hx-swap": "outerHTML",
        }
        self.helper.add_input(Submit("submit", "Submit"))

        # So it looks like this is how crispy forms can change the action, method, etc in the html form element
        # helper.form_action and helper.form_method
        # we are going to replace this with htmx
        # self.helper.form_action = reverse_lazy('login')
        # self.helper.form_method = 'POST'

    class Meta:
        model = CustomUser
        fields = (
            "username",
            "email",
        )

    def clean_username(self):
        username = self.cleaned_data["username"]
        if len(username) <= 3:
            raise forms.ValidationError("Username is too short")
        return username

    def save(self, commit=True):
        """Hash user's password on save"""
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
        return user


class LogInForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)
