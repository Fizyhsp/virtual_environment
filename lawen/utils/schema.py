"""工具包."""
from collections.abc import Callable, Sequence
from collections.abc import Set as AbstractSet
from importlib.util import find_spec, module_from_spec
from inspect import isfunction
from typing import (
    TYPE_CHECKING,
    ClassVar,
    Literal,
    TypedDict,
    TypeVar,
    overload,
)

from marshmallow import INCLUDE
from marshmallow import Schema as OriginalSchema
from marshmallow.fields import Field
from marshmallow_dataclass import class_schema
from typing_extensions import Unpack

if TYPE_CHECKING:
    from importlib.machinery import ModuleSpec
    from types import ModuleType

    from envs.basic import Action
    from typing_extensions import Self

    from .types import ARGS, KWARGS

    _C = TypeVar("_C")
    V = TypeVar("V")
spec: "ModuleSpec" = (
    find_spec(name="orjson")
    or find_spec(name="ujson")
    or find_spec(name="json")
)
json: "ModuleType" = module_from_spec(spec=spec)
spec.loader.exec_module(module=json)


class CallableField(Field):
    """Function."""

    default_error_messages: ClassVar[dict[Literal["invalid"], str]] = {
        "invalid": "Not a valid function.",
    }

    def __init__(self: "Self", *args: "ARGS", **kwargs: "KWARGS") -> None:
        """Init."""
        super().__init__(*args, **kwargs)

    def _deserialize(
        self: "Self",
        value: "V",
        _attr: str,
        _obj: object,
    ) -> Callable:
        """Deserialize."""
        if not isfunction(value):
            self.fail(key="invalid")
        return value

    def _serialize(
        self: "Self",
        value: "Callable",
        _attr: str | None,
        _obj: object,
    ) -> str:
        return value.__doc__


class Schema(OriginalSchema):
    """Change default json."""

    TYPE_MAPPING: ClassVar[dict[type, Field]] = {
        Callable: CallableField,
    }

    class Meta:
        """Change default json."""

        render_module = json
        unknown = INCLUDE


class Options(TypedDict):
    """Schema Options."""

    only: Sequence[str] | AbstractSet[str] | None
    exclude: Sequence[str] | AbstractSet[str] | None
    many: bool
    context: dict | None
    load_only: Sequence[str] | AbstractSet[str] | None
    dump_only: Sequence[str] | AbstractSet[str] | None
    partial: bool | Sequence[str] | AbstractSet[str] | None
    unknown: str | None


@overload
def make_instance(
    cls: "Action",
    *,
    description: str,
    enable: bool = True,
    func: Callable | None = None,
    input_args_schema: dict | None = None,
    metadata: list[dict] | None = None,
    name: str,
    options: Options | None = None,
    tags: list[str] | None = None,
) -> "Action":
    ...


def make_instance(
    cls: type["_C"],
    *,
    options: Options | None = None,
    list_data: list[dict] | None = None,
    **data: "KWARGS",
) -> "_C | list[_C]":
    """Make instance.

    Args:
        cls (type of dataclass): dataclass
        options (Options, optional): options for create schema. Defaults to None.
            only (Sequence[str] | Set[str], optional): Whitelist of the declared
            fields to select when instantiating the Schema. If None, all fields are
            used. Nested fieldscan be represented with dot delimiters.
            exclude (Sequence[str] | Set[str], optional): Blacklist of the declared
            fields to exclude when instantiating the Schema. If a field appears in
            both `only` and `exclude`, it is not used. Nested fields can be
            represented with dot delimiters.
            many (bool, optional): Should be set to `True` if ``obj`` is a collection
            so that the object will be serialized to a list.
            context (dict, optional): Optional context passed to :meth:`Schema.load
            <marshmallow.Schema.load>`.
            load_only (Sequence[str] | Set[str], optional): Fields to skip during
            serialization (write-only fields)
            dump_only (Sequence[str] | Set[str] | None): Fields to skip during
            deserialization (read-only fields)
            partial (bool | Sequence[str] | Set[str] | None): Whether to ignore missing
            fields and not require any fields declared. Propagates down to ``Nested``
            fields as well. If its value is an iterable, only missing fields listed in
            that iterable will be ignored. Use dot delimiters to specify nested fields.
            unknown (str | None): Whether to exclude, include, or raise an error for
            unknown fields in the data. Use `EXCLUDE`, `INCLUDE` or `RAISE`.
        list_data (dict, optional): list of data to deserialize
        data (keyword arguments): data to deserialize

    Returns:
        (instance of dataclass) | list[instance of dataclass]: dataclass instance or
        list of dataclass instance
    """
    if options is None:
        options = {}
    return class_schema(clazz=cls, base_schema=Schema)(**options).load(
        data=data if list_data is None else list_data,
        many=list_data is not None,
    )


def dump_instance(
    cls: type["_C"],
    instance: "_C | list[_C]",
    **options: Unpack[Options],
) -> dict | list[dict]:
    """Dump instance.

    Args:
        cls (type[_C]): dataclass
        instance (instance of dataclass | list[instance of dataclass]): dataclass
        instance
        many (bool, optional): dump list or not. Defaults to False.
        options: kwargs for dump schema. Defaults to None.
            only (Sequence[str] | Set[str], optional): Whitelist of the declared
            fields to select when instantiating the Schema. If None, all fields are
            used. Nested fieldscan be represented with dot delimiters.
            exclude (Sequence[str] | Set[str], optional): Blacklist of the declared
            fields to exclude when instantiating the Schema. If a field appears in
            both `only` and `exclude`, it is not used. Nested fields can be
            represented with dot delimiters.
            many (bool, optional): Should be set to `True` if ``obj`` is a collection
            so that the object will be serialized to a list.
            context (dict, optional): Optional context passed to :meth:`Schema.load
            <marshmallow.Schema.load>`.
            load_only (Sequence[str] | Set[str], optional): Fields to skip during
            serialization (write-only fields)
            dump_only (Sequence[str] | Set[str] | None): Fields to skip during
            deserialization (read-only fields)
            partial (bool | Sequence[str] | Set[str] | None): Whether to ignore missing
            fields and not require any fields declared. Propagates down to ``Nested``
            fields as well. If its value is an iterable, only missing fields listed in
            that iterable will be ignored. Use dot delimiters to specify nested fields.
            unknown (str | None): Whether to exclude, include, or raise an error for
            unknown fields in the data. Use `EXCLUDE`, `INCLUDE` or `RAISE`.

    Returns:
        dict | list[dict]: dict data or list of dict data
    """
    return class_schema(clazz=cls, base_schema=Schema)(**options).dump(
        instance,
        many=isinstance(instance, list),
    )
