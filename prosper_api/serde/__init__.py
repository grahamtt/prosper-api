"""Module for serializing and deserializing values into data objects.

Notes:
    1. Needs to be refactored into an external library.
"""

import json
import logging
import typing
from collections import ChainMap
from datetime import date, datetime
from decimal import Decimal
from queue import Empty, Queue
from typing import IO, Callable, Iterable, Union

from prosper_shared.omni_config import Config, SchemaType, config_schema
from schema import Optional

logger = logging.getLogger()

_object_hooks_by_type = {}

_USE_DECIMALS_CONFIG_PATH = "serde.use-decimals"
_PARSE_DATES_CONFIG_PATH = "serde.parse-dates"
_PARSE_ENUMS_CONFIG_PATH = "serde.parse-enums"


@config_schema
def _schema() -> SchemaType:
    return {
        Optional(
            "serde",
            default={"parse-decimals": True, "parse-dates": True, "parse-enums": True},
        ): {
            Optional("use-decimals", default=True): bool,
            Optional("parse-dates", default=True): bool,
            Optional("parse-enums", default=True): bool,
        }
    }


class Serde:
    """Utility class for serializing and deserializing objects based on type annotations."""

    def __init__(
        self, config: Config
    ):  # TODO: Figure out a better way to get the config
        """Get an instance of Serde.

        Args:
            config (Config): The application config
        """
        self._parse_decimals = config.get_as_bool(_USE_DECIMALS_CONFIG_PATH)
        self._parse_dates = config.get_as_bool(_PARSE_DATES_CONFIG_PATH)
        self._parse_enums = config.get_as_bool(_PARSE_ENUMS_CONFIG_PATH)

    def deserialize(
        self, input_val: Union[str, bytes, bytearray, IO[str]], obj_type: type
    ) -> object:
        """Deserialize the given input value into the given type.

        Args:
            input_val (Union[str, bytes, bytearray, IO[str]]): The input value to deserialize.
            obj_type (type): The type desired for the output.

        Returns:
            object: An object of type `obj_type` representing the data in the input.
        """
        func = json.load if isinstance(input_val, IO) else json.loads
        return func(
            input_val,
            parse_float=Decimal if self._parse_decimals else float,
            object_hook=self._get_type_introspecting_object_hook(obj_type),
        )

    def _get_type_introspecting_object_hook(
        self, type_def: type
    ) -> Callable[[dict], object]:
        if type_def in _object_hooks_by_type:
            return _object_hooks_by_type[type_def]

        def object_hook(obj: dict) -> type_def:
            new_obj = {}
            inner_model = self._get_matching_model(obj, type_def)
            if inner_model is None:
                return obj

            inner_annotations = inner_model.__annotations__ if inner_model else {}
            for key, val in obj.items():
                val_type = inner_annotations[key] if key in inner_annotations else None
                # TODO: Handle untyped values
                # if val_type is None:
                #     new_obj[key] = val
                #     logger.warning(
                #         f"Key {key} not found in type annotations for type {inner_model}"
                #     )
                #     continue

                if val_type == Union[str, date]:
                    new_obj[key] = date.fromisoformat(val) if self._parse_dates else val
                    continue

                if val_type == Union[str, datetime]:
                    new_obj[key] = (
                        datetime.strptime(val, "%Y-%m-%d %H:%M:%S %z")
                        if self._parse_dates
                        else val
                    )
                    continue

                if val_type == Union[float, Decimal]:
                    new_obj[key] = val  # Handled by simplejson
                    continue

                if isinstance(val, list):
                    new_obj[key] = val
                    continue

                # if issubclass(val_type, NamedTuple):
                #     new_obj[key] = val  # Will have been parsed and replaced previously
                #     continue

                if hasattr(val_type, "from_value"):
                    new_obj[key] = (
                        val_type.from_value(val_type, val) if self._parse_enums else val
                    )
                    continue

                new_obj[key] = val

            return inner_model(**new_obj) if inner_model else new_obj

        _object_hooks_by_type[type_def] = object_hook
        return object_hook

    def _get_matching_model(self, obj: dict, root_type: type) -> Union[None, type]:
        for model in ModelTreeWalker(root_type):
            if not hasattr(model, "__annotations__"):
                continue

            all_annotations = self._all_annotations(model)

            matches = True
            for key in obj.keys():
                if key not in all_annotations.keys():
                    matches = False
                    logger.debug(f"Prop {key} not found in type {root_type}")
                    break  # pragma: no mutate
            if matches:
                logger.debug(f"Found matching type {model}")
                return model

        logger.warning(f"Matching type not found for {obj}")
        return None

    def _all_annotations(self, cls) -> ChainMap:
        return ChainMap(
            *(c.__annotations__ for c in cls.__mro__ if "__annotations__" in c.__dict__)
        )


class ModelTreeWalker(Iterable):
    """Walks the type tree starting at the given type and emit each unique type found."""

    def __init__(self, root_type: type):
        """Creates a ModelTreeWalker starting with the given root type.

        Args:
            root_type (type): The root of the type tree to iterate through.
        """
        self._type_queue = Queue()
        self._type_queue.put(root_type)
        self._seen = {root_type}

    def __iter__(self):
        """Returns `self`."""
        return self

    def __next__(self) -> type:
        """Get the next type value.

        Pops a value off the queue, puts the types of its fields into the queue, then returns the value.

        Returns:
            type: The next value from the tree.

        Raises:
            StopIteration: When there are no more values.
        """
        try:
            next_type = self._type_queue.get_nowait()
        except Empty:
            raise StopIteration()

        if hasattr(next_type, "__annotations__"):
            for inner_type in next_type.__annotations__.values():
                if hasattr(inner_type, "__origin__") and inner_type.__origin__ in (
                    list,
                    set,
                ):
                    type_params = typing.get_args(inner_type)
                    if len(type_params) > 0:
                        inner_type = type_params[0]

                if inner_type in self._seen:
                    continue
                self._type_queue.put_nowait(inner_type)
                self._seen.add(inner_type)

        return next_type
