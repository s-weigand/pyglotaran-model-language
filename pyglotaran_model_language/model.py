from pydantic import BaseModel
from pydantic import Field

from pyglotaran_model_language.builtin.megacomplex import KnownMegacomplexTypes
from pyglotaran_model_language.label_types import DatasetLabel
from pyglotaran_model_language.label_types import IrfLabel
from pyglotaran_model_language.label_types import KMatrixLabel
from pyglotaran_model_language.top_level.clp_constraint import ClpConstraint
from pyglotaran_model_language.top_level.clp_penalty import ClpPenalty
from pyglotaran_model_language.top_level.clp_relation import ClpRelation
from pyglotaran_model_language.top_level.dataset import DataSet
from pyglotaran_model_language.top_level.irf import Irf
from pyglotaran_model_language.top_level.k_matrix import KMatrix


class Model(BaseModel):
    """pyglotaran model"""

    default_megacomplex: KnownMegacomplexTypes | None = Field(
        None,
        description="Megacomplex 'type' which is used when not defined on the megacomplex itself.",
    )
    irf: dict[IrfLabel, Irf] | None = Field(
        None,
        description=str(Irf.__doc__),
    )
    dataset: dict[DatasetLabel, DataSet] = Field(
        ...,
        description=str(DataSet.__doc__),
    )
    k_matrix: dict[KMatrixLabel, KMatrix] | None = Field(
        None,
        description=str(KMatrix.__doc__),
    )
    clp_penalties: list[ClpPenalty] | None = Field(
        None,
        description=str(ClpPenalty.__doc__),
    )
    clp_constraints: list[ClpConstraint] | None = Field(
        None, description=str(ClpConstraint.__doc__)
    )
    clp_relations: list[ClpRelation] | None = Field(
        None,
        description=str(ClpRelation.__doc__),
    )
    # deprecated
    # clp_area_penalties


if __name__ == "__main__":
    import json
    from pathlib import Path

    from pydantic import schema_json_of
    from rich import print_json

    schema_test = Path("test_schema.json")

    json_schema_str = schema_json_of(Model, title="Model", indent=2)
    schema_test.write_text(json_schema_str, encoding="utf8")

    schema_test.write_text(json.dumps(Model.schema(), indent=2), encoding="utf8")

    from pyglotaran_model_language.utils.schema_post_processing.yaml import (
        update_schema_definitions_yaml,
    )

    update_schema_definitions_yaml(schema_test)
    print_json(schema_test.read_text(encoding="utf8"))
