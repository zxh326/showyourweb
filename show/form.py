from django import forms

from django.contrib.auth.models import User

class RegisterForm(forms.ModelForm):
    last_name = forms.CharField(
        label='用户名',
        widget=forms.TextInput(
            attrs={
                'class': 'input',
                'type':'text',
                'placeholder': "用户名"
            }
        ),
    )
    username = forms.CharField(
        label=u"学号",
        error_messages={'required': u'请输入学号'},
        widget=forms.TextInput(
            attrs={
                'class': 'input',
                'type':'text',
                'placeholder': "16100000000"
            }
        ),
    )
    email = forms.CharField(
        label='邮箱',
        widget=forms.EmailInput(
            attrs={
            'class': 'input',
            'type':'email',
            'placeholder': "xx@xx.com"
            }
        )
    )
    password = forms.CharField(label='密码', widget=forms.PasswordInput(
            attrs={
                'class': 'input',
                'type':'password',
                'placeholder': "password"
            }
        ))
    password2 = forms.CharField(label='再来一遍', widget=forms.PasswordInput(
            attrs={
                'class': 'input',
                'type':'password',
                'placeholder': "repeat password"
            }
        ))

    class Meta:
        model = User
        fields = ('username', 'email', 'last_name')

    def clean_password2(self):
        cd = self.cleaned_data
        if cd['password'] != cd['password2']:
            raise forms.ValidationError('密码不一样啊')
        return cd['password2']

    # def clean_email(self):
    #     email = self.cleaned_data.get('email')
    #     t = User.objects.filter(email=email)
    #     if len(t) != 0:
    #         raise forms.ValidationError('该邮箱已经注册过了')
    #     else:
    #         return email

class LoginForm(forms.Form):
    username = forms.CharField(
        label=u"学号",
        error_messages={'required': u'请输入用户名'},
        widget=forms.TextInput(
            attrs={
                'class': 'input',
                'type':'text',
                'placeholder': "16100000000"
            }
        ),
    )

    password = forms.CharField(
        required=True,
        label=u"密码",
        error_messages={'required': u'请输入密码'},
        widget=forms.PasswordInput(
            attrs={
                'class': 'input',
                'placeholder': "密码",
                'type': 'password',
            }
        ),
    )


    def clean(self):
        if not self.is_valid():
            raise forms.ValidationError(u"用户名和密码为必填项")
        else:
            cleaned_data = super(LoginForm, self).clean()


class UploadForm(forms.Form):
    """docstring for UploadForm"""
    uploadname = forms.CharField(
        label=u"项目名字",
        error_messages={'required': u'请输入项目名字'},
        widget=forms.TextInput(
            attrs={
                'class': 'input',
                'id': 'file',
                'type':'text',
                'placeholder': "eg: 简历"
            }
        ),
    )

    uploadfile = forms.FileField(
        label='项目文件',
        widget=forms.FileInput(
            attrs={
                'class': 'file-input',
                'multiple':"multiple",
            }
            )
        )
        

class UserEditForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('username', 'last_name','email')

    username = forms.CharField(
        label=u"学号",
        error_messages={'required': u'请输入学号'},
        widget=forms.TextInput(
            attrs={
                'class': 'input',
                'type':'text',
                'readonly':True
            }
        ),
    )
    last_name = forms.CharField(
        label='用户名',
        widget=forms.TextInput(
            attrs={
                'class': 'input',
                'type':'text',
            }
        ),
    )

    email = forms.CharField(
        label='邮箱',
        widget=forms.EmailInput(
            attrs={
            'class': 'input',
            'type':'email',
            }
        )
    )
