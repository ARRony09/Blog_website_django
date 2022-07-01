from django import forms
from django.contrib.auth.forms import UserCreationForm,UserChangeForm
from django.contrib.auth.models import User
from .models import UserProfile

class UserSignUp(UserCreationForm):
    email=forms.EmailField(label="Email Address",required=True)
    class Meta:
        model=User
        fields=('username','email','password1','password2')


class ChangeProfileForm(UserChangeForm):
    class Meta:
        model=User
        fields=('username','email','first_name','last_name','password')

class AddProfilePicForm(forms.ModelForm):
    class Meta:
        model=UserProfile
        fields=('profile_pic',)

