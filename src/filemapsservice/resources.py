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

from flask import abort, jsonify, request
from flask_restplus import Resource

from . import storage
from .app import api


class List(Resource):
    """List all the maps availables."""

    @api.doc(params={})
    def get(self):
        """List all the maps availables."""
        # Exclude `map_data` field
        maps = [{
            'map': map_['map'],
            'model': map_['model'],
            'name': map_['name'],
        } for map_ in storage.MAPS]
        return jsonify(maps)


class Map(Resource):
    """Return the map."""

    @api.doc(params={'map': 'Full name of the map with extension'})
    def get(self):
        """Return the map."""
        for map_ in storage.MAPS:
            if map_['map'] == request.args['map']:
                return jsonify(map_['map_data'])
        else:
            abort(404, f"Cannot find map {request.args['map']}")


class Model(Resource):
    """List all the maps availables for a model."""

    @api.doc(params={'model': 'Full name of the model'})
    def get(self):
        """List all the maps availables for a model."""
        # Filter by provided model, and exclude `map_data` field
        maps = [{
            'map': map_['map'],
            'model': map_['model'],
            'name': map_['name'],
        } for map_ in storage.MAPS if map_['model'] == request.args['model']]
        return jsonify(maps)
