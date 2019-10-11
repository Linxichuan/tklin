from django.core.cache import cache
from rest_framework import viewsets, mixins
from rest_framework.decorators import action
from rest_framework.response import Response

from carts.models import CartModel
from carts.serializers import CartSerializer


class CartView(viewsets.GenericViewSet,
               mixins.ListModelMixin,
               mixins.UpdateModelMixin):
    queryset = CartModel.objects.all()

    serializer_class = CartSerializer

    # 用户认证
    # authentication_classes = (UserAuth,)

    # 将添加的商品展示在购物车中，判断商品是否处于全选状态，
    # 统计选中商品的总价格，设置收货人的地址等等
    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        user = request.user
        # 过滤
        queryset = queryset.filter(user=user)

        serializer = self.get_serializer(queryset, many=True)
        # 全选按钮为True，条件为:当前用户下的购物车中所有商品的is_select为True
        # 全选按钮为False，条件为:当前用户下的购物车中只要有商品的is_select为False
        all_select = True
        if CartModel.objects.filter(user=user, is_select=False).exists():
            all_select = False
        total_price = 0

        for item in serializer.data:
            if item['c_is_select']:
                total_price += item['c_goods_num'] * item['c_goods']['price']

        res = {
            'carts': serializer.data,
            'total_price': total_price,
            'all_select': all_select,  # 全选按钮
            'user_info': user.username
        }
        return Response(res)

    @action(detail=False, methods=['POST'])
    def add_cart(self, request):
        # 请求地址: /api/cart/cart/add_cart/
        # 请求方式: post
        # 1.根据前端传递的token进行判定用户是否登录
        goodsid = request.data.get('goodsid')
        user = request.user
        user_cart = CartModel.objects.filter(user=user,
                                             goods_id=goodsid).first()
        if user_cart:
            user_cart.c_num += 1
            user_cart.save()
        else:
            CartModel.objects.create(user=user,
                                     goods_id=goodsid)
        res = {'msg': '添加商品成功'}
        return Response(res)

    @action(detail=False, methods=['POST'])
    def sub_cart(self, request):
        # 获取用户信息
        user = request.user
        # 获取前端传递的商品id
        goodid = request.data.get('goodsid')
        # 1.获取用户user对象、前端传递的商品id
        # 2.根据用户和商品id获取购物车中的商品
        user_cart = CartModel.objects.filter(user=user,
                                             goods_id=goodid).first()
        if user_cart.c_num == 1:
            # 数据库删除
            user_cart.delete()
        else:
            user_cart.c_num -= 1
            user_cart.save()
        res = {
            'msg': '减少商品成功'
        }
        return Response(res)
        # 3.减少商品数量，如果商品c_num为1，删除数据，否则自减1

    # 修改商品的选中状态
    def update(self, request, *args, **kwargs):
        # 修改当前选择的商品的is_select字段
        # 获取选择的商品的对象
        instance = self.get_object()
        instance.is_select = not instance.is_select
        instance.save()
        res = {
            'msg': '选择状态修改成功'
        }
        return Response(res)

    @action(detail=False, methods=['PATCH'])
    # 作用是点击全选按钮的效果，如果选中，点击则全部取消，如果没有选中，点击则全部选中
    def change_select(self, request):
        user = request.user
        # 1.判断当前用户下的购物车中是否有is_select为False的商品
        # 如果有，所有的is_select修改为True
        if CartModel.objects.filter(user=user, is_select=False).exists():
            CartModel.objects.filter(user=user).update(is_select=True)
        # 2.如果没有，所有的is_select修改为False
        else:
            CartModel.objects.filter(user=user).update(is_select=False)
        res = {
            'msg': '商品状态选择成功'
        }
        return Response(res)

    # def list(self, request, *args, **kwargs):
    #     queryset = self.get_queryset()
    #     # 1.获取前端传递的token
    #     token = request.query_params.get('token')
    #     if token:
    #         user_id = cache.get(token)
    #         if user_id:
    #             # 过滤
    #             queryset = queryset.filter(user_id=user_id)
    #             # 数据序列化
    #             serializer = self.get_serializer(queryset, many=True)
    #             res = {
    #                 'carts': serializer.data,
    #                 'total_price': ''
    #             }
    #             return Response(res)
    #     res = {'code': 1009,
    #            'msg': '用户没有登录，请登录'}
    #     return Response(res)
    #
    #     # 2.根据token获取用户信息
    #     # 3.判断是否登录
    #
    # @action(detail=False, methods=['POST'])
    # def add_cart(self, request):
    #     # 请求地址: /api/cart/cart/add_cart/
    #     # 请求方式: post
    #     # 1.根据前端传递的token进行判定用户是否登录
    #     token = request.data.get('token')
    #
    #     if token:
    #         user_id = cache.get(token)
    #         if user_id:
    #             # 2.如果登录，则向cartmodel中添加数据
    #             goodsid = request.data.get('goodsid')
    #             user_cart = CartModel.objects.filter(user_id=user_id,
    #                                                  goods_id=goodsid).first()
    #             if user_cart:
    #                 user_cart.c_num += 1
    #                 user_cart.save()
    #             else:
    #                 CartModel.objects.create(user_id=user_id,
    #                                          goods_id=goodsid)
    #             res = {'msg': '添加商品成功'}
    #             return Response(res)
    #     # 3.如果没有登录，应该抛异常信息，信息为:没有登录，无法添加商品，请去登录
    #     res = {
    #         'code': 1008,
    #         'msg': '用户没有登录'
    #     }
    #     return Response(res)
