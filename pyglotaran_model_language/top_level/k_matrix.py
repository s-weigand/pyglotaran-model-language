from typing import TypeAlias
from typing import cast

from pydantic import Extra
from pydantic import Field

from pyglotaran_model_language.label_types import CompartmentLabel
from pyglotaran_model_language.label_types import ParameterLabel
from pyglotaran_model_language.model_item_base import ModelItemBase

T_MatrixElement: TypeAlias = dict[tuple[CompartmentLabel, CompartmentLabel], ParameterLabel]


class MatrixElement(ModelItemBase, extra=Extra.forbid):
    """Matrix element in to-from-notation."""

    __root__: T_MatrixElement = Field(
        description=(
            "Mapping of matrix entry positions in to-from-notation of compartment labels"
            " to parameter labels."
        )
    )

    @property
    def compartment_labels(self) -> set[CompartmentLabel]:
        labels = set()
        self_dict = cast(T_MatrixElement, self.dict())
        for to_compartment, from_compartment in self_dict:
            labels |= {to_compartment, from_compartment}
        return labels

    @property
    def parameter_labels(self) -> set[ParameterLabel]:
        return set(self.dict().values())


class KMatrix(ModelItemBase):
    """Kinetic matrix."""

    matrix: MatrixElement

    @property
    def compartment_labels(self) -> set[CompartmentLabel]:
        return self.matrix.compartment_labels

    @property
    def parameter_labels(self) -> set[ParameterLabel]:
        return self.matrix.parameter_labels
