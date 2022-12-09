"""Docstring creation/manipulation utility functions."""
from collections.abc import Iterable
from typing import TypeVar
from typing import _LiteralGenericAlias  # type:ignore[attr-defined]
from typing import get_args

from pydantic import BaseModel

Cls = TypeVar("Cls", bound=type[BaseModel])


def format_as_md_list_items(items: Iterable[str]) -> str:
    """Format ``items`` into a markdown list string.

    Parameters
    ----------
    items: Iterable[str]
        Items to be formatted.

    Returns
    -------
    str
    """
    delimiter = "\n * "
    return f"{delimiter}{delimiter.join(items)}"


def format_literal_to_md_list_items(literal: _LiteralGenericAlias) -> str:
    """Creates Markdown list items from a ``Literal`` type.

    Parameters
    ----------
    literal: _LiteralGenericAlias
        ``Literal`` type to extract values from.

    Returns
    -------
    str
        Markdown string listing the values of ``literal``.
    """
    return format_as_md_list_items(get_args(literal))


def add_discriminator_values_to_docstring(cls: Cls) -> Cls:
    """Adds possible values of ``__root__`` field with ``discriminator`` to the docstring.

    Parameters
    ----------
    cls: Cls
        Class to update the docstring for.

    Returns
    -------
    Cls
        Original class with updated docstring.
    """
    if cls.__custom_root_type__ is True:
        root = cls.__fields__["__root__"]
        if root.discriminator_key is not None and root.sub_fields_mapping is not None:
            cls.__doc__ = (
                f"{cls.__doc__}\n\n"
                f"Possible values for {root.discriminator_key!r} are:"
                f"{format_as_md_list_items(root.sub_fields_mapping)}"
            )

    return cls
