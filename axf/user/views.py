import uuid

from django.contrib.auth.hashers import make_password
from django.core.cache import cache
from rest_framework import viewsets, mixins
from rest_framework.decorators import action
from rest_framework.response import Response

from carts.models import CartModel
from orders.models import OrderModel
from user.Serializers import UserSerializer, UserRegisterSerializer, UserLoginSerializer
from user.models import UserModel
from utils.auth import UserAuth
from utils.errors import ParamsException


class UserView(viewsets.GenericViewSet,
               mixins.ListModelMixin):
    # 这里是取到数据库中所有的注册的用户信息，这里其实对注册并没有用，
    queryset = UserModel.objects.all()
    # 这里是用于字段校验，后面重写了校验方法，所以这里的校验方法并没有被使用
    serializer_class = UserSerializer

    # authentication_classes = (UserAuth,)

    # 这里是显示登录成功后的登录者的信息Mine页面发送的是get请求，
    # 所以是重构list方法
    def list(self, request, *args, **kwargs):

        user = request.user
        order_not_pay = OrderModel.objects.filter(user=user, o_status=0).count()
        order_not_send = OrderModel.objects.filter(user=user, o_status=1).count()

        res = {
            'user_info': {
                'u_username': user.username
            },
            'orders_not_pay_num': order_not_pay,
            'order_not_send_num': order_not_send
        }
        return Response(res)

    # def list(self, request, *args, **kwargs):
    #
    #     token = request.query_params.get('token')
    #     if token:
    #         user_id = cache.get(token)
    #         if user_id:
    #             user = UserModel.objects.get(id=user_id)
    #
    #             res = {
    #                 'user_info': {
    #                     'u_username': user.username
    #                 },
    #                 'orders_not_pay_num': '',
    #                 'order_not_send_num': ''
    #             }
    #             return Response(res)
    #     res = {
    #         'code': 1011, 'msg': '没有登录'
    #     }
    #     return Response(res)

    @action(detail=False, methods=['POST'], serializer_class=UserRegisterSerializer)
    def register(self, request):
        # 请求地址:/api/user/auth/register/
        # 请求方式:POST
        # 1.获取前端传递的参数
        data = request.data
        # serializer = self.get_serializer(queryset, many=True)

        # 2.字段校验(重新定义UserRegisterSerializer，validate)
        serializer = self.get_serializer(data=data)
        # 判断校验结果
        result = serializer.is_valid()
        if not result:
            # 这里的serializer.errors显示的是字段校验中设置error_messages信息
            res = {'code': 1004, 'msg': '字段校验错误', 'data': serializer.errors}
            raise ParamsException(res)
        # 3.注册功能实现
        # 取校验成功的数据serializer.data.get('')
        password = make_password(serializer.data.get('u_password'))
        user = UserModel.objects.create(
            username=serializer.data.get('u_username'),
            password=password,
            email=serializer.data.get('u_email')
        )
        # 4.返回数据
        res = {
            'user_id': user.id
        }
        return Response(res)

    @action(detail=False, methods=['POST'], serializer_class=UserLoginSerializer)
    def login(self, request):
        # 请求地址:/api/user/auth/login/
        data = request.data
        serializer = self.get_serializer(data=data)
        result = serializer.is_valid()
        if not result:
            res = {'code': 1005, 'msg': '字段校验错误', 'data': serializer.errors}
            raise ParamsException(res)

        # 登陆标识符的操作
        # 1.获取唯一的标识符传递给前端
        token = uuid.uuid4().hex
        # 2.存储标识符和当前登陆用户的关联关系(redis)
        # 这里取user是为了取得user.id,存入本地数据库，形成标识符和登录用户的关联关系
        user = UserModel.objects.filter(username=serializer.data.get('u_username')).first()
        # 使用redis中的string类型进行存储,存储的key为token值，value为当前登录用户的id值
        # 本地终端获取user.id    get token值
        cache.set(token, user.id, timeout=30000)
        res = {
            'token': token
        }
        return Response(res)
        



