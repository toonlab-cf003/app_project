from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model

class Command(BaseCommand):
    help = '全ユーザーを表示する'

    def handle(self, *args, **kwargs):
        User = get_user_model()
        for user in User.objects.all():
            self.stdout.write(f"{user.id} | {user.nickname} | {user.username} | {user.icon}")


# コマンドプロンプトで以下を実行
# python manage.py show_users
