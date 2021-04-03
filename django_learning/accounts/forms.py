# 这个用来定义登录、注册的类
# 显示登录、注册界面的时候就会显示他们的属性
from django.contrib.auth import get_user_model
from django import forms
# 先获取一个User的类的实例
User = get_user_model()

# 这个是用来禁止非法用户名
UNALLOWED_USER_NAME = ['zerz']

# 登录表
class LoginForm(forms.Form):
    # 使用initial来初始化 不是default
    username = forms.CharField(initial='username')
    password = forms.CharField(
        initial= None,
        widget = forms.PasswordInput(
            attrs={
                'class' : 'form-control',
                'id' : 'password',
            }
        )
    )


    def clean_username(self):
        # cleaned_data就得到Form子类的字典了
        username = self.cleaned_data.get('username')
        qs = User.objects.filter(username__iexact=username)
        if not qs.exists():
            raise forms.ValidationError('This is an invalid user! And this message is from clean_username.')
        return username



class RegisterForm(forms.Form):
    username = forms.CharField(initial='username')

    # 表示这个字段是必须的
    email = forms.EmailField(required=True,initial='email@example.com')
    password = forms.CharField(
        initial = None,
        label = 'password',
        widget = forms.PasswordInput(
            attrs={
                'class' : 'form-control',
                'id' : 'password',
            }
        )
    )

    password2 = forms.CharField(
        initial = None,
        label = 'password2',

        # 这个是单纯针对密码的一些小控件
        widget = forms.PasswordInput(
            attrs={
                'class' : 'form-control',
                'id' : 'password2',
            }
        )
    )
    # 检查用户名合法性，目前不知道为什么还不行
    def clean_username(self):
        username = self.cleaned_data.get('username')
        qs = User.objects.filter(username__iexact=username)
        if qs.exists() or username in UNALLOWED_USER_NAME:
            raise forms.ValidationError('This is an invalid username, please pick another!')
        return username

    # 检查email合法性，目前不知道为什么还不行
    def clean_email(self):
        email = self.cleaned_data.get('email')
        qs = User.objects.filter(username__iexact=email)
        if qs.exists():
            raise forms.ValidationError('This email is already used, please pick another!')
        return email
