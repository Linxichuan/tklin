"""author @ TK_lin"""
from django.core.cache import cache
from rest_framework.authentication import BaseAuthentication

from user.models import UserModel
from utils.errors import ParamsException


class UserAuth(BaseAuthentication):
    # 用户认证类

    def authenticate(self, request):
        # 登录地址才做token与user_id的判断
        # 不需要做登录认证的地址，如/register/、/login/、/home/不做认证
        path = request.path
        not_need_auth = ['/api/user/auth/register/',
                         '/api/user/auth/login/',
                         '/api/goods/home/',
                         '/api/goods/market/',
                         '/api/goods/foodtype/',
                         ]
        if path in not_need_auth:
            return None
        # request.query_params.get是GET请求获取
        # token request.data.get是POST请求获取token
        token = request.data.get('token') \
            if request.data.get('token') \
            else request.query_params.get('token')
        if token:
            user_id = cache.get(token)
            if user_id:
                user = UserModel.objects.get(id=user_id)
                return user, token
        res = {
            'code': 1008, 'msg': '用户没有登录，无法执行该操作'
        }
        raise ParamsException(res)



