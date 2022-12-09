from abc import ABC
from abc import abstractclassmethod
from typing import Literal

from pydantic import Extra
from pydantic import Field

from pyglotaran_model_language.label_types import CompartmentLabel
from pyglotaran_model_language.label_types import KMatrixLabel
from pyglotaran_model_language.label_types import ParameterLabel
from pyglotaran_model_language.model_item_base import ModelItemBase
from pyglotaran_model_language.utils.doc_strings import add_discriminator_values_to_docstring
from pyglotaran_model_language.utils.doc_strings import format_literal_to_md_list_items

KnownShapeTypes = Literal[
    "decay",
    "decay-parallel",
    "decay-sequential",
    "damped-oscillation",
    "spectral",
    "coherent-artifact",
    "baseline",
    "clp-guide",
]

SHAPE_TYPE_DESCRIPTION = (
    "Type of the Shape. \n"
    f"Possible values are: {format_literal_to_md_list_items(KnownShapeTypes)}"
)


class ShapeBase(ModelItemBase, ABC, extra=Extra.forbid):
    """Baseclass for Megacomplexes."""

    type: KnownShapeTypes


class SpectralShapeGaussian(ShapeBase, extra=Extra.forbid):
    """Baseclass for Megacomplexes."""

    type: KnownShapeTypes = Field("gaussian", const=True, description=SHAPE_TYPE_DESCRIPTION)
    amplitude: ParameterLabel | None = Field(None, description="")
    location: ParameterLabel = Field(description="")
    width: ParameterLabel = Field(description="")

    @property
    def parameter_labels(self) -> set[ParameterLabel]:
        labels = {self.location, self.width}
        if self.amplitude is not None:
            labels |= {self.amplitude}
        return labels
