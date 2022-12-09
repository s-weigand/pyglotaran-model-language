"""Module containing types of labels used for a better readability and type checking."""

from typing import NewType
from typing import TypeVar

_LabelType = TypeVar("_LabelType", bound=str)

ParameterLabel = NewType("ParameterLabel", str)
CompartmentLabel = NewType("CompartmentLabel", str)
IrfLabel = NewType("IrfLabel", str)
MegacomplexLabel = NewType("MegacomplexLabel", str)
InitialConcentrationLabel = NewType("InitialConcentrationLabel", str)
DatasetLabel = NewType("DatasetLabel", str)
KMatrixLabel = NewType("KMatrixLabel", str)
ShapeLabel = NewType("ShapeLabel", str)
