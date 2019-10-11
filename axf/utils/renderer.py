"""author @ TK_lin"""
from rest_framework.renderers import JSONRenderer


class MyJSONRenderer(JSONRenderer):

    def render(self, data, accepted_media_type=None, renderer_context=None):
        # render方法为将所有响应的结果(dict)转化为json
        # data为方法中return Response(serializer.data)中的参数
        try:
            code = data.pop('code')
        except:
            code = 200
        try:
            msg = data.pop('msg')
        except:
            msg = '请求成功'
        try:
            result = data.pop('data')
        except:
            result = data
        #     将所有的返回code值都转化为200
        renderer_context['response'].status_code = 200
        res = {
            'code': code,
            'msg': msg,
            'data': result
        }
        return super().render(res)





























