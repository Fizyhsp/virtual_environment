"""基础环境."""
from abc import ABCMeta, abstractmethod
from collections.abc import Callable
from dataclasses import KW_ONLY, MISSING, Field, dataclass, field
from functools import cached_property
from inspect import Parameter, signature
from types import UnionType
from typing import TYPE_CHECKING, cast, overload

import marshmallow
from marshmallow import ValidationError, missing
from marshmallow_dataclass import field_for_schema
from typing_extensions import Unpack

from lawen.utils.schema import Schema

if TYPE_CHECKING:
    from typing_extensions import Self

    from lawen.utils.types import (
        InputActionArgs,
        MiniWoBActionArgs,
        ResponseForEachStep,
        ResponseForReset,
        WebArenaActionArgs,
    )


@dataclass
class Action:
    """action基类."""

    name: str
    description: str
    _: KW_ONLY
    enable: bool = True
    func: Callable | None = None
    input_args_schema: dict = field(default_factory=dict)
    metadata: list[dict] | None = None
    tags: list[str] | None = None

    def __post_init__(self: "Self") -> None:
        """初始化."""
        self.schema = cast(
            Schema,
            Schema.from_dict(
                {
                    name: field_for_schema(field_or_type)
                    if isinstance(field_or_type, UnionType | type)
                    else field_for_schema(
                        type(default)
                        if default is not MISSING
                        else type(default_factory()),
                        default_factory
                        if (default_factory := field_or_type.default_factory)
                        is not MISSING
                        else missing
                        if default_factory is MISSING
                        else default,
                        field_or_type.metadata,
                    )
                    if isinstance(field_or_type, Field)
                    and (
                        (default := field_or_type.default) is not MISSING
                        or (default_factory := field_or_type.default_factory)
                        is not MISSING
                    )
                    else field_or_type
                    if isinstance(field_or_type, marshmallow.fields.Field)
                    else marshmallow.fields.Field()
                    for name, field_or_type in self.input_args_schema.items()
                },
            )(),
        )

    @overload
    def __call__(
        self: "Self",
        **input_action_args: Unpack["MiniWoBActionArgs"],
    ) -> str:
        ...

    @overload
    def __call__(
        self: "Self",
        **input_action_args: Unpack["WebArenaActionArgs"],
    ) -> str:
        ...

    def __call__(
        self: "Self",
        **input_action_args: Unpack["InputActionArgs"],
    ) -> str:
        """执行Action."""
        if not self.enable:
            msg = "Action不可用"
            raise ValueError(msg)
        if self.func is None:
            msg = "Action未实现"
            raise ValueError(msg)
        try:
            self.schema.load(
                {
                    name: param.default
                    for name, param in signature(
                        self.func,
                    ).parameters.items()
                    if param.default is not Parameter.empty
                }
                | input_action_args,
            )
        except ValidationError as e:
            msg = "参数不合法"
            raise ValueError(msg) from e
        return self.func(**input_action_args)


@dataclass
class ActionSpace:
    """Action空间."""

    @cached_property
    def actions(self: "Self") -> list[Action]:
        """actions."""
        return []

    @cached_property
    def action_names(self: "Self") -> list[str]:
        """Action names."""
        return [action.name for action in self.actions]

    def get(self: "Self", action_name: str) -> Action:
        """获取Action.

        Args:
            action_name (str): Action名称

        Returns:
            Action: Action实例
        """
        if action_name not in self.action_names:
            msg: str = f"Action {action_name} 不存在"
            raise ValueError(msg)
        return getattr(self, action_name)


@dataclass
class WebEnv(metaclass=ABCMeta):
    """Web environment.

    Args:
        name (str): environment name.
        env_type (str): environment type.
        kwargs (keyword arguments): environment arguments.
    """

    def __init__(
        self: "Self",
        *,
        name: str,
        env_type: str,
        env_task: str | None = None,
    ) -> None:
        """Web environment.

        Args:
            name (str): environment name.
            env_type (str): environment type.
            env_task (str): environment task.
        """
        self.name = name
        self.env_type = env_type
        self.env_task = env_task
        self.action_space: ActionSpace | None = None

    @abstractmethod
    def reset(self: "Self") -> "ResponseForReset":
        """重置."""
        raise NotImplementedError

    @abstractmethod
    def step(self: "Self") -> "ResponseForEachStep":
        """执行Action."""
        raise NotImplementedError
