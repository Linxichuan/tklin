"""author @ TK_lin"""
import django_filters

from orders.models import OrderModel


class OrderFilter(django_filters.rest_framework.FilterSet):
    o_status = django_filters.CharFilter(method='filter_status')

    class Meta:
        model = OrderModel
        fields = []

    def filter_status(self, queryset, name, value):
        # 所有的订单
        if value == 'all':
            return queryset
        # 未支付的订单
        elif value == 'not_pay':
            return queryset.filter(o_status=0)
        # 支付了未发送的订单
        else:
            return queryset.filter(o_status=1)



