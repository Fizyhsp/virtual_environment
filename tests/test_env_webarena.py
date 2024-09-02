"""测试webarena环境."""
from lawen.envs.webarena import WebArenaEnv


def test_env_webarena() -> None:
    """测试webarena环境."""
    env = WebArenaEnv(
        config_file="data/config_example.json",
        current_viewport_only=True,
        env_type="static",
        headless=False,
        name="webarena",
        observation_type="accessibility_tree",
        viewport_size={"width": 1280, "height": 720},
    )
    env.reset()
    obs, reward, terminated, truncated, info = env.step("click")
    assert not terminated
    assert not truncated
    assert reward < 1
