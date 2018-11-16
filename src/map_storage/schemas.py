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

from marshmallow import Schema, fields


class StrictSchema(Schema):
    class Meta:
        strict = True


class MapsRequest(StrictSchema):
    model_id = fields.Integer(
        required=False,
        description="ID of an optional model to filter by",
    )


class MapResponse(Schema):
    id = fields.Integer()
    project_id = fields.Integer()
    name = fields.String()
    model_id = fields.Integer()
    map = fields.Raw()
