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

"""Read and contain maps in memory."""

import json
import logging
import os


MAPS = []
logger = logging.getLogger(__name__)


def init_maps():
    """Read maps from disk into the `storage.MAPS` variable."""
    global MAPS
    logger.debug("Reading maps from disk")
    for map_filename in os.listdir('data/maps'):
        with open(f"data/maps/{map_filename}") as f:
            map_data = json.load(f)
        model_name, map_name, _ = map_filename.split('.')
        MAPS.append({
            'map': map_filename,
            'model': model_name,
            'name': map_name,
            'map_data': map_data,
        })

    # Sort by map name
    MAPS = sorted(MAPS, key=lambda map_: map_['name'])
