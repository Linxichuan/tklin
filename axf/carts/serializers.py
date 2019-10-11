from rest_framework import serializers

from carts.models import CartModel
from goods.models import Goods
from goods.serializers import GoodsSerializer


class CartSerializer(serializers.ModelSerializer):
    # 序列化商品对象信息，方法3
    # goods = GoodsSerializer()

    class Meta:
        model = CartModel
        fields = '__all__'

    def to_representation(self, instance):
        # 这儿重构是购物车里商品是否被选中(is_select),
        # 商品数量(c_num),商品本身的信息(goods)
        data = super().to_representation(instance)
        data['c_is_select'] = data['is_select']
        data['c_goods_num'] = data['c_num']
        data['c_goods'] = data['goods']

        # 序列化商品对象信息，方法1
        # goods = Goods.objects.filter(id=data['goods']).first()
        # instance是代表购物车 ，instance.goods代表从购物车里拿出数据
        goods = instance.goods
        # 将购物车里的商品数据进行序列化
        # 这里序列化是显示商品的名称，价格，图片
        data['c_goods'] = GoodsSerializer(goods).data

        # 序列化商品对象信息，方法2
        # data['c_goods'] = {
        #     'id': instance.goods.id,
        #     'price': instance.goods.price,
        # }
        del data['c_num']
        del data['user']
        del data['is_select']
        del data['goods']

        return data
