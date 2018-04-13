from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.http import JsonResponse
from mypet.models import Mypets, MypetsImage, PetBattleImages

class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User #where the user data wants to go in the database
        fields = ['username', 'email', 'password']

    def clean_username(self):
        username = self.cleaned_data['username']
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError("Username taken")
        return username


class PetForm(forms.ModelForm):
    class Meta:
        model = Mypets
        fields = ('petname', 'species',)


class ImageForm(forms.ModelForm):
    image = forms.ImageField()
    class Meta:
        model = MypetsImage
        fields = ('image', )

class PetBattleForm(forms.ModelForm):
    image1 = forms.CharField(max_length=100)
    image1_count = forms.IntegerField(required=False)
    image2 = forms.CharField(max_length=100)
    image2_count = forms.IntegerField(required=False)


    class Meta:
        model = PetBattleImages
        fields = ('image1','image2', 'image1_count', 'image1_count',)