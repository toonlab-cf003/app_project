from django.urls import path
# from django.contrib.auth import views as auth_views
from . import views
from django.contrib.auth.views import LoginView

urlpatterns = [
    path('', views.index_view, name='index'),

    # クイズ（学年別・問題別）------------------------------------------
    path('question2_1/', views.question2_1_view, name='question2_1'),
    path('question2_2/', views.question2_2_view, name='question2_2'),
    path('question3_1/', views.question3_1_view, name='question3_1'),
    path('question3_2/', views.question3_2_view, name='question3_2'),
    path('question3_3/', views.question3_3_view, name='question3_3'),
    path('question4_1/', views.question4_1_view, name='question4_1'),
    path('question4_2/', views.question4_2_view, name='question4_2'),
    path('question4_3/', views.question4_3_view, name='question4_3'),
    path('question4_4/', views.question4_4_view, name='question4_4'),

    path('finish2/', views.finish2_view, name='finish2'),
    path('finish3/', views.finish3_view, name='finish3'),
    path('finish4/', views.finish4_view, name='finish4'),

    # その他ページ ----------------------------------------------------
    path('answer/', views.answer_view, name='answer'),
    path('correct/', views.correct_view, name='correct'),
    path('wrong/', views.wrong_view, name='wrong'),
    path('save_sticker/', views.save_sticker_view, name='save_sticker'),
    path('mypage/', views.mypage_view, name='mypage'),


    # タイムライン関連 ----------------------------------------------------
    path('timeline/', views.timeline_view, name='timeline'),
    path('good/<int:pk>/', views.good_view, name='good'),

    # ユーザー関連 ----------------------------------------------------
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('register/', views.register_view, name='register'),
    path('register_birthday/', views.register_birthday_view
        , name='register_birthday'),
    path('select_icon/', views.select_icon_view, name='select_icon'),
    path('save_icon/', views.save_icon_view, name='save_icon'),
    path('register_done/', views.register_done_view, name='register_done'),


]
