from rest_framework.renderers import JSONRenderer
 
#重写render方法
class customrenderer(JSONRenderer):
    def render(self, data, accepted_media_type=None, renderer_context=None):
        '''
        :param data: 返回的数据
        :param accepted_media_type:接收的类型
        :param renderer_context: 呈现的内容
        '''
        #if renderer_context 相当于if request.method=="POST" 如果有请求的数据过来
        if renderer_context:
            #判断是否为实例
            if isinstance(data,dict):#判断返回的数据是否是字典
                msg=data.pop('msg',"成功")#如果是字典获取字典当中的msg参数
                code=data.pop("code",200)#如果是字典获取字典当中code参数
            else:#非字典类型
                msg="成功"
                code=200
                # 重新构建返回的JSON字典
            for key in data:
                # 判断是否有自定义的异常的字段
                if key == 'message':
                    msg = data[key]
                    data = data["detail"]
                    code = code
            ret={
                "code":code,
                "message":msg,
                "detail":data
            }#重新构建返回数据格式
            return super().render(ret,accepted_media_type,renderer_context)#返回数据格式
        else:
            return super().render(data,accepted_media_type,renderer_context)