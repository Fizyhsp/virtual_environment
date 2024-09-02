"""LLM智能体."""
from ast import literal_eval
from dataclasses import KW_ONLY, dataclass, field
from logging import log, warning
from typing import TYPE_CHECKING

from langchain.chains import LLMChain
from langchain.chat_models import ChatOpenAI

from lawen.prompts import AgentPrompt
from lawen.utils import Config, dump_instance, json, make_instance

from .basic import BasicAgent

if TYPE_CHECKING:
    from envs import Action
    from typing_extensions import Self


@dataclass
class Thought:
    """thought."""

    reasoning: str = field(default="reasoning")
    plan: str = field(
        default="- short bulleted\n- list that conveys\n- long-term plan",
    )
    criticism: str = field(default="constructive self-criticism")


@dataclass
class ActionSchema:
    """ActionSchema."""

    name: str = field(default="action name")
    input_action_args: dict = field(
        default_factory=lambda: {"arg name": "value"},
    )


@dataclass
class OutputFormat:
    """输出格式模式."""

    thoughts: Thought = field(default_factory=Thought)
    action: ActionSchema = field(default_factory=ActionSchema)
    observation: dict = field(init=False)


@dataclass
class SimpleLLMAgent(BasicAgent):
    """LLM智能体."""

    _: KW_ONLY
    api_base: str
    api_key: str
    model_name: str
    template: str
    temperature: float = 0.3
    trajectory: list[dict] = field(default_factory=list)
    trajectory_max_length: int = 5
    output_format: OutputFormat = field(default_factory=OutputFormat)
    proxy: str | None = None

    def __post_init__(self: "Self") -> None:
        """初始化."""
        self.llm = ChatOpenAI(
            temperature=self.temperature,
            openai_api_base=self.api_base,
            openai_api_key=self.api_key,
            openai_proxy=self.proxy,
            model=self.model_name,
        )
        self.prompt: AgentPrompt = AgentPrompt.from_file(
            template_path=self.template,
        )
        self.chain = LLMChain(llm=self.llm, prompt=self.prompt)

        self.actions = self.env.action_space.actions

    def next_action(self: "Self", observation: str) -> tuple["Action", dict]:
        """Predict the next action given the observation."""
        self.output_format.observation = observation
        prompt_variables: dict = dump_instance(
            self.__class__,
            self,
            only=self.prompt.input_variables,
        )
        prompt_info_str = f"Prompt variables: {prompt_variables}"
        log(Config.VERBOSE_LEVEL, prompt_info_str)
        llm_return_str: str = self.chain.run(**prompt_variables)
        return_info_str = f"LLM return: {llm_return_str}"
        log(Config.VERBOSE_LEVEL, return_info_str)
        action, llm_return = self.output_parse(llm_return_str=llm_return_str)

        llm_return.observation = observation
        self.trajectory.append(dump_instance(OutputFormat, llm_return))
        self.trajectory.pop(0) if len(
            self.trajectory,
        ) > self.trajectory_max_length else None
        return (action, llm_return.action.input_action_args)

    def plan(self: "Self", observation: str, steps: int = 3) -> list["Action"]:
        """Plan the actions given the observation."""
        return [self.next_action(observation) for _ in range(steps)]

    def reset(self: "Self") -> None:
        """重置."""
        self.trajectory = []
        self.actions = self.env.action_space.actions
        if self.env.env_task is not None:
            self.task = self.env.env_task
        self.env.reset()

    def output_parse(
        self: "Self",
        llm_return_str: str,
        none_action_name: str = "none",
    ) -> tuple["Action", OutputFormat]:
        """解析LLM返回.

        Args:
            llm_return_str (str): LLM返回
            none_action_name (str, optional): 无动作名称. Defaults to "none".

        Returns:
            (Action, dict): action, llm_return
        """
        try:
            llm_return: OutputFormat = make_instance(
                OutputFormat,
                **literal_eval(
                    llm_return_str.replace("\r", "").replace("\n", ""),
                ),
            )
        except json.JSONDecodeError as e:
            if none_action_name not in self.env.action_space.action_names:
                msg = f"Action {none_action_name} not in action space"
                raise ValueError(msg) from e
            action = self.env.action_space.get(action_name=none_action_name)
            llm_return = OutputFormat()
        else:
            if llm_return.action.name not in self.env.action_space.action_names:
                msg = f"Action {llm_return.action.name} not in action space"
                warning(msg)
                action = self.env.action_space.get(action_name=none_action_name)
            else:
                action: Action = self.env.action_space.get(
                    action_name=llm_return.action.name,
                )
        return action, llm_return

    def set_task(self: "Self", task: str) -> None:
        """设置任务."""
        self.task = task
