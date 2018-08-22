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

import os
from flask_restplus import Resource, fields
from filemapsservice.app import app
from flask import jsonify,abort, request
from .app import api, app


SITE_ROOT = os.path.realpath(os.path.dirname(__file__))


class List(Resource):
    """List all the maps availables"""
    @api.doc(params={})
    def get(self):
        json_url = os.path.join(SITE_ROOT, 'static/maps')
        result = jsonindir(json_url)
        if not result:
            return abort(400,
                         "No maps were found")
        else:
            return jsonify(result)


class Map(Resource):
    """List all the maps availables"""
    @api.doc(params={'map': 'Full name of the map with extension'})
    def get(self):
        mapname = request.args.get('map')
        json_url = os.path.join(SITE_ROOT, 'static/maps')
        result = jsonindir(json_url, mapname)
        if not result:
            return abort(400,
                         "No maps were found")
        else:
            return jsonify(result)


class Model(Resource):
    """List all the maps availables"""
    @api.doc(params={'model': 'Full name of the model'})
    def get(self):
        modelname = request.args.get('model')
        json_url = os.path.join(SITE_ROOT, 'static/maps/' + modelname)
        result = jsonindir(json_url)
        if not result:
            return abort(400,
                         "No models were found")
        else:
            return jsonify(result)


def jsonindir(dir, mapname=None):
    jsonlist = []
    for root, dirs, files in os.walk(dir):
        for name in files:
            if mapname:
                if mapname == name:
                    json_url = os.path.join(SITE_ROOT, root, mapname)
                    token = open(json_url)
                    stored_json = token.readlines()
                    token.close()
                    return stored_json[0]
            else:
                if name.endswith(".json"):
                    jsonlist.append(name)
    return jsonlist

