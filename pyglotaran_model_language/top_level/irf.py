from pydantic import Field

from pyglotaran_model_language.builtin.irf import IrfGaussian
from pyglotaran_model_language.builtin.irf import IrfMultiGaussian
from pyglotaran_model_language.builtin.irf import IrfSpectralGaussian
from pyglotaran_model_language.builtin.irf import IrfSpectralMultiGaussian
from pyglotaran_model_language.model_item_base import ModelItemBase
from pyglotaran_model_language.utils.doc_strings import add_discriminator_values_to_docstring


@add_discriminator_values_to_docstring
class Irf(ModelItemBase):
    """Instrument Response Function (IRF)."""

    __root__: IrfGaussian | IrfMultiGaussian | IrfSpectralGaussian | IrfSpectralMultiGaussian = (
        Field(..., discriminator="type")
    )
