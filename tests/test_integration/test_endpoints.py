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


def test_get_maps(client, session, map_fixtures):
    response = client.get("/maps")
    assert response.status_code == 200
    assert len(response.json) > 0


def test_get_maps_filtered(client, session, map_fixtures):
    response = client.get("/maps?model=iMM904")
    assert response.status_code == 200
    assert len(response.json) > 0


def test_get_maps_filtered_not_found(client, session, map_fixtures):
    response = client.get("/maps?model_id=404")
    assert response.status_code == 200
    assert len(response.json) == 0


def test_get_map(client, session, map_fixtures):
    """Test if the response of /map is 200."""
    response = client.get(f"/maps/{map_fixtures[0].id}")
    assert response.status_code == 200


def test_get_map_not_found(client, session, map_fixtures):
    """Test if the response of /map is 404."""
    response = client.get("/maps/404")
    assert response.status_code == 404
