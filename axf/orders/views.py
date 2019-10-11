import uuid

from rest_framework import viewsets, mixins
from rest_framework.response import Response

from carts.models import CartModel
from orders.filters import OrderFilter
from orders.models import OrderModel, OrderGoodsModel
from orders.serializers import OrderSerializer


class OrdersView(viewsets.GenericViewSet,
                 mixins.ListModelMixin,
                 mixins.CreateModelMixin):

    queryset = OrderModel.objects.all()

    serializer_class = OrderSerializer

    filter_class = OrderFilter

    def get_queryset(self):

        return self.queryset.filter(user=self.request.user)

    def create(self, request, *args, **kwargs):
        # 请求地址: /api/orders/orders/
        # 请求方式: post

        # 1.获取登录用户user、获取创建的订单号
        user = request.user
        # 订单号
        o_num = uuid.uuid4().hex
        # 2.查询购物车中商品is_select为True的数据
        # is_select=True代表商品处于被选中的状态
        carts = CartModel.objects.filter(is_select=True, user=user).all()
        if len(carts):
            # 3.创建订单
            order = OrderModel.objects.create(user=user, o_num=o_num)
            # 4.创建订单详情
            for cart in carts:
                OrderGoodsModel.objects.create(goods=cart.goods,
                                               order=order,
                                               goods_num=cart.c_num)
                # 4.已下单的商品，应该从购物车中删掉
                cart.delete()
                res = {
                    'msg': '下单成功'
                }
        else:
            res = {
                'code': 1012, 'msg': '没有下单的商品，请添加'
            }
        return Response(res)



