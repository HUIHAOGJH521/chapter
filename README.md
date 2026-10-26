# 电商商品管理模块（FastAPI + SQLAlchemy）

商品 `Product` 的 RESTful 接口练习：新增 / 查询 / 修改 / 扣库存（不能超卖），统一返回体与异常处理。

## 项目结构

```
PythonProject3/
├── main.py              # 入口：装配路由、CORS、统一异常处理
├── requirements.txt
├── models/
│   ├── database.py      # engine / SessionLocal / Base / get_db
│   └── product.py       # Product ORM 模型（7 个字段）
├── schemas/
│   └── product.py       # Pydantic 请求/响应模型 + 校验规则
└── api/
    ├── common.py        # 统一响应 ok() 与业务异常 BizError
    └── product.py       # 商品路由（5 个接口）
```

## 运行

```bash
# 1. 安装依赖（只需一次）
pip install -r requirements.txt

# 2. 启动（二选一）
uvicorn main:app --reload
python main.py

# 3. 打开文档测试
#    http://127.0.0.1:8000/docs
```

首次启动会在项目根目录生成 `ecommerce.db`（SQLite），删掉它即可重建空库。

## 接口

| 方法 | 路径 | 说明 |
|---|---|---|
| POST | `/product` | 新增商品 |
| GET | `/product/{product_id}` | 查询单个商品，不存在返回 404 |
| PUT | `/product/{product_id}` | 修改商品，只改传了的字段 |
| POST | `/product/stock/{product_id}` | 扣减库存，库存不足返回 400 |
| GET | `/products?page=1&size=10` | 商品列表（拓展，便于调试） |

成功响应：

```json
{"code": 200, "msg": "操作成功", "data": {"id": 1, "name": "iPhone 15", "price": 5999.0, "...": "..."}}
```

## 学习检查点

1. **database.py**：为什么 SQLite 要 `check_same_thread=False`？`get_db` 为什么用 `yield`？
2. **models/product.py**：`Mapped[int]` 与 `mapped_column` 是 SQLAlchemy 2.0 写法；`create_time` 为什么用 Python 的 `default` 而不是数据库的 `server_default`？
3. **schemas/product.py**：`gt=0` / `ge=0` / `min_length=1` 分别对应哪条需求？`from_attributes=True` 解决什么问题？
4. **api/product.py**：`exclude_unset=True` 为什么能实现"部分更新"？超卖是怎么拦住的？
5. **main.py**：三个 exception_handler 分别接住了什么异常？为什么统一返回体里还要带 HTTP 状态码？

## 可继续做的练习

- 给列表接口加 `category`、`is_on_sale` 过滤和价格区间筛选
- 用 `SELECT ... FOR UPDATE` 或条件更新（`UPDATE product SET stock = stock - :n WHERE id = :id AND stock >= :n`）解决并发超卖
- 把 `create_all` 换成 Alembic 迁移
- 加 `GET /product/search?keyword=` 模糊搜索
