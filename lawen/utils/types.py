"""Define types for the package."""
from typing import NamedTuple, TypeAlias, TypedDict, TypeVar

from .config import Config

ARGS = TypeVar("ARGS")
KWARGS = TypeVar("KWARGS")


class ResponseForEachStep(NamedTuple):
    """每步的响应."""

    observation: dict
    reward: float
    terminated: bool
    truncated: bool
    info: dict


class ResponseForReset(NamedTuple):
    """重置的响应."""

    observation: dict
    info: dict


if Config.USE_MINIWOB:
    from miniwob.environment import MiniWoBEnvironment

    class MiniWoBOptions(TypedDict):
        """MiniWoB环境选项."""

        apply_api_compatibility: bool
        autoreset: bool
        disable_env_checker: bool
        env_task: str
        env_type: str
        episode_max_time: int
        episode_max_time: int
        max_episode_steps: int
        name: str
        render_mode: str

    class MiniWoBActionArgs(TypedDict):
        """MiniWoB动作参数."""

        env: MiniWoBEnvironment
        left: float
        top: float
        key: str
        ref: int
        field: int
        text: str


if Config.USE_WEBARENA:

    class WebArenaOptions(TypedDict):
        """webarena环境选项."""

        current_viewport_only: bool
        headless: bool
        observation_type: str
        viewport_size: dict[str, int]
        max_page_length: int
        slow_mo: int
        save_trace_enabled: bool
        sleep_after_execution: int

    class WebArenaActionArgs(TypedDict):
        """webarena动作参数."""

        pw_code: str
        element_id: str
        element_role: str
        element_name: str
        nth: int
        keys: list[int | str] | str
        url: str
        key_comb: str
        left: float
        top: float
        page_number: int
        direction: str
        key: str
        ref: int
        field: int
        text: str


InputActionArgs: TypeAlias = MiniWoBActionArgs | WebArenaActionArgs
