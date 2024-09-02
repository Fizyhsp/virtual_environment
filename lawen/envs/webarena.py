"""webarena环境."""
from dataclasses import dataclass
from functools import cached_property, singledispatchmethod
from pathlib import Path
from typing import TYPE_CHECKING, Literal

from marshmallow.fields import Float, Integer, String
from marshmallow.validate import URL, OneOf, Range
from typing_extensions import Unpack

from lawen.utils import make_instance
from webarena.browser_env import ScriptBrowserEnv
from webarena.browser_env.actions import (
    create_check_action,
    create_click_action,
    create_focus_action,
    create_focus_and_click_action,
    create_focus_and_type_action,
    create_go_back_action,
    create_go_forward_action,
    create_goto_url_action,
    create_hover_action,
    create_key_press_action,
    create_keyboard_type_action,
    create_mouse_click_action,
    create_mouse_hover_action,
    create_new_tab_action,
    create_none_action,
    create_page_close_action,
    create_page_focus_action,
    create_scroll_action,
    create_select_option_action,
    create_stop_action,
    create_type_action,
)
from webarena.browser_env.constants import RolesType

from .basic import Action, ActionSpace, WebEnv

if TYPE_CHECKING:
    from typing_extensions import Self

    from lawen.utils.types import (
        ResponseForEachStep,
        ResponseForReset,
        WebArenaActionArgs,
        WebArenaOptions,
    )


@dataclass
class WebArenaActionSpace(ActionSpace):
    """webarena Action空间."""

    @cached_property
    def none(self: "Self") -> Action:
        """无操作."""

        def func() -> dict:
            return create_none_action()

        return make_instance(
            cls=Action,
            name="none",
            func=func,
            description="No-op",
            input_args_schema={},
        )

    @cached_property
    def check(self: "Self") -> Action:
        """check."""

        def func(pw_code: str) -> dict:
            return create_check_action(pw_code)

        return make_instance(
            cls=Action,
            name="check",
            func=func,
            description="check",
            input_args_schema={"pw_code": str},
        )

    @cached_property
    def click(self: "Self") -> Action:
        """click."""

        def func(
            element_id: str = "",
            element_role: RolesType = "link",
            element_name: str = "",
            pw_code: str = "",
            nth: int = 0,
        ) -> dict:
            return create_click_action(
                element_id=element_id,
                element_role=element_role,
                element_name=element_name,
                pw_code=pw_code,
                nth=nth,
            )

        return make_instance(
            cls=Action,
            name="click",
            func=func,
            description="click",
            input_args_schema={
                "element_id": str,
                "element_role": String(validate=OneOf(RolesType.__args__)),
                "element_name": str,
                "pw_code": str,
                "nth": Integer(validate=Range(min=0)),
            },
        )

    @cached_property
    def focus(self: "Self") -> Action:
        """focus."""

        def func(
            element_role: RolesType,
            element_name: str = "",
            nth: int = 0,
        ) -> dict:
            return create_focus_action(
                element_role=element_role,
                element_name=element_name,
                nth=nth,
            )

        return make_instance(
            cls=Action,
            name="focus",
            func=func,
            description="focus",
            input_args_schema={
                "element_role": String(validate=OneOf(RolesType.__args__)),
                "element_name": str,
                "nth": Integer(validate=Range(min=0)),
            },
        )

    @cached_property
    def focus_and_click(self: "Self") -> Action:
        """focus_and_click."""

        def func(
            element_role: RolesType,
            element_name: str = "",
            nth: int = 0,
        ) -> dict:
            return create_focus_and_click_action(
                element_role=element_role,
                element_name=element_name,
                nth=nth,
            )

        return make_instance(
            cls=Action,
            name="focus_and_click",
            func=func,
            description="focus_and_click",
            input_args_schema={
                "element_role": String(validate=OneOf(RolesType.__args__)),
                "element_name": str,
                "nth": Integer(validate=Range(min=0)),
            },
        )

    @cached_property
    def focus_and_type(self: "Self") -> Action:
        """focus_and_type."""

        def func(
            keys: list[int | str] | str,
            element_role: RolesType,
            element_name: str = "",
            nth: int = 0,
        ) -> dict:
            return create_focus_and_type_action(
                keys=keys,
                element_role=element_role,
                element_name=element_name,
                nth=nth,
            )

        return make_instance(
            cls=Action,
            name="focus_and_type",
            func=func,
            description="focus_and_type",
            input_args_schema={
                "keys": list[int | str] | str,
                "element_role": String(validate=OneOf(RolesType.__args__)),
                "element_name": str,
                "nth": Integer(validate=Range(min=0)),
            },
        )

    @cached_property
    def go_back(self: "Self") -> Action:
        """go_back."""

        def func() -> dict:
            return create_go_back_action()

        return make_instance(
            cls=Action,
            name="go_back",
            func=func,
            description="go_back",
            input_args_schema={},
        )

    @cached_property
    def go_forward(self: "Self") -> Action:
        """go_forward."""

        def func() -> dict:
            return create_go_forward_action()

        return make_instance(
            cls=Action,
            name="go_forward",
            func=func,
            description="go_forward",
            input_args_schema={},
        )

    @cached_property
    def goto_url(self: "Self") -> Action:
        """goto_url."""

        def func(url: str) -> dict:
            return create_goto_url_action(url=url)

        return make_instance(
            cls=Action,
            name="goto_url",
            func=func,
            description="goto_url",
            input_args_schema={"url": String(validate=URL())},
        )

    @cached_property
    def hover(self: "Self") -> Action:
        """hover."""

        def func(
            element_id: str = "",
            element_role: RolesType = "link",
            element_name: str = "",
            pw_code: str = "",
            nth: int = 0,
        ) -> dict:
            return create_hover_action(
                element_id=element_id,
                element_role=element_role,
                element_name=element_name,
                pw_code=pw_code,
                nth=nth,
            )

        return make_instance(
            cls=Action,
            name="hover",
            func=func,
            description="hover",
            input_args_schema={
                "element_id": str,
                "element_role": String(validate=OneOf(RolesType.__args__)),
                "element_name": str,
                "pw_code": str,
                "nth": Integer(validate=Range(min=0)),
            },
        )

    @cached_property
    def key_press(self: "Self") -> Action:
        """key_press."""

        def func(key_comb: str) -> dict:
            return create_key_press_action(key_comb=key_comb)

        return make_instance(
            cls=Action,
            name="key_press",
            func=func,
            description="key_press",
            input_args_schema={"key_comb": str},
        )

    @cached_property
    def keyboard_type(self: "Self") -> Action:
        """keyboard_type."""

        def func(keys: list[int | str] | str) -> dict:
            return create_keyboard_type_action(keys=keys)

        return make_instance(
            cls=Action,
            name="keyboard_type",
            func=func,
            description="keyboard_type",
            input_args_schema={"keys": list[int | str] | str},
        )

    @cached_property
    def mouse_click(self: "Self") -> Action:
        """mouse_click."""

        def func(left: float | None = None, top: float | None = None) -> dict:
            return create_mouse_click_action(left=left, top=top)

        return make_instance(
            cls=Action,
            name="mouse_click",
            func=func,
            description="mouse_click",
            input_args_schema={
                "left": Float(validate=Range(min=0)),
                "top": Float(validate=Range(min=0)),
            },
        )

    @cached_property
    def mouse_hover(self: "Self") -> Action:
        """mouse_hover."""

        def func(left: float | None = None, top: float | None = None) -> dict:
            return create_mouse_hover_action(left=left, top=top)

        return make_instance(
            cls=Action,
            name="mouse_hover",
            func=func,
            description="mouse_hover",
            input_args_schema={
                "left": Float(validate=Range(min=0)),
                "top": Float(validate=Range(min=0)),
            },
        )

    @cached_property
    def new_tab(self: "Self") -> Action:
        """new_tab."""

        def func() -> dict:
            return create_new_tab_action()

        return make_instance(
            cls=Action,
            name="new_tab",
            func=func,
            description="new_tab",
            input_args_schema={},
        )

    @cached_property
    def page_close(self: "Self") -> Action:
        """page_close."""

        def func() -> dict:
            return create_page_close_action()

        return make_instance(
            cls=Action,
            name="page_close",
            func=func,
            description="page_close",
            input_args_schema={},
        )

    @cached_property
    def page_focus(self: "Self") -> Action:
        """page_focus."""

        def func(page_number: int) -> dict:
            return create_page_focus_action(page_number=page_number)

        return make_instance(
            cls=Action,
            name="page_focus",
            func=func,
            description="page_focus",
            input_args_schema={"page_number": Integer(validate=Range(min=0))},
        )

    @cached_property
    def scroll(self: "Self") -> Action:
        """scroll."""

        def func(direction: Literal["up", "down"]) -> dict:
            return create_scroll_action(direction=direction)

        return make_instance(
            cls=Action,
            name="scroll",
            func=func,
            description="scroll",
            input_args_schema={
                "direction": String(validate=OneOf(["up", "down"]))
            },
        )

    @cached_property
    def select_option(self: "Self") -> Action:
        """select_option."""

        def func(pw_code: str) -> dict:
            return create_select_option_action(pw_code=pw_code)

        return make_instance(
            cls=Action,
            name="select_option",
            func=func,
            description="select_option",
            input_args_schema={"pw_code": str},
        )

    @cached_property
    def stop(self: "Self") -> Action:
        """stop."""

        def func(answer: str) -> dict:
            return create_stop_action(answer=answer)

        return make_instance(
            cls=Action,
            name="stop",
            func=func,
            description="stop",
            input_args_schema={"answer": str},
        )

    @cached_property
    def type(self: "Self") -> Action:
        """type."""

        def func(
            text: str,
            element_id: str = "",
            element_role: RolesType = "link",
            element_name: str = "",
            pw_code: str = "",
            nth: int = 0,
        ) -> dict:
            return create_type_action(
                text=text,
                element_id=element_id,
                element_role=element_role,
                element_name=element_name,
                pw_code=pw_code,
                nth=nth,
            )

        return make_instance(
            cls=Action,
            name="type",
            func=func,
            description="type",
            input_args_schema={
                "text": str,
                "element_id": str,
                "element_role": String(validate=OneOf(RolesType.__args__)),
                "element_name": str,
                "pw_code": str,
                "nth": Integer(validate=Range(min=0)),
            },
        )

    @cached_property
    def actions(self: "Self") -> list[Action]:
        """所有Action."""
        return [
            self.none,
            self.check,
            self.click,
            self.focus,
            self.focus_and_click,
            self.focus_and_type,
            self.go_back,
            self.go_forward,
            self.goto_url,
            self.hover,
            self.key_press,
            self.keyboard_type,
            self.mouse_click,
            self.mouse_hover,
            self.new_tab,
            self.page_close,
            self.page_focus,
            self.scroll,
            self.select_option,
            self.stop,
            self.type,
        ]


class WebArenaEnv(WebEnv):
    """webarena环境."""

    def __init__(
        self: "Self",
        *,
        config_file: str,
        env_task: str | None = None,
        env_type: str,
        name: str,
        **options: Unpack["WebArenaOptions"],
    ) -> None:
        """初始化."""
        self.config_file = config_file
        self.env_task = env_task
        self.env_type = env_type
        self.name = name
        self.action_space = WebArenaActionSpace()
        self.situations = ScriptBrowserEnv(**options)

    def reset(
        self: "Self",
        config_file: str | None = None,
    ) -> "ResponseForReset":
        """重置.

        Args:
            config_file (str, optional): 配置文件. Defaults to None.

        Returns:
            observation (dict): An element of the environment's observation_space.
            info (dict) : Infos.
        """
        file_path = config_file or self.config_file
        if not Path(file_path).exists():
            msg = f"{file_path} not found"
            raise FileNotFoundError(msg)
        return self.situations.reset(options={"config_file": file_path})

    @singledispatchmethod
    def step(
        self: "Self",
        action: "str|Action",
        **kwargs: Unpack["WebArenaActionArgs"],
    ) -> "ResponseForEachStep":
        """执行动作.

        Args:
            action (str|Action): 动作/动作名称
            kwargs (dict): 动作参数

        Returns:
            observation (dict): An element of the environment's observation_space.
            reward (float) : Amount of reward returned after previous action.
            terminated (bool): Whether the episode has ended.
            truncated (bool): Whether the step limit has been reached.
            info (dict) : Infos.
        """

    @step.register(str)
    def _(
        self: "Self",
        action: str,
        **kwargs: Unpack["WebArenaActionArgs"],
    ) -> "ResponseForEachStep":
        """执行动作.

        Args:
            action (str): 动作名称
            kwargs (dict): 动作参数

        Returns:
            observation (dict): An element of the environment's observation_space.
            reward (float) : Amount of reward returned after previous action.
            terminated (bool): Whether the episode has ended.
            truncated (bool): Whether the step limit has been reached.
            info (dict) : Infos.
        """
        return self.situations.step(
            action=self.action_space.get(action_name=action)(**kwargs),
        )

    @step.register(Action)
    def _(
        self: "Self",
        action: Action,
        **kwargs: Unpack["WebArenaActionArgs"],
    ) -> "ResponseForEachStep":
        """执行动作.

        Args:
            action (Action): 动作
            kwargs (dict): 动作参数

        Returns:
            observation (dict): An element of the environment's observation_space.
            reward (float) : Amount of reward returned after previous action.
            terminated (bool): Whether the episode has ended.
            truncated (bool): Whether the step limit has been reached.
            info (dict) : Infos.
        """
        return self.situations.step(action.func(**kwargs))

    def close(self: "Self") -> None:
        """关闭."""
        self.situations.close()
