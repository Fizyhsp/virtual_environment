"""测试日志模块."""
from logging import Logger

from sqlalchemy.orm import Session

from lawen.utils import Config
from lawen.utils.logger import Logs, MongoHandler, RedisHandler, SQLHandler


def test_sqlite_sql_logger() -> None:
    """测试日志模块."""
    logger = Logger("sqlite")
    logger.setLevel(Config.VERBOSE_LEVEL)
    handler = SQLHandler()
    handler.setLevel(Config.VERBOSE_LEVEL)
    logger.addHandler(handler)
    logger.log(Config.VERBOSE_LEVEL, "test")
    with Session(handler.engine) as session:
        assert (
            session.query(Logs)
            .filter(Logs.level == "VERBOSE")
            .order_by(Logs.time.desc())
            .first()
            .message
            == "test"
        )


def test_mysql_sql_logger() -> None:
    """测试日志模块."""
    Config.SQLALCHEMY_DATABASE_URI = (
        f"mysql://root:123456@localhost:3306/{Config.SQL_DATABASE_NAME}"
    )
    logger = Logger("mysql")
    logger.setLevel(Config.VERBOSE_LEVEL)
    handler = SQLHandler()
    handler.setLevel(Config.VERBOSE_LEVEL)
    logger.addHandler(handler)
    logger.log(Config.VERBOSE_LEVEL, "test")
    with Session(handler.engine) as session:
        assert (
            session.query(Logs)
            .filter(Logs.level == "VERBOSE")
            .order_by(Logs.time.desc())
            .first()
            .message
            == "test"
        )


def test_postgresql_sql_logger() -> None:
    """测试日志模块."""
    Config.SQLALCHEMY_DATABASE_URI = f"postgresql://postgres:123456@localhost:5432/{Config.SQL_DATABASE_NAME}"
    logger = Logger("postgresql")
    logger.setLevel(Config.VERBOSE_LEVEL)
    handler = SQLHandler()
    handler.setLevel(Config.VERBOSE_LEVEL)
    logger.addHandler(handler)
    logger.log(Config.VERBOSE_LEVEL, "test")
    with Session(handler.engine) as session:
        assert (
            session.query(Logs)
            .filter(Logs.level == "VERBOSE")
            .order_by(Logs.time.desc())
            .first()
            .message
            == "test"
        )


def test_redis_logger() -> None:
    """测试日志模块."""
    logger = Logger("redis")
    logger.setLevel(Config.VERBOSE_LEVEL)
    handler = RedisHandler()
    handler.setLevel(Config.VERBOSE_LEVEL)
    logger.addHandler(handler)
    ps = handler.db.pubsub()
    ps.subscribe(Config.REDIS_CHANNEL_NAME)
    logger.log(Config.VERBOSE_LEVEL, "test")
    for msg in ps.listen():
        if msg["type"] == "message":
            assert msg["data"].decode() == "test"
            break


def test_mongo_logger() -> None:
    """测试日志模块."""
    logger = Logger("mongo")
    logger.setLevel(Config.VERBOSE_LEVEL)
    handler = MongoHandler()
    handler.setLevel(Config.VERBOSE_LEVEL)
    logger.addHandler(handler)
    logger.log(Config.VERBOSE_LEVEL, "test")
    assert (
        handler.collection.find_one({"level": "VERBOSE"})["message"] == "test"
    )
