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
from flask import Flask

app = Flask(__name__, static_url_path='/static')


@app.route('/')
def hello_world():
    return 'Hello World!'


@app.route("/json")
def readwrite():
    SITE_ROOT = os.path.realpath(os.path.dirname(__file__))
    json_url = os.path.join(SITE_ROOT, 'static/maps/iJN746', 'iJN746.Central metabolism.json')
    token = open(json_url)
    stored_json = token.readlines()
    token.close()
    return stored_json[0]


if __name__ == '__main__':
    app.run()
