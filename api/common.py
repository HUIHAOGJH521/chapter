"""统一响应体与业务异常。

所有接口成功时都返回 {"code": 200, "msg": "...", "data": ...}，
业务失败抛 BizError，由 main.py 的异常处理器统一转成 JSON。
"""


def ok(data=None, msg: str = "操作成功"):
    """成功响应。"""
    return {"code": 200, "msg": msg, "data": data}

class BizError(Exception):
    """业务异常：例如 404 商品不存在、400 库存不足。"""

    def __init__(self, code: int, msg: str):
        self.code = code
        self.msg = msg
