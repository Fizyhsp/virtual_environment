"""基础智能体."""
from abc import ABCMeta, abstractmethod
from dataclasses import KW_ONLY, dataclass
from typing import TYPE_CHECKING

from lawen.envs import Action, WebEnv

if TYPE_CHECKING:
    from typing_extensions import Self


@dataclass
class BasicAgent(metaclass=ABCMeta):
    """智能体."""

    name: str
    env: WebEnv
    _: KW_ONLY
    task: str | None = None
    actions: list[Action] | None = None

    def __post_init__(self: "Self") -> None:
        """初始化."""
        self.actions = self.env.action_space.actions
        if self.env.env_task is not None:
            self.task = self.env.env_task
        if self.task is None:
            msg = "Agent / Env need a task"
            raise ValueError(msg)

    @abstractmethod
    def next_action(self: "Self") -> "Action":
        """Predict the next Action given the observation."""
        raise NotImplementedError

    @abstractmethod
    def plan(self: "Self") -> list["Action"]:
        """Predict the actions plan given the observation."""
        raise NotImplementedError

    @abstractmethod
    def reset(self: "Self") -> None:
        """Predict the actions plan given the observation."""
        raise NotImplementedError
