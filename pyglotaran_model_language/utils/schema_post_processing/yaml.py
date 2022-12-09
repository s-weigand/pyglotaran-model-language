import json
from pathlib import Path
from typing import TYPE_CHECKING
from typing import Any

from pydantic import BaseModel
from pydantic import Extra
from pydantic import Field
from pydantic import constr
from pydantic import schema_json_of

from pyglotaran_model_language.label_types import ParameterLabel

# Mypy issue hack Ref.: https://github.com/pydantic/pydantic/issues/156
if TYPE_CHECKING:
    MatrixItem = str
else:
    MatrixItem = constr(regex=r"^\s*\([a-zA-Z_][a-zA-Z0-9_]*\s*,\s*[a-zA-Z_][a-zA-Z0-9_]*\s*\)$")


class MatrixElementYaml(BaseModel, extra=Extra.forbid):
    """Matrix element in to-from-notation."""

    __root__: dict[MatrixItem, ParameterLabel] = Field(
        description="Mapping of matrix entry positions in to-from-notation to parameter labels.",
    )


def matrix_element_yaml_definition() -> dict[str, Any]:
    schema_str = schema_json_of(MatrixElementYaml).replace("MatrixElementYaml", "MatrixElement")
    return json.loads(schema_str)["definitions"]


def update_schema_definitions_yaml(schema_path: Path | str) -> None:
    schema_path = Path(schema_path)
    schema = json.loads(schema_path.read_text(encoding="utf8"))
    definitions = [matrix_element_yaml_definition()]
    for definition in definitions:
        schema["definitions"] |= definition
    schema_path.write_text(json.dumps(schema, indent=2), encoding="utf8")
