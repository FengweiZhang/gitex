from django.shortcuts import render,redirect
from django.http import HttpResponse,Http404,JsonResponse
from django.contrib.auth import authenticate,login,logout,get_user_model
from .forms import (
    LoginForm,
    RegisterForm
)
# Create your views here.

def login_view(request):
    form = LoginForm(request.POST or None)

    # 只有vaild之后才能使用cleaned_data
    if form.is_valid():
        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password')

        # Django默认进行验证
        user = authenticate(request,password=password,username=username)
        if user == None:
            request.sessions['invalid_user'] = 1
            return redirect('/login')
        login(request,user)

        # 这个地方要注意，传给需要渲染的html的时候，需要传递一个字典，而form是一个Form类的子类
        return render(request,'accounts/login_success.html',{'context':form.cleaned_data})
    
    # 如果登录失败就会返回login界面，这个时候需要传递form用于html里面的as_p
    return render(request,'accounts/login.html',{'context':form})
    
# 退出 然后重定向
def logout_view(request):
    logout(request)
    return redirect('/login')


def register_view(request):
    form = RegisterForm(request.POST or None)
    if form.is_valid():
        username = form.cleaned_data.get('username')
        email = form.cleaned_data.get('email')
        password = form.cleaned_data.get('password')
        password2 = form.cleaned_data.get('password2')

        User = get_user_model()
        try:
            user = User.objects.create_user(username=username,password=password,email=email)
        except :
            user = None
        if user != None:
            login(request,user)
            form_data = form.cleaned_data
            return render(request,'accounts/reg_success.html',{'context':form_data})
        else:
            request.sessions['register_error'] = 1
    form = RegisterForm()
    return render(request,'accounts/register.html',{'context':form})
