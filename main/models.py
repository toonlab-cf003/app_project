from django.db import models
from django.conf import settings
from django.contrib.auth.models import AbstractUser

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
    filename = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.user_id} - {self.filename}'