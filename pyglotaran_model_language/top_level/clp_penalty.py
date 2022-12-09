from abc import ABC
from typing import Literal

from pydantic import BaseModel
from pydantic import Extra
from pydantic import Field

from pyglotaran_model_language.label_types import CompartmentLabel
from pyglotaran_model_language.label_types import ParameterLabel
from pyglotaran_model_language.model_item_base import ModelItemBase
from pyglotaran_model_language.utils.doc_strings import add_discriminator_values_to_docstring
from pyglotaran_model_language.utils.doc_strings import format_literal_to_md_list_items

KnownClpPenaltyTypes = Literal["equal_area"]

CLP_PENALTY_TYPE_DESCRIPTION = (
    "Type of the Clp Constraint. \n"
    f"Possible values are: {format_literal_to_md_list_items(KnownClpPenaltyTypes)}"
)


class ClpPenaltyBase(ModelItemBase, ABC, extra=Extra.forbid):
    """Baseclass for clp penalties."""

    type: KnownClpPenaltyTypes
    target: CompartmentLabel = Field(
        description="Label of the compartment the constraint should be applied to."
    )

    @property
    def compartment_labels(self) -> set[CompartmentLabel]:
        return {self.target}


class EqualAreaPenalty(ClpPenaltyBase, extra=Extra.forbid):
    """Forces the area of 2 clp to be the same.

    An equal area constraint adds a the difference of the sum of a
    compartments in the e matrix in one or more intervals to the scaled sum
    of the e matrix of one or more target compartments to residual. The additional
    residual is scaled with the weight.
    """

    type: KnownClpPenaltyTypes = Field(
        "equal_area", const=True, description=CLP_PENALTY_TYPE_DESCRIPTION
    )
    source: CompartmentLabel = Field(description="")
    source_intervals: list[tuple[float, float]] = Field(description="")
    target_intervals: list[tuple[float, float]] = Field(description="")
    parameter: ParameterLabel = Field(description="")
    weight: float = Field(description="")

    @property
    def compartment_labels(self) -> set[CompartmentLabel]:
        return {self.source, *super().compartment_labels}

    @property
    def parameter_labels(self) -> set[ParameterLabel]:
        return {self.parameter}


@add_discriminator_values_to_docstring
class ClpPenalty(BaseModel):
    """Additional penalty that should be applied to during optimization."""

    __root__: EqualAreaPenalty = Field(description=str(EqualAreaPenalty.__doc__))
