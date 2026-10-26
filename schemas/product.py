"""Pydantic 校验模型（请求体 / 响应体）。

对应需求「三、强制约束 & 数据校验」：
- 商品名称不能为空  -> min_length=1
- 价格 > 0          -> gt=0
- 库存 >= 0         -> ge=0
"""

from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class ProductBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=100, description="商品名称，非空")
    price: float = Field(..., gt=0, description="商品价格，必须大于 0")
    stock: int = Field(..., ge=0, description="库存数量，不能为负数")
    category: str = Field(..., min_length=1, max_length=50, description="商品分类")
    is_on_sale: bool = Field(True, description="是否上架，默认 true")


class ProductCreate(ProductBase):
    """POST /product 请求体：create_time 由服务端自动生成，前端不用传。"""


class ProductUpdate(BaseModel):
    """PUT /product/{id} 请求体：全部可选，只改传了的字段。"""

    name: str | None = Field(None, min_length=1, max_length=100)
    price: float | None = Field(None, gt=0)
    stock: int | None = Field(None, ge=0)
    category: str | None = Field(None, min_length=1, max_length=50)
    is_on_sale: bool | None = None


class ProductOut(ProductBase):
    """响应体：补上 id 和 create_time，并允许直接从 ORM 对象读取。"""

    model_config = ConfigDict(from_attributes=True)

    id: int
    create_time: datetime


class StockDeduct(BaseModel):
    """POST /product/stock/{id} 请求体。"""

    quantity: int = Field(..., gt=0, description="扣减数量，必须大于 0")
