"""测试mind2web环境."""
from pandas import DataFrame

from lawen.agents import RandomAgent
from lawen.envs.mind2web import Mind2WebEnv


def test_mind2web_env() -> None:
    """测试mind2web环境."""
    env: Mind2WebEnv = Mind2WebEnv(
        dataset_path="data/test_domain_9.json",
        name="mind2web_test_1",
        env_type="static",
    )
    assert isinstance(env.action_space.action_names, list)
    agent = RandomAgent(
        name="random_agent",
        env=env,
        task="test",
    )
    assert (
        agent.next_action(env.reset()[0]) in env.action_space.actions
    )
    assert all(
        action in env.action_space.actions
        for action in agent.plan(env.reset()[0])
    )
