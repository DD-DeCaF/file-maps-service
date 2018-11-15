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

"""Implement RESTful API endpoints using resources."""

from flask import abort, jsonify
from flask_apispec import (
    FlaskApiSpec, MethodResource, doc, marshal_with, use_kwargs)

from . import storage
from .schemas import MapsRequest


@doc(description="List all the maps available")
class Maps(MethodResource):
    @use_kwargs(MapsRequest)
    def get(self, model=None):
        # Exclude `map_data` field
        maps = [{
            'map': map_['map'],
            'model': map_['model'],
            'name': map_['name'],
        } for map_ in storage.MAPS]
        if model:
            maps = [m for m in maps if m['model'] == model]
        return jsonify(maps)


@doc(description="Map resource")
class Map(MethodResource):
    @marshal_with(None, code=200)
    @marshal_with(None, code=404)
    def get(self, map_name):
        for map_ in storage.MAPS:
            if map_['map'] == map_name:
                return jsonify(map_['map_data'])
        else:
            abort(404, f"Cannot find map {map_name}")


def init_app(app):
    """Register API resources on the provided Flask application."""
    def register(path, resource):
        app.add_url_rule(path, view_func=resource.as_view(resource.__name__))
        docs.register(resource, endpoint=resource.__name__)

    docs = FlaskApiSpec(app)
    register("/maps", Maps)
    register("/maps/<string:map_name>", Map)
