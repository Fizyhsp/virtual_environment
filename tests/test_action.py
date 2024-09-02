"""Test action."""
from dataclasses import field

import pytest
from marshmallow.fields import Integer
from marshmallow.validate import Range

from lawen.envs import Action


def test_action() -> None:
    """Test action."""
    action = Action(name="test", description="test")
    with pytest.raises(ValueError, match="Action未实现") as excinfo:
        action(a=1)
    assert excinfo.type is ValueError
    assert excinfo.value.args[0] == "Action未实现"

    action = Action(
        name="test",
        description="test",
        func=lambda a: a,
        enable=False,
    )
    with pytest.raises(ValueError, match="Action不可用") as excinfo:
        action(a=1)
    assert excinfo.type is ValueError
    assert excinfo.value.args[0] == "Action不可用"

    action = Action(
        name="test",
        description="test",
        func=lambda a: a,
        input_args_schema={"a": int},
    )
    assert action(a=1) == 1

    with pytest.raises(ValueError, match="参数不合法") as excinfo:
        action(a="a")
    assert excinfo.type is ValueError
    assert excinfo.value.args[0] == "参数不合法"

    action = Action(
        name="test",
        description="test",
        func=lambda a: a,
        input_args_schema={"a": Integer(validate=Range(min=0, max=10))},
    )
    action = Action(
        name="test",
        description="test",
        func=lambda a: a,
        input_args_schema={"a": field(default=1)},
    )
    action = Action(
        name="test",
        description="test",
        func=lambda a: a,
        input_args_schema={"a": field(default_factory=int)},
    )
    action = Action(
        name="test",
        description="test",
        func=lambda a: a,
        input_args_schema={"a": field(default_factory=lambda: 1)},
    )
    action = Action(
        name="test",
        description="test",
        func=lambda a: a,
        input_args_schema={"a": field()},
    )
    action = Action(
        name="test",
        description="test",
        func=lambda a: a,
        input_args_schema={"a": list[int | str] | str},
    )
