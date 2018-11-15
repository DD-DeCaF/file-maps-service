# Copyright 2018 Novo Nordisk Foundation Center for Biosustainability, DTU.
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

"""Integration tests for resource endpoints"""


def test_get_maps(client):
    response = client.get("/maps")
    assert response.status_code == 200
    assert len(response.json) > 0


def test_get_maps_filtered(client):
    response = client.get("/maps?model=iMM904")
    assert response.status_code == 200
    assert len(response.json) > 0


def test_get_maps_filtered_not_found(client):
    response = client.get("/maps?model=404")
    assert response.status_code == 200
    assert len(response.json) == 0


def test_get_map(client):
    """Test if the response of /map is 200."""
    response = client.get("/maps/e_coli_core.Core metabolism.json")
    assert response.status_code == 200


def test_get_map_not_found(client):
    """Test if the response of /map is 404."""
    response = client.get("/maps/404")
    assert response.status_code == 404
