"""Tests for ``pyglotaran_model_language.utils.doc_strings``."""

from collections.abc import Iterable
from textwrap import dedent
from typing import Literal

import pytest
from pydantic import BaseModel
from pydantic import Field

from pyglotaran_model_language.utils.doc_strings import add_discriminator_values_to_docstring
from pyglotaran_model_language.utils.doc_strings import format_as_md_list_items
from pyglotaran_model_language.utils.doc_strings import format_literal_to_md_list_items


@pytest.mark.parametrize(
    "items, expected",
    (
        pytest.param(("foo", "bar"), "\n * foo\n * bar", id="tuple"),
        pytest.param(["foo", "bar"], "\n * foo\n * bar", id="list"),
        pytest.param({"foo": 1, "bar": 1}, "\n * foo\n * bar", id="dict"),
        pytest.param(iter(("foo", "bar")), "\n * foo\n * bar", id="generator"),
    ),
)
def test_format_as_md_list_items(items: Iterable[str], expected: str):
    """Formatting works with different kinds of iterables."""
    assert format_as_md_list_items(items) == expected


def test_format_literal_to_md_list_items():
    """Values are extracted from literal."""
    assert format_literal_to_md_list_items(Literal["foo", "bar"]) == "\n * foo\n * bar"


def test_add_discriminator_values_to_docstring():
    """Discriminator values are only added when the root element uses ``discriminator``."""

    class Base(BaseModel):
        disc: Literal["foo", "bar"]

    class Foo(Base):
        disc: Literal["foo"]

    class Bar(Base):
        disc: Literal["bar"]

    @add_discriminator_values_to_docstring
    class FooBar(BaseModel):
        """Could be instance of ``Foo`` or ``Bar``."""

        __root__: Foo | Bar = Field(discriminator="disc")

    expected = dedent(
        """\
        Could be instance of ``Foo`` or ``Bar``.

        Possible values for 'disc' are:
         * foo
         * bar"""
    )

    assert FooBar.__doc__ == expected

    @add_discriminator_values_to_docstring
    class NotRoot(BaseModel):
        """The ``not_root`` be instance of ``Foo`` or ``Bar``."""

        not_root: Foo | Bar = Field(discriminator="disc")

    assert NotRoot.__doc__ == "The ``not_root`` be instance of ``Foo`` or ``Bar``."

    @add_discriminator_values_to_docstring
    class NoDiscriminator(BaseModel):
        """NoDiscriminator"""

        not_root: Foo | Bar = Field()

    assert NoDiscriminator.__doc__ == "NoDiscriminator"
