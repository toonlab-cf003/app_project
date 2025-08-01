from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Message, Good
from .forms import PostForm
from django.utils import timezone
# from .forms import NicknameRegisterForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.contrib.auth import logout
# from django.http import HttpResponse
# from django.conf import settings
from django.contrib.auth import get_user_model
# from django.contrib.auth.hashers import make_password

# トップページ -----------------------------------------------------------
def index_view(request):
    return render(request, 'main/index.html')

# 共通テストページ（あれば） ----------------------------------------------
def question_view(request):
    return render(request, 'main/question.html')

# 各問題ページ（小学2年生） -----------------------------------------------
def question2_1_view(request):
    params = {
        'title': '小学2年生｜もんだい①',
        'question': 'りんごが いくつ うれましたか？',
        'choices': ['10こ', '30こ', '50こ'],
        'correct': '30こ',
        'next_url': 'question2_2',
    }
    return render(request, 'main/question_base.html', params)

def question2_2_view(request):
    params = {
        'title': '小学2年生｜もんだい②',
        'question': 'なんこ たべましたか？',
        'choices': ['2こ', '5こ', '7こ'],
        'correct': '5こ',
        'next_url': 'finish2',
    }
    return render(request, 'main/question_base.html', params)

# 小学3年生 -----------------------------------------------------------
def question3_1_view(request):
    params = {
        'title': '小学3年生｜もんだい①',
        'question': 'りんごが いくつ うれましたか？',
        'choices': ['10こ', '30こ', '50こ'],
        'correct': '30こ',
        'next_url': 'question3_2',
    }
    return render(request, 'main/question_base.html', params)

def question3_2_view(request):
    params = {
        'title': '小学3年生｜もんだい②',
        'question': 'りんごが いくつ うれましたか？',
        'choices': ['10こ', '30こ', '50こ'],
        'correct': '30こ',
        'next_url': 'question3_3',
    }
    return render(request, 'main/question_base.html', params)

def question3_3_view(request):
    params = {
        'title': '小学3年生｜もんだい③',
        'question': 'りんごが いくつ うれましたか？',
        'choices': ['10こ', '30こ', '50こ'],
        'correct': '30こ',
        'next_url': 'finish3',
    }
    return render(request, 'main/question_base.html', params)

# 小学4年生 -----------------------------------------------------------
def question4_1_view(request):
    params = {
        'title': '小学4年生｜もんだい①',
        'question': 'りんごが いくつ うれましたか？',
        'choices': ['10こ', '30こ', '50こ'],
        'correct': '30こ',
        'next_url': 'question4_2',
    }
    return render(request, 'main/question_base.html', params)

def question4_2_view(request):
    params = {
        'title': '小学4年生｜もんだい②',
        'question': 'りんごが いくつ うれましたか？',
        'choices': ['10こ', '30こ', '50こ'],
        'correct': '30こ',
        'next_url': 'question4_3',
    }
    return render(request, 'main/question_base.html', params)

def question4_3_view(request):
    params = {
        'title': '小学4年生｜もんだい③',
        'question': 'りんごが いくつ うれましたか？',
        'choices': ['10こ', '30こ', '50こ'],
        'correct': '30こ',
        'next_url': 'question4_4',
    }
    return render(request, 'main/question_base.html', params)

def question4_4_view(request):
    params = {
        'title': '小学4年生｜もんだい④',
        'question': 'りんごが いくつ うれましたか？',
        'choices': ['10こ', '30こ', '50こ'],
        'correct': '30こ',
        'next_url': 'finish4',
    }
    return render(request, 'main/question_base.html', params)

# 終了画面 -----------------------------------------------------------
def finish2_view(request):
    return render(request, 'main/finish2.html')

def finish3_view(request):
    return render(request, 'main/finish3.html')

def finish4_view(request):
    return render(request, 'main/finish4.html')

# 回答処理（仮）-----------------------------------------------------------
def answer_view(request):
    if request.method == 'POST':
        selected = request.POST.get('answer')
        correct = request.POST.get('correct')
        next_url = request.POST.get('next_url', 'index')  # ← ここで受け取る
        current_url = request.POST.get('current_url', 'index')

        if selected == correct:
            # 正解 → correct に next をつけて遷移
            return redirect(f'/correct/?next={next_url}')
        else:
            return redirect(f'/wrong/?retry={current_url}')
    return redirect('index')

# 結果ページ -----------------------------------------------------------
def correct_view(request):
    # セッション or POSTから next_url を取り出して使う
    next_url = request.GET.get('next', 'index')  # なければ index に戻る
    params = {
        'next_url': next_url
    }
    return render(request, 'main/correct.html', params)

def wrong_view(request):
    retry_url = request.GET.get('retry', 'index')
    params = {
        'retry_url': retry_url
    }
    return render(request, 'main/wrong.html', params)

# シールを保存 -----------------------------------------------------------
def save_sticker_view(request):
    if request.method == 'POST':
        sticker = request.POST.get('sticker')
        next_url = request.GET.get('next', 'index')  # ←ここで受け取る！

        if sticker:
            sticker_list = request.session.get('stickers', [])
            sticker_list.append(sticker)
            request.session['stickers'] = sticker_list

        # correct.html を再表示し、next_url を含める！
        return render(request, 'main/correct.html', {
            'next_url': next_url,
            'saved': True,
            'saved_sticker': sticker
        })

    return redirect('index')

# マイページで集めたシールを表示 --------------------------------------------
def mypage_view(request):
    stickers = request.session.get('stickers', [])
    params = {
        'stickers': stickers
    }
    return render(request, 'main/mypage.html', params)

# タイムライン表示と投稿処理　-----------------------------------------------
@login_required
def timeline_view(request):
    messages = Message.objects.all()
    form = PostForm(user=request.user)

    if request.method == 'POST':
        form = PostForm(user=request.user, data=request.POST)
        if form.is_valid():
            message = Message()
            message.owner = request.user
            message.content = form.cleaned_data['content']
            message.pub_date = timezone.now()
            message.save()
            return redirect('timeline')

    params = {
        'messages': messages,
        'form': form,
    }
    return render(request, 'main/timeline.html', params)

# 👍ボタンを押したときの処理（1人1回）　-------------------------------------
@login_required
def good_view(request, pk):
    message = get_object_or_404(Message, pk=pk)
    already_good = Good.objects.filter(owner=request.user, message=message).exists()

    if not already_good:
        Good.objects.create(owner=request.user, message=message, pub_date=timezone.now())
        message.good_count += 1
        message.save()

    return redirect('timeline')

# ユーザー関連　----------------------------------------------------------
User = get_user_model()
# ステップ1：ニックネーム＋敬称を受け取り、セッション保存
def register_view(request):
    if request.method == 'POST':
        request.session['nickname'] = request.POST['nickname']
        request.session['suffix'] = request.POST.get('suffix', '')
        return redirect('register_birthday')
    return render(request, 'main/register.html')

# ステップ2：誕生日を受け取り、セッションに保存 → select_iconへ
def register_birthday_view(request):
    if request.method == 'POST':
        request.session['birthday'] = request.POST['birthday']
        return redirect('select_icon')
    return render(request, 'main/register_birthday.html')

def select_icon_view(request):
    # 仮で10個の画像ファイル名
    icons = [f'player_{str(i)}.jpg' for i in range(1, 16)]
    return render(request, 'main/select_icon.html', {'icons': icons})

User = get_user_model()

def save_icon_view(request):
    if request.method == 'POST':
        icon = request.POST.get('icon')

        # ステップ1～2で保存したセッションデータを取得
        nickname = request.session.get('nickname')
        suffix = request.session.get('suffix')
        birthday = request.session.get('birthday')

        if not all([nickname, suffix, birthday]):
            return redirect('register')  # 情報が足りなければ登録へ戻す

        # ユーザーを作成（usernameは仮で作って、あとでIDで上書き）
        user = User.objects.create_user(
            username='temp_user',
            password=birthday,
            nickname=nickname,
            suffix=suffix,
            icon=icon,
        )
        user.username = f"user_{user.id}"
        user.save()

        # ログインさせてセッションを整理
        login(request, user)
        for key in ['nickname', 'suffix', 'birthday']:
            if key in request.session:
                del request.session[key]
        return redirect('register_done')
    return redirect('select_icon')

@login_required 
def register_done_view(request):
    return render(request, 'main/register_done.html', {
        'nickname': request.user.nickname,
        'suffix': request.user.suffix,
        'icon': request.user.icon,
    })

# ログアウト　----------------------------------------------------------
def logout_view(request):
    logout(request)
    return redirect('index')

