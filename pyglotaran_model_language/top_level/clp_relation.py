from pydantic import Extra
from pydantic import Field

from pyglotaran_model_language.label_types import CompartmentLabel
from pyglotaran_model_language.label_types import ParameterLabel
from pyglotaran_model_language.model_item_base import ModelItemBase


class ClpRelation(ModelItemBase, extra=Extra.forbid):
    """Applies a relation between two clps.

    The relation is applied as :math:`target = parameter * source`.
    """

    source: CompartmentLabel = Field(description="")
    target: CompartmentLabel = Field(description="")
    parameter: ParameterLabel = Field(description="")
    interval: tuple[float, float] | list[tuple[float, float]] | None = Field(
        None,
        description=(
            "Interval/s the ClpRelation should be applied to. "
            "If omitted it applies to the full data range."
        ),
    )

    @property
    def compartment_labels(self) -> set[CompartmentLabel]:
        return {self.source, self.target}

    @property
    def parameter_labels(self) -> set[ParameterLabel]:
        return {self.parameter}
