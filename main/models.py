from django.db import models
from django.conf import settings
from django.contrib.auth.models import AbstractUser

# Message（コメント）モデル
class Message(models.Model):
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    content = models.TextField(max_length=1000)
    good_count = models.IntegerField(default=0)
    pub_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.content} ({self.owner})'

    class Meta:
        ordering = ['-pub_date']

# Good（いいね）モデル：1ユーザー1回制限あり
class Good(models.Model):
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='good_owner')
    message = models.ForeignKey(Message, on_delete=models.CASCADE)
    pub_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'"{self.message}" (by {self.owner})'

    class Meta:
        ordering = ['-pub_date']

# アカウント登録
class CustomUser(AbstractUser):
    nickname = models.CharField(max_length=20)
    suffix = models.CharField(
        max_length=10,
        choices=[('さん', 'さん'), ('くん', 'くん'), ('ちゃん', 'ちゃん')],
        default='さん'
    )
    icon = models.CharField(max_length=100, blank=True)

    def display_name(self):
        return self.nickname + self.suffix