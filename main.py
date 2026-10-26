"""FastAPI 入口：装配路由、注册中间件、统一异常处理。

启动方式（二选一）：
    uvicorn main:app --reload
    python main.py
然后打开 http://127.0.0.1:8000/docs 测试接口。
"""

from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from sqlalchemy.exc import SQLAlchemyError
from starlette.middleware.cors import CORSMiddleware

from api.common import BizError
from api.product import router as product_router
from models.database import Base, engine

# 建表：练习够用；真实项目用 Alembic 做迁移，不要 create_all
Base.metadata.create_all(bind=engine)

app = FastAPI(title="电商商品管理 API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    # 注意：allow_origins=["*"] 与 allow_credentials=True 是浏览器不接受的组合，
    # 需要带 Cookie 时请把 "*" 换成具体的前端地址
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(product_router)


# ---------------------------------------------------------------- 统一异常处理
@app.exception_handler(BizError)
async def biz_error_handler(request: Request, exc: BizError):
    """业务异常 -> {"code": 404, "msg": "该商品不存在", "data": null}"""
    return JSONResponse(
        status_code=exc.code,
        content={"code": exc.code, "msg": exc.msg, "data": None},
    )


@app.exception_handler(RequestValidationError)
async def validation_error_handler(request: Request, exc: RequestValidationError):
    """把 Pydantic 的报错翻译成一句中文，避免直接抛 422 英文栈。"""
    first = exc.errors()[0]
    field = ".".join(str(part) for part in first["loc"][1:]) or "请求参数"
    return JSONResponse(
        status_code=422,
        content={
            "code": 422,
            "msg": f"参数校验失败：{field} —— {first['msg']}",
            "data": None,
        },
    )


@app.exception_handler(SQLAlchemyError)
async def sqlalchemy_error_handler(request: Request, exc: SQLAlchemyError):
    """数据库兜底：不把 SQL 细节和堆栈暴露给前端。"""
    return JSONResponse(
        status_code=500,
        content={"code": 500, "msg": "数据库操作失败，请稍后重试", "data": None},
    )


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
