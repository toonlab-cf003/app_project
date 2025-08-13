from django import forms
from .models import CustomUser
from django.contrib.auth.forms import UserCreationForm

class NicknameRegisterForm(UserCreationForm):
    nickname = forms.CharField(label='ニックネーム', max_length=20)
    suffix = forms.ChoiceField(label='', choices=[('さん', 'さん'), ('くん', 'くん'), ('ちゃん', 'ちゃん')])

    class Meta:
        model = CustomUser
        fields = ('nickname', 'suffix', 'username', 'password1', 'password2')