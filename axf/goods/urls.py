"""author @ TK_lin"""
from django.urls import path
from rest_framework.routers import SimpleRouter

from goods.views import home, FoodTypeView, MarketView

router = SimpleRouter()
# 前端访问/api/goods/foodtype/  调用父类ListModelMixin
router.register('foodtype', FoodTypeView)
router.register('market', MarketView)

urlpatterns = [
    path('home/', home)
]
urlpatterns += router.urls
