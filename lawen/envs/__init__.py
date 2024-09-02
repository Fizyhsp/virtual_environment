"""环境."""
from lawen.utils import Config

from .basic import Action, ActionSpace, WebEnv

__all__ = [
    "Action",
    "ActionSpace",
    "WebEnv",
]
if Config.USE_MINIWOB:
    from .miniwob import MiniWoBEnv

    __all__ += ["MiniWoBEnv"]
if Config.USE_MIND2WEB:
    from .mind2web import Mind2WebEnv

    __all__ += ["Mind2WebEnv"]
if Config.USE_WEBARENA:
    from .webarena import WebArenaEnv

    __all__ += ["WebArenaEnv"]
