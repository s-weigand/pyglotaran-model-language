from pydantic import Extra
from pydantic import Field

from pyglotaran_model_language.label_types import CompartmentLabel
from pyglotaran_model_language.label_types import ParameterLabel
from pyglotaran_model_language.model_item_base import ModelItemBase


class InitialConcentration(ModelItemBase, extra=Extra.forbid):
    """An initial concentration describes the population of the compartments at
    the beginning of an experiment."""

    compartments: list[CompartmentLabel] = Field(description="")
    parameters: list[ParameterLabel] = Field(description="")
    exclude_from_normalize: list[CompartmentLabel] = Field(
        default_factory=list,
        description="List of compartment labels which should be excluded from normalization.",
    )

    @property
    def compartment_labels(self) -> set[CompartmentLabel]:
        return set(self.compartments)

    @property
    def parameter_labels(self) -> set[ParameterLabel]:
        return set(self.parameters)
