from django.contrib.auth.signals import user_logged_in
from django.dispatch import receiver
from .models import Sticker

@receiver(user_logged_in)
def move_session_stickers_to_db(sender, user, request, **kwargs):
    session_list = request.session.get('stickers', [])
    if not session_list:
        return

    # セッション内のシールをDBに移行
    objs = [Sticker(user=user, filename=f) for f in session_list]
    Sticker.objects.bulk_create(objs, ignore_conflicts=True)  # unique制約があれば衝突無視

    # セッションを空にする
    request.session['stickers'] = []
