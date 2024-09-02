"""测试miniwob环境."""
from time import sleep

from lawen.envs.miniwob import MiniWoBEnv


def test_env_miniwob() -> None:
    """测试miniwob环境."""
    env: MiniWoBEnv = MiniWoBEnv(
        name="miniwob/click-test-2-v1",
        env_type="static",
    )
    try:
        # Start a new episode.
        obs, info = env.reset()
        assert obs["utterance"] == "Click button ONE."
        assert obs["fields"] == (("target", "ONE"),)
        sleep(2)  # Only here to let you look at the environment.

        # Find the HTML element with text "ONE".
        for element in obs["dom_elements"]:
            if element["text"] == "ONE":
                break

        # Click on the element.
        assert isinstance(element["ref"], int)
        obs, reward, terminated, truncated, info = env.step(
            "click_element",
            ref=element["ref"],
        )

        # Check if the action was correct.
        assert reward < 1
        assert terminated is True

    finally:
        env.close()
