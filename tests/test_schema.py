"""Test schema."""
from importlib.util import find_spec

from marshmallow.fields import Integer

from lawen.envs.basic import Action
from lawen.utils.schema import Schema, dump_instance, make_instance


class TestSchema(Schema):
    """Test schema."""

    __test__ = False
    a = Integer()


def test_schema() -> None:
    """Test schema."""
    if find_spec("orjson"):
        assert TestSchema().opts.render_module.__name__ == "orjson"
    elif find_spec("ujson"):
        assert TestSchema().opts.render_module.__name__ == "ujson"
    else:
        assert TestSchema().opts.render_module.__name__ == "json"
    assert TestSchema().load({"a": 1}) == {"a": 1}
    assert TestSchema().dump({"a": 1}) == {"a": 1}


def test_make_instance() -> None:
    """Test make_instance."""
    assert make_instance(Action, name="test", description="test").name == "test"


def test_dump_instance() -> None:
    """Test dump_instance."""
    assert dump_instance(
        Action,
        Action(name="test", description="test"),
        only={"name", "description"},
    ) == {
        "name": "test",
        "description": "test",
    }
