"""测试prompt模块."""
from lawen.prompts import AgentPrompt


def test_prompt_template() -> None:
    """测试prompt模块."""
    ap = AgentPrompt.from_file("prompts/templates/baseline_agent.txt")
    assert isinstance(ap.input_variables, list)
    assert all(isinstance(i, str) for i in ap.input_variables)
