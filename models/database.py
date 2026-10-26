"""数据库连接层：engine / SessionLocal / Base / get_db。

SQLite 只有一个文件（ecommerce.db），零安装，适合练习；
换成 MySQL 只需把 URL 改成 "mysql+pymysql://..."，其余代码不动。
"""

from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker

# 数据库文件放在项目根目录
SQLALCHEMY_DATABASE_URL = "sqlite:///./ecommerce.db"

# check_same_thread=False：FastAPI 的同步路由可能在不同线程里使用连接池
engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
)

# 每个请求一个 Session；autoflush / autocommit 关闭，由代码显式 commit
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)

class Base(DeclarativeBase):
    """所有 ORM 模型的基类（SQLAlchemy 2.0 写法）。"""
def get_db():
    """FastAPI 依赖：请求进来开 Session，请求结束自动关闭。"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
