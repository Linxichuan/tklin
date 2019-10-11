"""author @ TK_lin"""
import re

from django.contrib.auth.hashers import check_password
from rest_framework import serializers

from user.models import UserModel
from utils.errors import ParamsException


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = UserModel
        fields = '__all__'


# 只实现字段校验功能
class UserRegisterSerializer(serializers.Serializer):
    u_username = serializers.CharField(required=True, max_length=10,
                                       min_length=3,
                                       error_messages={
                                         'required': '该参数必填',
                                         'max_length': '不超过10字符',
                                         'min_length': '不短于3字符'
                                       })
    u_password = serializers.CharField(required=True, max_length=16,
                                       min_length=6,
                                       # style在输入密码会不可见
                                       style={'input_type': 'password'},
                                       error_messages={
                                         'required': '该参数必填',
                                         'max_length': '不超过16字符',
                                         'min_length': '不短于6字符'
                                       })
    u_password2 = serializers.CharField(required=True, max_length=16,
                                        min_length=6,
                                        style={'input_type': 'password'},
                                        error_messages={
                                         'required': '该参数必填',
                                         'max_length': '不超过16字符',
                                         'min_length': '不短于6字符'
                                        })
    u_email = serializers.CharField(required=True,
                                    error_messages={
                                     'required': '该参数必填'
                                    })

    def validate(self, attrs):
        # 1.账号必须不存在
        username = attrs.get('u_username')
        if UserModel.objects.filter(username=username).exists():
            res = {'code': 1001, 'msg': '账号已存在,请更换账号'}
            raise ParamsException(res)
        # 2.密码和确认密码必须一致
        f_password = attrs.get('u_password')
        s_password = attrs.get('u_password2')
        if f_password != s_password:
            res = {'code': 1002, 'msg': '两次输入的密码不一致'}
            raise ParamsException(res)
        # 3.邮箱正则匹配
        email = attrs.get('u_email')
        patterns = re.fullmatch('^[a-z0-9][\w.\-]*@[a-z0-9\-]+(\.[a-z]{2,5}){1,2}$', email)
        if not patterns:
            res = {'code': 1003, 'msg': '邮箱格式不正确'}
            raise ParamsException(res)
        return attrs


class UserLoginSerializer(serializers.Serializer):

    u_username = serializers.CharField(required=True, max_length=10,
                                       min_length=3,
                                       error_messages={
                                           'required': '该参数必填',
                                           'max_length': '不超过10字符',
                                           'min_length': '不短于3字符'
                                       })
    u_password = serializers.CharField(required=True, max_length=16,
                                       min_length=6,
                                       error_messages={
                                           'required': '该参数必填',
                                           'max_length': '不超过16字符',
                                           'min_length': '不短于6字符'
                                       })

    def validate(self, attrs):
        # 1.账号必须存在
        username = attrs.get('u_username')
        user = UserModel.objects.filter(username=username).first()
        if not user:
            res = {'code': 1005, 'msg': '账号不存在'}
            raise ParamsException(res)
        password = attrs.get('u_password')
        # user = UserModel.objects.filter(username=username).first()
        if not check_password(password, user.password):
            res = {'code': 1006, 'msg': '密码不正确'}
            raise ParamsException(res)
        return attrs






