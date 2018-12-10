from django.shortcuts import render, redirect
from django.contrib.auth import login as django_login, logout as django_logout, authenticate
from django.template.loader import get_template
from django.template.context_processors import csrf
from .forms import LoginForm, SignupForm, UserInfoForm
from django.http import HttpResponse
from member.models import UserInfo


# 초기 페이지
def login(request):
    if request.user.is_authenticated:
        return redirect('rec')
    template = get_template('root.html')
    if request.method == 'POST':
        # Data bounded form인스턴스 생성
        if request.POST.get("login"):
            login_form = LoginForm(request.POST)
            # 유효성 검증에 성공할 경우
            if login_form.is_valid():
                # form으로부터 username, password값을 가져옴
                username = login_form.cleaned_data['username']
                password = login_form.cleaned_data['password']

                # 가져온 username과 password에 해당하는 User가 있는지 판단한다
                # 존재할경우 user변수에는 User인스턴스가 할당되며,
                # 존재하지 않으면 None이 할당된다
                user = authenticate(
                    username=username,
                    password=password
                )
                # 인증에 성공했을 경우
                if user:
                    # Django의 auth앱에서 제공하는 login함수를 실행해 앞으로의 요청/응답에 세션을 유지한다
                    django_login(request, user)
                    # Post목록 화면으로 이동
                    return redirect('rec')
                # 인증에 실패하면 login_form에 non_field_error를 추가한다
                login_form.add_error(None, '아이디 또는 비밀번호가 올바르지 않습니다')
        elif request.POST.get("join"):
            user = signup(request)
            django_login(request, user)
            return redirect('rec')
        else:
            print('error')
    else:
        login_form = LoginForm()
        signup_form = SignupForm()
        info_form = UserInfoForm()
    context = {'login_form': login_form, 'signup_form': signup_form, 'info_form': info_form}
    context.update(csrf(request))
    return HttpResponse(template.render(context))


def logout(request):
    django_logout(request)
    return redirect('/')


def signup(request):
    signup_form = SignupForm(request.POST)
    info_form = UserInfoForm(request.POST)
    # 유효성 검증에 통과한 경우 (username의 중복과 password1, 2의 일치 여부)
    print(request.POST)
    if signup_form.is_valid() and info_form.is_valid():
        gender = info_form.cleaned_data['gender']
        age = info_form.cleaned_data['age']
        # SignupForm의 인스턴스 메서드인 signup() 실행, 유저 생성
        user = signup_form.signup()
        UserInfo.objects.create(user=user, gender=gender, age=age)
        return user

"""
def signup(request):
    
    if request.method == 'POST':
        signup_form = SignupForm(request.POST)
        info_form = UserInfoForm(request.POST)
        # 유효성 검증에 통과한 경우 (username의 중복과 password1, 2의 일치 여부)
        print(request.POST)
        if signup_form.is_valid() and info_form.is_valid():
            gender = info_form.cleaned_data['gender']
            age = info_form.cleaned_data['age']
            # SignupForm의 인스턴스 메서드인 signup() 실행, 유저 생성
            user = signup_form.signup()
            UserInfo.objects.create(user=user, gender=gender, age=age)
            return redirect('rec')
    else:
        signup_form = SignupForm()
        info_form = UserInfoForm()


    context = {'signup_form': signup_form, 'info_form': info_form}
    context.update(csrf(request))
    return HttpResponse(template.render(context))
"""