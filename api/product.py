"""商品模块路由。

接口清单：
- POST /product                 新增商品
- GET  /product/{product_id}    查询单个商品
- PUT  /product/{product_id}    修改商品
- POST /product/stock/{id}      扣减库存（进阶：不能超卖）
- GET  /products                商品列表（拓展，方便调试）
"""

from fastapi import APIRouter, Depends
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from api.common import BizError, ok
from models.database import get_db
from models.product import Product
from schemas.product import ProductCreate, ProductOut, ProductUpdate, StockDeduct

router = APIRouter(tags=["商品管理"])

@router.post("/product", summary="新增商品")
def create_product(payload: ProductCreate, db: Session = Depends(get_db)):
    product = Product(**payload.model_dump())
    try:
        db.add(product)
        db.commit()
        db.refresh(product)  # 取回自增 id 和自动生成的 create_time
    except SQLAlchemyError:
        db.rollback()
        raise
    return ok(ProductOut.model_validate(product))


@router.get("/product/{product_id}", summary="查询单个商品")
def get_product(product_id: int, db: Session = Depends(get_db)):
    product = db.get(Product, product_id)
    if product is None:
        raise BizError(404, "该商品不存在")
    return ok(ProductOut.model_validate(product))


@router.put("/product/{product_id}", summary="修改商品信息")
def update_product(
    product_id: int,
    payload: ProductUpdate,
    db: Session = Depends(get_db),
):
    product = db.get(Product, product_id)
    if product is None:
        raise BizError(404, "该商品不存在")

    # exclude_unset=True：只更新客户端真正传过来的字段
    changes = payload.model_dump(exclude_unset=True)
    if not changes:
        raise BizError(400, "没有需要修改的字段")

    try:
        for field, value in changes.items():
            setattr(product, field, value)
        db.commit()
        db.refresh(product)
    except SQLAlchemyError:
        db.rollback()
        raise
    return ok(ProductOut.model_validate(product))


@router.post("/product/stock/{product_id}", summary="扣减库存（不能超卖）")
def deduct_stock(
    product_id: int,
    payload: StockDeduct,
    db: Session = Depends(get_db),
):
    product = db.get(Product, product_id)
    if product is None:
        raise BizError(404, "该商品不存在")
    if product.stock < payload.quantity:
        raise BizError(
            400,
            f"库存不足：当前库存 {product.stock}，需要扣减 {payload.quantity}",
        )

    try:
        product.stock -= payload.quantity
        db.commit()
        db.refresh(product)
    except SQLAlchemyError:
        db.rollback()
        raise
    return ok({"id": product.id, "stock": product.stock}, msg="库存扣减成功")


@router.get("/products", summary="商品列表（拓展）")
def list_products(page: int = 1, size: int = 10, db: Session = Depends(get_db)):
    page = max(page, 1)
    size = min(max(size, 1), 100)  # 防御：每页最多 100 条
    total = db.query(Product).count()
    items = (
        db.query(Product)
        .order_by(Product.id)
        .offset((page - 1) * size)
        .limit(size)
        .all()
    )
    return ok(
        {
            "total": total,
            "page": page,
            "size": size,
            "items": [ProductOut.model_validate(i) for i in items],
        }
    )
