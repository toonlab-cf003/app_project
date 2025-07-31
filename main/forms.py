from django import forms
from .models import Message, Good
from django.contrib.auth.models import User
from .models import CustomUser
from django.contrib.auth.forms import UserCreationForm

class MessageForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ['owner', 'content',]
        
class GoodForm(forms.ModelForm):
    class Meta:
        model = Good
        fields = ['owner', 'message',]

class PostForm(forms.Form):
    content = forms.CharField(max_length=500, widget= forms.Textarea(attrs={'class' : 'form-control', 'rows' : 2}))

    def __init__(self, user, *args, **kwargs):
        super(PostForm, self).__init__(*args, **kwargs)

class NicknameRegisterForm(UserCreationForm):
    nickname = forms.CharField(label='ニックネーム', max_length=20)
    suffix = forms.ChoiceField(label='', choices=[('さん', 'さん'), ('くん', 'くん'), ('ちゃん', 'ちゃん')])

    class Meta:
        model = CustomUser
        fields = ('nickname', 'suffix', 'username', 'password1', 'password2')