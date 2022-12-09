from typing import Literal

from pydantic import Extra
from pydantic import Field

from pyglotaran_model_language.model_item_base import ModelItemBase


class DatasetGroup(ModelItemBase, extra=Extra.forbid):
    residual_function: Literal["variable_projection", "non_negative_least_squares"] = Field(
        "variable_projection", description="The residual function to use."
    )
    link_clp: None | bool = Field(None, description="Whether to link the clp parameter.")
