from django.db import models

from goods.models import Goods
from user.models import UserModel


class OrderModel(models.Model):
    user = models.ForeignKey(UserModel, on_delete=models.CASCADE)  # 关联用户
    o_num = models.CharField(max_length=64)  # 数量  没用
    # 0 代表已下单，但是未付款， 1 已付款未发货  2 已付款，已发货.....
    o_status = models.IntegerField(default=0)  # 状态
    o_create = models.DateTimeField(auto_now_add=True)  # 创建时间

    class Meta:
        db_table = 'axf_order'


class OrderGoodsModel(models.Model):
    goods = models.ForeignKey(Goods, on_delete=models.CASCADE)  # 关联的商品
    order = models.ForeignKey(OrderModel, on_delete=models.CASCADE)  # 关联的订单
    goods_num = models.IntegerField(default=1)  # 商品的个数

    class Meta:
        db_table = 'axf_order_goods'
