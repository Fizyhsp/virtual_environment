"""项目设置."""
from dataclasses import KW_ONLY, dataclass, field
from datetime import timedelta, timezone

from toml import load


@dataclass
class BaseConfig:
    """项目设置."""

    _: KW_ONLY

    EXPIRES: int  # 日志过期时间
    TIMEZONE: timezone = field(
        default=timezone(timedelta(hours=8), "CST"),
    )  # 时区
    VERBOSE: bool  # 是否显示详细日志
    VERBOSE_LEVEL: int  # 详细日志等级

    USE_MONGO: bool  # 是否使用mongo
    USE_REDIS: bool  # 是否使用redis
    USE_SQL: bool  # 是否使用sql类数据库

    USE_MINIWOB: bool  # 是否使用miniwob
    USE_MIND2WEB: bool  # 是否使用mind2web
    USE_WEBARENA: bool  # 是否使用webarena

    SQL_DATABASE_NAME: str  # sql数据库名称
    MONGO_DATABASE_NAME: str  # mongo数据库名称
    REDIS_CHANNEL_NAME: str  # redis频道名称

    MONGO_URI: str  # mongo地址
    REDIS_URL: str  # redis地址
    SQLALCHEMY_DATABASE_URI: str  # sql地址


Config = BaseConfig(**load("pyproject.toml")["tool"]["lawen"])
