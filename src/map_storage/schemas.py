# Copyright (c) 2018, Novo Nordisk Foundation Center for Biosustainability,
# Technical University of Denmark.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import json

from marshmallow import Schema, fields, ValidationError

from jsonschema import ValidationError as JSONSchemaValidationError
from jsonschema import validate


class StrictSchema(Schema):
    class Meta:
        strict = True


class MapListFilter(StrictSchema):
    model_id = fields.Integer(
        required=False,
        description="ID of an optional model to filter by",
    )


class EscherMap(fields.Field):
    """
    Custom field for the escher map.

    The field is not changed on deserialization (it remains a dict structure),
    but it's validated against the escher json schema.
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        with open("jsonschema/1-0-0") as file_:
            self._escher_schema = json.load(file_)

    def _deserialize(self, value, attr, data):
        try:
            validate(value, self._escher_schema)
        except JSONSchemaValidationError as error:
            raise ValidationError(error.message)
        else:
            return value


class Map(StrictSchema):
    id = fields.Integer(required=True)
    project_id = fields.Integer(required=True)
    name = fields.String(required=True)
    model_id = fields.Integer(required=True)
    map = EscherMap(required=True)
