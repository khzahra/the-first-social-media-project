from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from .models import Profile


class UserRegistrationForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(attrs={"class": "form-control",
                                                             'placeholder': "Enter Your Username here:"}))
    email = forms.CharField(widget=forms.EmailInput(attrs={"class": "form-control",
                                                           'placeholder': "Enter Your Email Here:"}))
    password1 = forms.CharField(label="password", widget=forms.PasswordInput(attrs={"class": "form-control",
                                                                 'placeholder': "Enter Your Password Here:"}))
    password2 = forms.CharField(label="confirm password", widget=forms.PasswordInput(attrs={"class": "form-control",
                                                                 'placeholder': "Enter Your Password Here:"}))

    def clean_email(self):
        email = self.cleaned_data['email']
        user = User.objects.filter(email=email).exists()
        if user:
            raise ValidationError("This EMAIL is already exist.")
        return email

    def clean_username(self):
        username = self.cleaned_data['username']
        user = User.objects.filter(username=username).exists()
        if user:
            raise ValidationError("This USERNAME is already exist.")
        return username

    # def clean(self):
    #     cd = super().clean()
    #     p1 = cd.get("password1")
    #     p2 = cd.get("password2")
    #     if p1 and p2 and p1 != p2:
    #         raise ValidationError("Passwords must match")

    def clean(self):
        cd = self.cleaned_data
        p1 = cd['password1']
        p2 = cd["password2"]
        if p1 and p2 and p1 != p2:
            raise ValidationError("Passwords must match")


class UserLoginForm(forms.Form):
    username = forms.CharField(label="username or email", widget=forms.TextInput(attrs={"class": "form-control",
                                                             'placeholder': "Enter Your Username Or Your Email Here:"}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={"class": "form-control",
                                                                 'placeholder': "Enter Your Password Here:"}))


class EditUserForm(forms.ModelForm):
    email = forms.EmailField()
    class Meta:
        model = Profile
        fields = ('age', 'bio')
