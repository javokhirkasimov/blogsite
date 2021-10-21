from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from blog.models import Blog
from .models import Profile
from django import forms

class AddUserInfoForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields=['first_name', 'last_name', 'bio']


class CreateUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ["username", "email", "password1", "password2"]

class MakePostForm(forms.ModelForm):
    class Meta:
        model = Blog
        fields = ["image","title","description","category"]
    
# class EditPostForm(forms.ModelForm):
#     class Meta:
#         model = Blog
#         fields = ["image","title","description","category"]

        

class SetPhotoForm(forms.ModelForm):
    class Meta:
        model=Profile
        fields=['profile_photo']



