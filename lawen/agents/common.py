"""随机智能体."""
from dataclasses import dataclass
from random import Random
from typing import TYPE_CHECKING

from typing_extensions import override

from .basic import BasicAgent

if TYPE_CHECKING:
    from envs import Action
    from typing_extensions import Self


@dataclass
class RandomAgent(BasicAgent):
    """随机智能体."""

    @override
    def __post_init__(self: "Self") -> None:
        """初始化."""
        self._rnd = Random()

    @override
    def next_action(self: "Self", observation: str) -> "Action":
        """Predict the next Action given the observation."""
        observation = str(observation)
        self._rnd.seed(a=observation)
        return self._rnd.choice(seq=self.env.action_space.actions)

    @override
    def plan(self: "Self", observation: str, steps: int = 3) -> list["Action"]:
        """Predict the actions plan given the observation."""
        observation = str(observation)
        self._rnd.seed(a=observation)
        return self._rnd.choices(population=self.env.action_space.actions, k=steps)

    @override
    def reset(self: "Self") -> None:
        """重置."""
        self._rnd.seed(a=None)
