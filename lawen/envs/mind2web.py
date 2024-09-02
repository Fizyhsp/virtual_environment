"""Mind2Web环境."""
from dataclasses import dataclass, field
from difflib import SequenceMatcher
from functools import cached_property
from logging import warning
from pathlib import Path
from typing import TYPE_CHECKING, TypedDict, cast
from uuid import UUID

from numpy import mean
from typing_extensions import Unpack

from lawen.utils import json, make_instance

from .basic import Action, ActionSpace, WebEnv

if TYPE_CHECKING:
    from typing_extensions import Self

    from lawen.utils.types import KWARGS, ResponseForEachStep, ResponseForReset


@dataclass
class Mind2WebActionOperation:
    """Mind2Web Action操作."""

    op: str
    original_op: str
    value: str


@dataclass(init=False)
class Mind2WebActionCandidate:
    """Mind2Web Action候选."""

    backend_node_id: int
    tag: str

    attributes: str | None = None

    def __init__(
        self: "Self",
        backend_node_id: int,
        tag: str,
        attributes: str | None = None,
        value: str | None = None,
        **other: "KWARGS",
    ) -> None:
        """Mind2Web Action候选.

        Args:
            backend_node_id (int):  unique id for the element.
            tag (str): HTML tag of the element.
            attributes (str, optional): serialized attributes of the element.
            Defaults to None.
            value (str, optional): optional value for the operation, e.g., text to
            type, option to select
            other (KWARGS): 其他参数
        """
        self.backend_node_id = backend_node_id
        self.tag = tag
        self.attributes = attributes
        self.value = value
        (setattr(self, k, v) for k, v in other.items() if v is not None)

    def reward(self: "Self", ground_truth: "Self") -> float:
        """Get reward of the action.

        Args:
            ground_truth (Self): ground truth
        """
        return mean(
            [
                self.tag == ground_truth.tag,
                self.backend_node_id == ground_truth.backend_node_id,
                SequenceMatcher(
                    None,
                    self.value or "",
                    ground_truth.value,
                ).quick_ratio(),
            ]
            if isinstance(ground_truth.value, str)
            else [
                self.tag == ground_truth.tag,
                self.backend_node_id == ground_truth.backend_node_id,
            ],
        )


@dataclass
class Mind2WebActionData:
    """Mind2Web Action数据."""

    action_uid: UUID
    cleaned_html: str
    _neg_candidates: list[Mind2WebActionCandidate] = field(
        metadata={"data_key": "neg_candidates"},
    )
    operation: Mind2WebActionOperation
    _pos_candidates: list[Mind2WebActionCandidate] = field(
        metadata={"data_key": "pos_candidates"},
    )
    raw_html: str

    def __post_init__(self: "Self") -> None:
        """初始化candidates."""
        self.candidates = self._neg_candidates + self._pos_candidates


@dataclass
class Mind2WebSituation:
    """Mind2Web场景."""

    action_reprs: list[str]
    actions: list[Mind2WebActionData]
    annotation_id: UUID
    confirmed_task: str
    domain: str
    subdomain: str
    website: str


@dataclass
class Mind2WebActionSpace(ActionSpace):
    """Mind2Web Action空间."""

    @cached_property
    def click(self: "Self") -> Action:
        """点击."""

        def func(backend_node_id: int, tag: str) -> Mind2WebActionCandidate:
            """点击.

            Args:
                backend_node_id (Target): 目标元素id
                tag (str): 目标元素tag

            Returns:
                Mind2WebActionCandidate: 执行结果
            """
            return Mind2WebActionCandidate(
                backend_node_id=backend_node_id,
                tag=tag,
            )

        return make_instance(
            cls=Action,
            name="click",
            func=func,
            description="Click the element in web page",
            input_args_schema={
                "backend_node_id": int,
                "tag": str,
            },
        )

    @cached_property
    def type(self: "Self") -> Action:  # noqa: A003
        """输入."""

        def func(backend_node_id: int, tag: str, text: str) -> str:
            """输入.

            Args:
                backend_node_id (Target): 目标元素id
                tag (str): 目标元素tag
                text (str): 输入文本

            Returns:
                str: 执行结果
            """
            return Mind2WebActionCandidate(
                backend_node_id=backend_node_id,
                tag=tag,
                text=text,
            )

        return make_instance(
            cls=Action,
            name="type",
            func=func,
            description="type the element in web page",
            input_args_schema={"backend_node_id": int, "tag": str, "text": str},
        )

    @cached_property
    def select(self: "Self") -> Action:
        """选择."""

        def func(
            backend_node_id: int,
            tag: str,
            option: dict,
        ) -> str:
            """选择.

            Args:
                backend_node_id (Target): 目标元素id
                tag (str): 目标元素tag
                option (dict): 选项

            Returns:
                str: 执行结果
            """
            return Mind2WebActionCandidate(
                backend_node_id=backend_node_id,
                tag=tag,
                option=option,
            )

        return make_instance(
            cls=Action,
            name="select",
            func=func,
            description="select the element in web page",
            input_args_schema={
                "backend_node_id": int,
                "tag": str,
                "option": dict,
            },
        )

    @cached_property
    def actions(self: "Self") -> list[Action]:
        """actions."""
        return [self.click, self.type, self.select]


class Mind2WebActionArgs(TypedDict):
    """Mind2Web Action参数."""

    backend_node_id: int
    tag: str
    text: str
    option: dict


class Mind2WebEnv(WebEnv):
    """Mind2Web环境."""

    def __init__(
        self: "Self",
        *,
        dataset_path: str | Path,
        env_task: str | None = None,
        env_type: str,
        name: str,
    ) -> None:
        """初始化."""
        self.env_task = env_task
        self.env_type = env_type
        self.name = name
        self.action_space = Mind2WebActionSpace()
        if not Path(dataset_path).exists():
            msg = f"{dataset_path} not found"
            raise FileNotFoundError(msg)
        with Path(dataset_path).open("r") as f:
            self.situations = {
                situation.annotation_id: situation
                for situation in cast(
                    list[Mind2WebSituation],
                    make_instance(
                        Mind2WebSituation,
                        many=True,
                        list_data=json.loads(f.read()),
                    ),
                )
            }
        self.available_annotation_ids = list(self.situations.keys())
        self.situations_step_index = 0

    def reset(
        self: "Self",
        annotation_id: UUID | None = None,
    ) -> "ResponseForReset":
        """重置环境.

        Args:
            annotation_id (UUID): 场景id

        Returns:
            observation (dict): An element of the environment's observation_space.
            info (dict) : Infos.
        """
        info = {}
        if annotation_id is None:
            self.now_situation = self.situations.get(
                self.available_annotation_ids[0],
            )
        else:
            if annotation_id not in self.available_annotation_ids:
                msg = (
                    f"{annotation_id} not in available_annotation_ids "
                    f"{self.available_annotation_ids}"
                )
                raise ValueError(msg)
            self.now_situation = self.situations.get(annotation_id)
        self.env_task = self.now_situation.confirmed_task
        return self.get_observation(self.situations_step_index), info

    def step(
        self: "Self",
        action: Action,
        **kwargs: Unpack["Mind2WebActionArgs"],
    ) -> "ResponseForEachStep":
        """执行动作.

        Args:
            action (Action): 动作
            **kwargs (WebArenaActionArgs): 动作参数

        Returns:
            observation (dict): An element of the environment's observation_space.
            reward (float) : Amount of reward returned after previous action.
            terminated (bool): Whether the episode has ended.
            truncated (bool): Whether the step limit has been reached.
            info (dict) : Infos.
        """
        terminated = False
        truncated = False
        info = {}
        if (
            self.situations_step_index
            >= len(self.now_situation.action_reprs) - 1
        ):
            msg = (
                "No more steps in the situation "
                f"{self.now_situation.domain}",
            )
            warning(msg)
            terminated = True
        reward = cast(Mind2WebActionCandidate, action(**kwargs)).reward(
            Mind2WebActionCandidate(
                backend_node_id=self.now_situation.actions[  # noqa: SLF001
                    self.situations_step_index
                ]
                ._pos_candidates[0]
                .backend_node_id,
                tag=self.now_situation.actions[  # noqa: SLF001
                    self.situations_step_index
                ]
                ._pos_candidates[0]
                .tag,
                value=self.now_situation.actions[
                    self.situations_step_index
                ].operation.value,
            ),
        )

        self.situations_step_index += 1
        return (
            self.get_observation(self.situations_step_index),
            reward,
            terminated,
            truncated,
            info,
        )

    def get_observation(self: "Self", step: int) -> dict:
        """Get observation for step."""
        return {
            "action_repr": self.now_situation.action_reprs[step],
            "raw_html": self.now_situation.actions[step].raw_html,
            "cleaned_html": self.now_situation.actions[step].cleaned_html,
            "candidates": self.now_situation.actions[step].candidates,
        }
