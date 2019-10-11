from django.db import models

from goods.models import Goods
from user.models import UserModel


class CartModel(models.Model):
    user = models.ForeignKey(UserModel, on_delete=models.CASCADE)  # 关联用户
    goods = models.ForeignKey(Goods, on_delete=models.CASCADE)  # 关联商品
    c_num = models.IntegerField(default=1)  # 商品的个数
    is_select = models.BooleanField(default=True)  # 是否选择商品

    class Meta:
        db_table = 'axf_cart'
