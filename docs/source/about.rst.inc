**Lawen** is an open-source code library for large-scale model intelligent agents. Its purpose is to provide a simple, user-friendly, and stable research foundation for large-scale model intelligent agents in web environments.

.. code-block:: python

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
        api_base="your-api-base",
        api_key="your-api-key",
        model_name="your-model-name",
        template="prompts/templates/test.txt",
        task="click-test",
        proxy="your-proxy",
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

Get It Now
==========

.. code-block:: bash

    $ # The basic package can be installed with pip
    $ pip install lawen[miniwob, mongodb, mysql, orjson, postgresql, redis, ujson, mind2web, webarena]

    $ # or poetry
    $ poetry add lawen --extras "miniwob mongodb mysql orjson postgresql redis ujson mind2web webarena"
