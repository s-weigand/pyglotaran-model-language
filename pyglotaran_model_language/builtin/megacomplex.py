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

KnownMegacomplexTypes = Literal[
    "decay",
    "decay-parallel",
    "decay-sequential",
    "damped-oscillation",
    "spectral",
    "coherent-artifact",
    "baseline",
    "clp-guide",
]

MEGACOMPLEX_TYPE_DESCRIPTION = (
    "Type of the Megacomplex. \n"
    f"Possible values are: {format_literal_to_md_list_items(KnownMegacomplexTypes)}"
)


class MegacomplexBase(ModelItemBase, ABC, extra=Extra.forbid):
    """Baseclass for Megacomplexes."""

    type: KnownMegacomplexTypes
    _unique: bool = Field(
        False,
        description=(
            "Whether or not multiple megacomplexes of this "
            "type are allowed in a set of megacomplexes."
        ),
    )
    _exclusive: bool = Field(
        False,
        description=(
            "Whether or not other megacomplexes are allowed besides this type of megacomplex "
            "in a set of megacomplexes."
        ),
    )

    @property
    @abstractclassmethod
    def required_dataset_fields(cls) -> set[str]:
        """Dataset fields which are required by the megacomplex."""


class DecayMegacomplex(MegacomplexBase, extra=Extra.forbid):
    """Megacomplex describing a general exponential decay."""

    type: KnownMegacomplexTypes = Field(
        "decay", const=True, description=MEGACOMPLEX_TYPE_DESCRIPTION
    )
    k_matrix: list[KMatrixLabel] = Field(
        ...,
        description=(
            "List of KMatrixLabels which are used to build the "
            "full Kmatrix for the megacomplex."
        ),
    )

    @property
    def kmatrix_labels(self) -> set[KMatrixLabel]:
        return {*self.k_matrix}


class DecayParallelMegacomplex(MegacomplexBase, extra=Extra.forbid):
    """Megacomplex describing a parallel exponential decay."""

    type: KnownMegacomplexTypes = Field(
        "decay-parallel", const=True, description=MEGACOMPLEX_TYPE_DESCRIPTION
    )
    compartments: list[CompartmentLabel] = Field(
        description=(
            "List of CompartmentLabel which are used to build the Kmatrix for the megacomplex."
        ),
    )
    rates: list[ParameterLabel] = Field(
        description=(
            "List of CompartmentLabel which are used to build the Kmatrix for the megacomplex."
        ),
    )

    @property
    def compartment_labels(self) -> set[CompartmentLabel]:
        return {*self.compartments}

    @property
    def parameter_labels(self) -> set[ParameterLabel]:
        return {*self.rates}


class DecaySequentialMegacomplex(DecayParallelMegacomplex, extra=Extra.forbid):
    """Megacomplex describing a sequential exponential decay."""

    type: KnownMegacomplexTypes = Field(
        "decay-sequential", const=True, description=MEGACOMPLEX_TYPE_DESCRIPTION
    )


class DampedOscillationMegacomplex(MegacomplexBase, extra=Extra.forbid):
    """Megacomplex describing damped oscillations."""

    type: KnownMegacomplexTypes = Field(
        "damped-oscillation", const=True, description=MEGACOMPLEX_TYPE_DESCRIPTION
    )
    labels: list[ParameterLabel] = Field(description="")
    frequencies: list[ParameterLabel] = Field(description="")
    rates: list[ParameterLabel] = Field(description="")

    @property
    def parameter_labels(self) -> set[ParameterLabel]:
        return {*self.labels, *self.frequencies, *self.rates}


class ClpGuideMegacomplex(MegacomplexBase, extra=Extra.forbid):
    """Megacomplex used to guide the optimization for a ``target`` compartment towards a value."""

    type: KnownMegacomplexTypes = Field(
        "clp-guide", const=True, description=MEGACOMPLEX_TYPE_DESCRIPTION
    )
    target: CompartmentLabel = Field(
        description="The label of the compartment the guide applies for."
    )
    _exclusive = True

    @property
    def compartment_labels(self) -> set[CompartmentLabel]:
        return {self.target}


class BaselineMegacomplex(MegacomplexBase, extra=Extra.forbid):
    """Megacomplex describing a baseline/offset of the dataset."""

    type: KnownMegacomplexTypes = Field(
        "baseline", const=True, description=MEGACOMPLEX_TYPE_DESCRIPTION
    )
    _unique = True


class CoherentArtifactMegacomplex(MegacomplexBase, extra=Extra.forbid):
    """Megacomplex describing a coherent artifact."""

    type: KnownMegacomplexTypes = Field(
        "coherent-artifact", const=True, description=MEGACOMPLEX_TYPE_DESCRIPTION
    )
    _unique = True

    order: int = Field(
        le=3,
        ge=1,
        description=(
            "Number of ``IRF`` derivatives to include in the approximation "
            "(needs to be in {1, 2, 3}).\n"
            "* 1 -> 0th derivative\n"
            "* 2 -> 0th and 1st derivative\n"
            "* 3 -> 0th, 1st and 2nd derivative\n"
        ),
    )
    width: ParameterLabel | None = Field(
        None,
        description=(
            "Width of the coherent artifact. "
            "If omitted the first width component of the ``IRF`` is used."
        ),
    )

    @property
    def parameter_labels(self) -> set[ParameterLabel]:
        return {self.width} if self.width is not None else set()
