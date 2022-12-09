from pydantic import Field

from pyglotaran_model_language.label_types import InitialConcentrationLabel
from pyglotaran_model_language.label_types import IrfLabel
from pyglotaran_model_language.label_types import MegacomplexLabel
from pyglotaran_model_language.label_types import ParameterLabel
from pyglotaran_model_language.model_item_base import ModelItemBase


class DataSet(ModelItemBase):
    """Definition of the model specification for a dataset."""

    megacomplex: list[MegacomplexLabel] = Field(
        description="List of megacomplex labels defined in the 'megacomplex' section."
    )
    initial_concentration: InitialConcentrationLabel = Field(
        description="Label of an ``initial_concentration`` in the 'initial_concentrations' section."
    )
    irf: IrfLabel | None = Field(None, description="Label of an ``irf`` in the 'irf' section.")
    scale: ParameterLabel | None = Field(None, description="Relative scale of the dataset.")

    @property
    def parameter_labels(self) -> set[ParameterLabel]:
        return {self.scale} if self.scale is not None else set()

    @property
    def irf_labels(self) -> set[IrfLabel]:
        return {self.irf} if self.irf is not None else set()

    @property
    def initial_concentration_labels(self) -> set[InitialConcentrationLabel]:
        return {self.initial_concentration}

    @property
    def megacomplex_labels(self) -> set[MegacomplexLabel]:
        return {*self.megacomplex}
