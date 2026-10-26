"""ORM 模型：Product（商品表）。

对应需求「一、数据库模型 Product」的 7 个字段：
id / name / price / stock / category / is_on_sale / create_time
"""

from datetime import datetime

from sqlalchemy import Boolean, DateTime, Float, Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from models.database import Base


class Product(Base):
    __tablename__ = "product"

    id: Mapped[int] = mapped_column(
        Integer, primary_key=True, autoincrement=True, comment="商品ID"
    )
    name: Mapped[str] = mapped_column(
        String(100), nullable=False, index=True, comment="商品名称"
    )
    # 练习用 Float；真实项目建议 Numeric(10, 2)，避免浮点误差
    price: Mapped[float] = mapped_column(Float, nullable=False, comment="商品价格")
    stock: Mapped[int] = mapped_column(
        Integer, nullable=False, default=0, comment="库存数量"
    )
    category: Mapped[str] = mapped_column(
        String(50), nullable=False, comment="商品分类（手机/电脑/服饰等）"
    )
    is_on_sale: Mapped[bool] = mapped_column(
        Boolean, nullable=False, default=True, comment="是否上架"
    )
    # default=datetime.now：Python 侧自动填充（本地时间）。
    # 若改用 server_default=func.now()，SQLite 存 UTC，会差 8 小时。
    create_time: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.now, comment="创建时间"
    )
