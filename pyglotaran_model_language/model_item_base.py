from typing import Any

from pydantic import BaseModel

from pyglotaran_model_language.label_types import CompartmentLabel
from pyglotaran_model_language.label_types import InitialConcentrationLabel
from pyglotaran_model_language.label_types import IrfLabel
from pyglotaran_model_language.label_types import KMatrixLabel
from pyglotaran_model_language.label_types import MegacomplexLabel
from pyglotaran_model_language.label_types import ParameterLabel
from pyglotaran_model_language.label_types import ShapeLabel
from pyglotaran_model_language.label_types import _LabelType


class ModelItemBase(BaseModel):
    """Base class for model items ensuring that they have properties returning all the used labels."""

    def __init_subclass__(cls, **kwargs) -> None:
        _raise_on_missing_property(cls, CompartmentLabel, "compartment_labels")
        _raise_on_missing_property(cls, ParameterLabel, "parameter_labels")
        _raise_on_missing_property(cls, MegacomplexLabel, "megacomplex_labels")
        _raise_on_missing_property(cls, InitialConcentrationLabel, "initial_concentration_labels")
        _raise_on_missing_property(cls, IrfLabel, "irf_labels")
        _raise_on_missing_property(cls, ShapeLabel, "shape_labels")
        _raise_on_missing_property(cls, KMatrixLabel, "kmatrix_labels")
        super().__init_subclass__(**kwargs)

    class Config:
        @staticmethod
        def schema_extra(schema: dict[str, Any], model: type["ModelItemBase"]) -> None:
            for key, val in schema.get("properties", {}).items():
                if key == "type":
                    # val.pop("default", None)
                    required_fields = schema.get("required", [])
                    if "type" not in required_fields:
                        schema["required"] = ["type", *required_fields]


def _raise_on_missing_property(
    cls: type[ModelItemBase], label_type: type[_LabelType], property_name: str
) -> None:
    if label_type.__name__ in repr(cls.__annotations__.values()) and not isinstance(
        getattr(cls, property_name, None),
        property,
    ):
        raise NotImplementedError(
            f"The class {cls.__name__} uses ``{label_type.__name__}``/-s,"
            f" but does not have a ``{property_name}`` property."
        )
    setattr(cls, property_name, property(set))
