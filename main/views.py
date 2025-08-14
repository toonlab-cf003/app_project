from .forms import NicknameRegisterForm
from .models import Sticker
from django.conf import settings
from django.core.paginator import Paginator
from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth import logout
from django.contrib.auth import get_user_model
from django.contrib.auth import authenticate
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.hashers import make_password
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404

# topページ --------------------------------------------------------------
def index_view(request):
    return render(request, 'main/index.html')

# 問題選択ページ --------------------------------------------------------------
@login_required
def problem_select(request):
    return render(request, 'main/problem_select.html')

# ユーザー関連　-------------------------------------------------------------
User = get_user_model()

# ----- ログイン　-----------------------------------------------------------
def login_view(request):
    if request.method == 'POST':
        nickname = request.POST.get('nickname')
        password = request.POST.get('password')

        try:
            user = User.objects.get(nickname=nickname)
            if user.check_password(password):
                login(request, user)
                messages.success(request, f"{user.nickname}さん、ログインしました！")
                return redirect('index')
            else:
                messages.error(request, "パスワードがちがいます。")
        except User.DoesNotExist:
            messages.error(request, "ニックネームが見つかりません。")

    return render(request, 'main/login.html')

# ----- ログアウト　---------------------------------------------------------
def logout_view(request):
    logout(request)
    return redirect('index')

# ----- 未ログイン　---------------------------------------------------------
def not_logged_view(request):
    return render(request, 'main/not_logged.html')

# ----- セッション保存 ------------------------------------------------------
def register_view(request):
    if request.method == 'POST':
        request.session['nickname'] = request.POST['nickname']
        request.session['suffix'] = request.POST.get('suffix', '')
        return redirect('register_birthday')
    return render(request, 'main/register.html')

def register_birthday_view(request):
    if request.method == 'POST':
        request.session['birthday'] = request.POST['birthday']
        return redirect('select_icon')
    return render(request, 'main/register_birthday.html')

def select_icon_view(request):
    # 仮で10個の画像ファイル名
    icons = [f'player_{str(i)}.jpg' for i in range(1, 16)]
    return render(request, 'main/select_icon.html', {'icons': icons})

def save_icon_view(request):
    if request.method == 'POST':
        icon = request.POST.get('icon')

        nickname = request.session.get('nickname')
        suffix = request.session.get('suffix')
        birthday = request.session.get('birthday')

        if not all([nickname, suffix, birthday]):
            return redirect('select_icon')

        user = User.objects.create_user(
            username='temp_user',
            password=birthday,
            nickname=nickname,
            suffix=suffix,
            icon=icon,
        )
        user.username = f"{user.id}:{user.nickname}"
        user.save()

        # ログインさせてセッションを整理
        login(request, user)
        for key in ['nickname', 'suffix', 'birthday']:
            if key in request.session:
                del request.session[key]
        return redirect('register_done')
    return redirect('select_icon')

def register_done_view(request):
    return render(request, 'main/register_done.html', {
        'nickname': request.user.nickname,
        'suffix': request.user.suffix,
        'icon': request.user.icon,
    })

# 問題ページ ---------------------------------------------------------------
def question2_1_view(request):
    params = {
        'title': '小学2年生｜もんだい①',
        'sab_title': '池に いる 生きものの 数を しらべました。',
        'question': 'いちばん 数が 多いのは 何ですか？',
        'choices': ['めだか', 'こい', 'ざりがに'],
        'correct': 'めだか',
        'next_url': 'question2_2',
        'image_url': '/static/images/question2.png', 
    }
    return render(request, 'main/question_base.html', params)

def question2_2_view(request):
    params = {
        'title': '小学2年生｜もんだい②',
        'sab_title': '池に いる 生きものの 数を しらべました。',
        'question': 'ふなは こいより 何ひき 多いですか？',
        'choices': ['１ぴき', '３びき', '４ひき'],
        'correct': '３びき',
        'next_url': 'finish2',
        'image_url': '/static/images/question2.png', 
    }
    return render(request, 'main/question_base.html', params)

def question3_1_view(request):
    params = {
        'title': '小学3年生｜もんだい①',
        'sab_title': '次のグラフを見て、答えましょう。',
        'question': 'すきな人が いちばん多い スポーツは 何ですか？',
        'choices': ['ドッチボール', '水泳', 'サッカー'],
        'correct': 'サッカー',
        'next_url': 'question3_2',
        'image_url': '/static/images/question3_1.png',
    }
    return render(request, 'main/question_base.html', params)

def question3_2_view(request):
    params = {
        'title': '小学3年生｜もんだい②',
        'sab_title': '次のグラフを見て、答えましょう。',
        'question': 'ドッジボールの人数は、野球の人数の何倍ですか？',
        'choices': ['２倍', '３倍', '５倍'],
        'correct': '２倍',
        'next_url': 'question3_3',
        'image_url': '/static/images/question3_1.png',
    }
    return render(request, 'main/question_base.html', params)

def question3_3_view(request):
    params = {
        'title': '小学3年生｜もんだい③',
        'sab_title': '3年生の町べつの人数を調べました。',
        'question': '表の㋑に入る数は 何でしょう？',
        'choices': ['３０', '３１', '３２'],
        'correct': '３１',
        'next_url': 'finish3',
        'image_url': '/static/images/question3_3.png',
    }
    return render(request, 'main/question_base.html', params)

def question4_1_view(request):
    params = {
        'title': '小学4年生｜もんだい①',
        'sab_title': '次の折れ線グラフを見て問題に答えましょう。',
        'question': 'プールの水の温度がいちばん高かったのは何時ですか？',
        'choices': ['午後２時', '午後３時', '午後７時'],
        'correct': '午後３時',
        'next_url': 'question4_2',
        'image_url': '/static/images/question4_1.png',
    }
    return render(request, 'main/question_base.html', params)

def question4_2_view(request):
    params = {
        'title': '小学4年生｜もんだい②',
        'sab_title': '次の表を見て問題に答えましょう。',
        'question': '日曜日に勉強した人は 何人ですか？',
        'choices': ['２０人', '２１人', '３６人'],
        'correct': '２１人',
        'next_url': 'question4_3',
        'image_url': '/static/images/question4_2.png',
    }
    return render(request, 'main/question_base.html', params)

def question4_3_view(request):
    params = {
        'title': '小学4年生｜もんだい③',
        'sab_title': '次の折れ線グラフを見て問題に答えましょう。',
        'question': 'オーストラリアで気温がいちばん高いのは何月ですか？',
        'choices': ['１月', '８月', '１２月'],
        'correct': '１月',
        'next_url': 'question4_4',
        'image_url': '/static/images/question4_3.png',
    }
    return render(request, 'main/question_base.html', params)

def question4_4_view(request):
    params = {
        'title': '小学4年生｜もんだい④',
        'sab_title': '次の表を見て問題に答えましょう。',
        'question': 'おべんとうも、お茶も注文した人は何人ですか？',
        'choices': ['１２人', '１８人', '２３人'],
        'correct': '１２人',
        'next_url': 'finish4',
        'image_url': '/static/images/question4_4.png',
    }
    return render(request, 'main/question_base.html', params)

# ----- 終了画面 -----------------------------------------------------------
def finish2_view(request):
    return render(request, 'main/finish2.html')

def finish3_view(request):
    return render(request, 'main/finish3.html')

def finish4_view(request):
    return render(request, 'main/finish4.html')

# ----- 回答処理 -----------------------------------------------------------
def answer_view(request):
    if request.method == 'POST':
        selected = request.POST.get('answer')
        correct = request.POST.get('correct')
        next_url = request.POST.get('next_url', 'index')
        current_url = request.POST.get('current_url', 'index')

        if selected == correct:
            # 正解 → correct に next をつけて遷移
            return redirect(f'/correct/?next={next_url}')
        else:
            return redirect(f'/wrong/?retry={current_url}')
    return redirect('index')

# ----- 結果ページ ----------------------------------------------------------
def correct_view(request):
    # セッション or POSTから next_url を取り出して使う
    next_url = request.GET.get('next', 'index')  # なければ index に戻る
    params = {
        'next_url': next_url,
        'sticker_list': range(1, 51),
    }
    return render(request, 'main/correct.html', params)

def wrong_view(request):
    retry_url = request.GET.get('retry', 'index')
    params = {
        'retry_url': retry_url
    }
    return render(request, 'main/wrong.html', params)

# マイページ ----------------------------------------------------------------
def mypage_view(request):
    qs = Sticker.objects.filter(user=request.user).order_by('-created_at')
    filenames = list(qs.values_list('filename', flat=True))
    sticker_count = qs.count()

    paginator = Paginator(filenames, 10)
    page_number = request.GET.get('page') or 1
    page_obj = paginator.get_page(page_number)

    current_page_count = len(page_obj.object_list)
    empty_slots = max(0, 10 - current_page_count)

    rank_title = _rank_title(sticker_count)

    return render(request, 'main/mypage.html', {
        'page_obj': page_obj,
        'empty_slots': empty_slots,
        'sticker_count': sticker_count,        # 合計
        'current_page_count': current_page_count,
        'rank_title': rank_title,              # マイページ用称号
    })

# ----- シールを保存 --------------------------------------------------------
def save_sticker_view(request):
    if request.method != 'POST':
        return redirect('index')

    next_url = request.GET.get('next') or 'index'
    sticker = request.POST.get('sticker')

    if not sticker:
        return render(request, 'main/correct.html', {
            'saved': False,
            'next_url': next_url,
            'error': 'シールをえらんでね！',
        })

    Sticker.objects.create(user=request.user, filename=sticker)

    # --- セッションにもミラー保存（互換用・任意） ---
    sticker_list = request.session.get('stickers', [])
    sticker_list.append(sticker)
    request.session['stickers'] = sticker_list
    request.session.modified = True

    sticker_count = Sticker.objects.filter(user=request.user).count()

    return render(request, 'main/correct.html', {
        'saved': True,
        'saved_sticker': sticker,
        'sticker_count': sticker_count,
        'next_url': next_url,
    })

# ----- 称号 ---------------------------------------------------------------
def _rank_title(count: int) -> str:
    if count <= 10:
        return "かけだし"
    elif count <= 20:
        return "はんにんまえ"
    elif count <= 30:
        return "いちにんまえ"
    elif count <= 40:
        return "じゅくれん"
    elif count <= 50:
        return "たつじん"
    elif count <= 60:
        return "でんせつ"
    else:
        plus = ((count - 61) // 10) + 1
        return f"でんせつ +{min(plus, 100)}"

def save_sticker_view(request):
    if request.method != 'POST':
        return redirect('index')

    next_url = request.GET.get('next') or 'index'
    sticker = request.POST.get('sticker')

    # 何も選んでない→正解画面に戻す
    if not sticker:
        return render(request, 'main/correct.html', {
            'saved': False,
            'next_url': next_url,
            'error': 'シールをえらんでね！',
        })

    # DB保存（重複OK。重複禁止にするなら get_or_create に）
    Sticker.objects.create(user=request.user, filename=sticker)

    # 合計枚数＆称号を正解画面に表示
    sticker_count = Sticker.objects.filter(user=request.user).count()
    rank_title = _rank_title(sticker_count)

    return render(request, 'main/correct.html', {
        'saved': True,
        'saved_sticker': sticker,
        'sticker_count': sticker_count,
        'rank_title': rank_title,
        'next_url': next_url,
    })

