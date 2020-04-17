import json

from werkzeug.exceptions import HTTPException
from config import development_environment



class API_exception(HTTPException):
    error_code = 999

    def __init__(self, msg='一些意外发生了', debug_msg=None, http_code=200, data={}, state=34):
        self.data = data  # 如果请求成功,返回的信息
        self.state = state  # 自定义状态码 便于前端处理
        self.code = http_code  # http状态码
        self.msg = msg  # 错误信息
        self.debug_msg = debug_msg  # 一些调试信息
        if data:
            self.debug_msg = debug_msg
        super(API_exception, self).__init__(self.msg, None)

    def get_body(self, environ=None):
        body = {"msg": self.msg,
                "stateCode": self.state,
                "data": self.data,

                }

        if development_environment and self.debug_msg:
            body.update({"msg": f"""{self.msg} 
#########################################################################################
{str(self.debug_msg)}"""})

        text = json.dumps(body)

        return text

    def get_headers(self, environ=None):
        return [('Content-Type', 'application/json')]



