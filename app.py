#!/usr/bin/env python
# Copyright (c) {{cookiecutter.year}}, Novo Nordisk Foundation Center for Biosustainability,
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
import os
from flask import Flask, jsonify, request

app = Flask(__name__, static_url_path='/static')
SITE_ROOT = os.path.realpath(os.path.dirname(__file__))


@app.route("/list", methods=['GET'])
def list():
    json_url = os.path.join(SITE_ROOT, 'static/maps')
    return jsonindir(json_url)


@app.route("/map", methods=['GET'])
def map():
    mapname = request.args.get('map')
    json_url = os.path.join(SITE_ROOT, 'static/maps')
    return jsonindir(json_url, mapname)


@app.route("/model", methods=['GET'])
def model():
    modelname = request.args.get('model')
    json_url = os.path.join(SITE_ROOT, 'static/maps/' + modelname)
    return jsonindir(json_url)


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
    return jsonify(jsonlist)


if __name__ == '__main__':
    app.run()
