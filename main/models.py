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
    
class Sticker(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='stickers'
    )
    filename = models.CharField(max_length=100)   # 例: "sticker_12.jpg"
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.user_id} - {self.filename}'