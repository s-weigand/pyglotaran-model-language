from abc import ABC
from typing import Literal

from pydantic import BaseModel
from pydantic import Extra
from pydantic import Field

from pyglotaran_model_language.label_types import CompartmentLabel
from pyglotaran_model_language.model_item_base import ModelItemBase
from pyglotaran_model_language.utils.doc_strings import add_discriminator_values_to_docstring
from pyglotaran_model_language.utils.doc_strings import format_literal_to_md_list_items

KnownClpConstraintTypes = Literal["zero", "only"]

CLP_CONSTRAINT_TYPE_DESCRIPTION = (
    "Type of the ClpConstraint. \n"
    f"Possible values are: {format_literal_to_md_list_items(KnownClpConstraintTypes)}"
)


class ClpConstraintBase(ModelItemBase, ABC, extra=Extra.forbid):
    """Baseclass for clp constraints."""

    type: KnownClpConstraintTypes
    target: CompartmentLabel = Field(
        description="Label of the compartment the constraint should be applied to."
    )
    interval: tuple[float, float] | list[tuple[float, float]] | None = Field(
        None,
        description=(
            "Interval/s the ClpConstraint should be applied to. "
            "If omitted it applies to the full data range."
        ),
    )

    @property
    def compartment_labels(self) -> set[CompartmentLabel]:
        return {self.target}


class ZeroConstraint(ClpConstraintBase, extra=Extra.forbid):
    """Constraints the target to 0 in the given interval."""

    type: KnownClpConstraintTypes = Field(
        "zero", const=True, description=CLP_CONSTRAINT_TYPE_DESCRIPTION
    )


class OnlyConstraint(ClpConstraintBase, extra=Extra.forbid):
    """Constraints the target to 0 outside the given interval."""

    type: KnownClpConstraintTypes = Field(
        "only", const=True, description=CLP_CONSTRAINT_TYPE_DESCRIPTION
    )


@add_discriminator_values_to_docstring
class ClpConstraint(BaseModel):
    """Instrument Response Function (IRF)."""

    __root__: ZeroConstraint | OnlyConstraint = Field(discriminator="type")
