from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import viewsets, mixins

from goods.filters import GoodsFilter
from goods.models import MainWheel, MainNav, MainShow, FoodType, Goods
from goods.serializers import MainWheelSerializer, MainNavSerializer, MainShowSerializer, FoodTypeSerializer, \
    GoodsSerializer


# 这里是展示首页的数据，
# 因为这里涉及到多个model所以用@api_view这种方式
@api_view(['GET'])
def home(request):
    # 这三组是取得三个模型内的所有的数据
    main_wheels = MainWheel.objects.all()
    main_navs = MainNav.objects.all()
    main_shows = MainShow.objects.all()
    res = {
        # 将数据序列化并返回
        'main_wheels': MainWheelSerializer(main_wheels, many=True).data,
        'main_navs': MainNavSerializer(main_navs, many=True).data,
        'main_shows': MainShowSerializer(main_shows, many=True).data,
    }
    return Response(res)


# 这个分类是实现商品的一级分类
class FoodTypeView(viewsets.GenericViewSet,
               mixins.ListModelMixin):

    queryset = FoodType.objects.all()

    serializer_class = FoodTypeSerializer


# 这个类是实现商品的子分类
class MarketView(viewsets.GenericViewSet,
                 mixins.ListModelMixin):  # 前端访问/api/goods/market/ GET 调用ListModelMixin请求

    queryset = Goods.objects.all()

    serializer_class = GoodsSerializer

    filter_class = GoodsFilter

    def list(self, request, *args, **kwargs):
        # 这一步是将选中分类全部展示
        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(queryset, many=True)

        # order_rule_list构造[{id:'', chile_name='', chile_value=''}...]
        rule_list = [
            {'id': 1, 'order_name': '价格升序', 'order_value': '0'},
            {'id': 2, 'order_name': '价格降序', 'order_value': '1'},
            {'id': 3, 'order_name': '销量升序', 'order_value': '2'},
            {'id': 4, 'order_name': '销量降序', 'order_value': '3'},
        ]

        # foodtype_chilename_list构造[{id: '', child_name='', child_value=''}...]
        # 将选中的一级分类的id拿到
        typeid = request.query_params.get('typeid')
        food_type = FoodType.objects.filter(typeid=typeid).first()
        a = food_type.childtypenames

        # 简单方法
        # d = []
        # for b in a.split('#'):
        #     c = {
        #         'child_name': b.split(':')[0],
        #         'child_value': b.split(':')[1]
        #     }
        #     d.append(c)

        # 列表推导式
        d = [{'child_name': item.split(':')[0], 'child_value': item.split(':')[1]} for item in a.split('#')]
        # chilename_list = [
        #     {'child_name': '全部分类', 'chile_value': '0'},
        #     {'child_name': '进口水果', 'chile_value': '103534'},
        #     {'child_name': '国产水果', 'chile_value': '103533'},
        # ]
        res = {
            'goods_list': serializer.data,
            # 综合排序
            'order_rule_list': rule_list,
            # 全部分类
            'foodtype_childname_list': d
        }
        return Response(res)
