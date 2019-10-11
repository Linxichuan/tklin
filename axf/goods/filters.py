"""author @ TK_lin"""
import django_filters
from goods.models import Goods


class GoodsFilter(django_filters.rest_framework.FilterSet):
    # 接口中过滤的参数 = CharFilter(数据库中过滤的字段， menthods='', lookup_expr='')
    # typeid = django_filters.CharFilter('categoryid')
    childcid = django_filters.CharFilter(method='filter_childcid')
    order_rule = django_filters.CharFilter(method='filter_order_rule')

    class Meta:
        model = Goods
        fields = []

    def filter_childcid(self, queryset, name, value):

         if value == '0':
             return queryset
         else:
             # childcid是子分类的id
             return queryset.filter(childcid=value)

    def filter_order_rule(self, queryset, name, value):

        if value == '0':
            return queryset.order_by('price')
        elif value == '1':
            return queryset.order_by('-price')
        elif value == '2':
            return queryset.order_by('productnum')
        else:
            return queryset.order_by('-productnum')
