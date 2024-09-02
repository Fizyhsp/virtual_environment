"""This is a simple example of using the SimpleLLMAgent."""
from logging import info

from lawen.agents import SimpleLLMAgent
from lawen.envs.miniwob import MiniWoBEnv

env: MiniWoBEnv = MiniWoBEnv(
    name="miniwob/click-test-2-v1",
    env_type="static",
    render_mode="human",
)
agent = SimpleLLMAgent(
    name="llm_agent",
    env=env,
    api_base="https://api.unopenedai.site/v1",
    api_key="sk-aPeXKSwlwdSq3SJI8d788651E650490bA2982559B22eAb36",
    model_name="gpt-3.5-turbo-0613",
    template="prompts/templates/test.txt",
    task="click-test",
)
try:
    for _ in range(10):
        # Start a new episode.
        obs, infos = env.reset()

        # choose action.
        action, input_action_args = agent.next_action(obs)
        obs, reward, terminated, truncated, infos = env.step(
            action,
            **input_action_args,
        )

        # print info.
        action_info = f"Action: {action.name}, Args: {input_action_args}"
        info(action_info)
        reward_info = f"Reward: {reward}"
        info(reward_info)
        terminated_info = f"Terminated: {terminated}"
        info(terminated_info)
        truncated_info = f"Truncated: {truncated}"
        info(truncated_info)
        infos_info = f"Info: {infos}"
        info(infos_info)

finally:
    env.close()
