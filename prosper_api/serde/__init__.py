import logging
from datetime import date, datetime
from decimal import Decimal
from enum import Enum
from typing import Callable, Union

from prosper_api import models
from prosper_api.config import Config

logger = logging.getLogger()

_object_hooks_by_type = {}

_RETURN_STRINGS_NOT_DATES_CONFIG_PATH = "client.return-strings-not-dates"
_RETURN_STRINGS_NOT_ENUMS_CONFIG_PATH = "client.return-strings-not-enums"


def get_type_introspecting_object_hook(
    type_def: type, config: Config
) -> Callable[[dict], object]:
    """Gets an `object_hook` that can be used with deserializers like `simplejson` to deal with objects.

    Args:
        type_def (type): The type of the object to deserialize
        config (Config): The config for this run

    Returns:
        Callable[[dict], object]: A object hook that can deal with typed objects.
    """
    if type_def in _object_hooks_by_type:
        return _object_hooks_by_type[type_def]

    return_strings_not_dates = config.get_as_bool(_RETURN_STRINGS_NOT_DATES_CONFIG_PATH)
    return_strings_not_enums = config.get_as_bool(_RETURN_STRINGS_NOT_ENUMS_CONFIG_PATH)

    def object_hook(obj: dict) -> type_def:
        new_obj = {}
        inner_model = _get_matching_model(obj)
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
                new_obj[key] = (
                    val if return_strings_not_dates else date.fromisoformat(val)
                )
                continue

            if val_type == Union[str, datetime]:
                new_obj[key] = (
                    str
                    if return_strings_not_dates
                    else datetime.strptime(val, "%Y-%m-%d %H:%M:%S %z")
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

            if issubclass(val_type, Enum):
                new_obj[key] = (
                    val
                    if return_strings_not_enums
                    else val_type._value2member_map_[val]
                )
                continue

            new_obj[key] = val

        return inner_model(**new_obj) if inner_model else new_obj

    _object_hooks_by_type[type_def] = object_hook
    return object_hook


def _get_matching_model(obj: dict) -> type:
    for name, model in models.__dict__.items():
        if not hasattr(model, "__annotations__"):
            continue
        matches = True
        for key in obj.keys():
            if key not in model.__annotations__:
                matches = False
                break  # pragma: no mutate
        if matches:
            return model

    logger.warning(f"Matching type not found for {obj}")
    return None
