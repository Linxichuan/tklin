"""author @ TK_lin"""
from rest_framework import serializers

from goods.models import MainWheel, MainNav, MainShow, FoodType, Goods


class MainWheelSerializer(serializers.ModelSerializer):

    class Meta:
        model = MainWheel
        fields = '__all__'


class MainNavSerializer(serializers.ModelSerializer):
    class Meta:
        model = MainNav
        fields = '__all__'


class MainShowSerializer(serializers.ModelSerializer):
    class Meta:
        model = MainShow
        fields = '__all__'


class FoodTypeSerializer(serializers.ModelSerializer):

    class Meta:
        model = FoodType
        fields = ['typename', 'typeid']


class GoodsSerializer(serializers.ModelSerializer):

    class Meta:
        model = Goods
        fields = '__all__'

