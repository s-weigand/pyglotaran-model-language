from abc import ABC
from typing import Literal

from pydantic import Extra
from pydantic import Field

from pyglotaran_model_language.label_types import ParameterLabel
from pyglotaran_model_language.model_item_base import ModelItemBase
from pyglotaran_model_language.utils.doc_strings import format_literal_to_md_list_items

KnownIrfTypes = Literal[
    "multi-gaussian", "gaussian", "spectral-gaussian", "spectral-multi-gaussian"
]

IRF_TYPE_DESCRIPTION = (
    f"Type of the IRF. \nPossible values are: {format_literal_to_md_list_items(KnownIrfTypes)}"
)


class IrfBase(ModelItemBase, ABC):
    """Base class for Irf implementations."""

    type: KnownIrfTypes

    shift: list[ParameterLabel] | None = Field(
        None,
        description="List of relative shift parameter labels for each gaussian component.",
    )
    normalize: bool = Field(
        True, description="Whether or not to normalize the IRF to an area of one."
    )
    backsweep: bool = Field(False, description="Whether or not to apply backsweep to the IRF.")
    backsweep_period: ParameterLabel | None = Field(
        None,
        description="Period of the Backsweep (only applied if ``backsweep`` is ``True``).",
    )

    @property
    def parameter_labels(self) -> set[ParameterLabel]:
        labels = {*self.shift} if self.shift is not None else set()
        if self.backsweep_period is not None:
            labels.add(self.backsweep_period)
        return labels


class IrfGaussian(IrfBase, extra=Extra.forbid):
    """Instrument Response Function (IRF) consisting of a single gaussian."""

    type: Literal["gaussian"] = Field(description=IRF_TYPE_DESCRIPTION)

    center: ParameterLabel = Field(description="Center positions of the gaussian.")
    width: ParameterLabel = Field(description="Width of the gaussian.")

    @property
    def parameter_labels(self) -> set[ParameterLabel]:
        return {*super().parameter_labels, self.center, self.width}


class IrfMultiGaussian(IrfBase, extra=Extra.forbid):
    """Instrument Response Function (IRF) consisting of a super position of multiple gaussian's."""

    type: KnownIrfTypes = Field("multi-gaussian", description=IRF_TYPE_DESCRIPTION)

    center: list[ParameterLabel] = Field(
        alias="centers",
        description="List of center position parameter labels for each gaussian component.",
    )
    width: list[ParameterLabel] = Field(
        alias="widths",
        description="List of width parameter labels for each gaussian component.",
    )
    scale: list[ParameterLabel] | None = Field(
        None,
        alias="scales",
        description="List of relative scale parameter labels for each gaussian component.",
    )
    # Deprecations
    _deprecated_center: list[ParameterLabel] | None = Field(
        None,
        alias="center",
        exclude=True,
        description="List of center position parameter labels for each gaussian component.",
        deprecated=True,
        deprecationMessage="DEPRECATED: Please use ``centers`` instead.",
    )
    _deprecated_width: list[ParameterLabel] | None = Field(
        None,
        alias="width",
        exclude=True,
        description="List of width parameter labels for each gaussian component.",
        deprecated=True,
        deprecationMessage="DEPRECATED: Please use ``widths`` instead.",
    )
    _deprecated_scale: list[ParameterLabel] | None = Field(
        None,
        alias="scale",
        exclude=True,
        description="List of relative scale parameter labels for each gaussian component.",
        deprecated=True,
        deprecationMessage="DEPRECATED: Please use ``scales`` instead.",
    )

    @property
    def parameter_labels(self) -> set[ParameterLabel]:
        labels = {*super().parameter_labels, *self.center, *self.width}
        if self.scale is not None:
            labels |= {*self.scale}
        return labels


class _SpectralIrfMixin(ModelItemBase):
    dispersion_center: ParameterLabel = Field(
        description="Center positions of the dispersion on the global axis."
    )
    center_dispersion_coefficients: list[ParameterLabel] = Field(
        description="Center positions of the dispersion."
    )
    width_dispersion_coefficients: list[ParameterLabel] = Field(
        description="Center positions of the dispersion."
    )
    model_dispersion_with_wavenumber: bool = Field(
        False, description="Whether to . Defaults to False"
    )

    @property
    def parameter_labels(self) -> set[ParameterLabel]:
        return {
            self.dispersion_center,
            *self.center_dispersion_coefficients,
            *self.width_dispersion_coefficients,
        }


class IrfSpectralGaussian(IrfGaussian, _SpectralIrfMixin, extra=Extra.forbid):
    type: KnownIrfTypes = Field("spectral-gaussian", description=IRF_TYPE_DESCRIPTION)


class IrfSpectralMultiGaussian(IrfGaussian, _SpectralIrfMixin, extra=Extra.forbid):
    type: KnownIrfTypes = Field("spectral-multi-gaussian", description=IRF_TYPE_DESCRIPTION)
