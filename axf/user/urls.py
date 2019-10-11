"""author @ TK_lin"""
from rest_framework.routers import SimpleRouter

from user.views import UserView

router = SimpleRouter()
# 注册路由
# 地址:/api/user/auth/  /api/user/auth/[id]/
# 使用路由注册是下面的操作都在views中的一个类中实现，
# 就可以使用路由注册，自动添加该类下的路由地址到urlpatterns中
# 路由注册依赖rest_framework.routers下的SimpleRouter
# 这里可以根据前端的路由地址来注册路由，写接口
router.register('auth', UserView)
urlpatterns = [

]
urlpatterns += router.urls
