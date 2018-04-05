from django import forms

from django.contrib.auth.models import User


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