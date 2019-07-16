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

"""Integration tests for resource endpoints."""

from map_storage.models import Map


def test_get_maps(client, session, map_fixtures):
    response = client.get("/maps")
    assert response.status_code == 200
    assert len(response.json) > 0


def test_get_public_maps(client, session, map_fixtures):
    response = client.get("/maps")
    assert all([m['project_id'] is None for m in response.json])


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


def test_post_map(client, session, tokens, ecoli_map):
    response = client.post(
        f"/maps",
        json={
            'project_id': 1,
            'name': "Testmap",
            'model_id': 1,
            'map': ecoli_map,
        },
        headers={
            'Authorization': f"Bearer {tokens['write']}",
        },
    )
    assert response.status_code == 201


def test_post_invalid_map(client, session, tokens):
    response = client.post(
        f"/maps",
        json={
            'project_id': 1,
            'name': "Testmap",
            'model_id': 1,
            'map': {"foo": "bar"},
        },
        headers={'Authorization': f"Bearer {tokens['write']}"},
    )
    assert response.status_code == 422


def test_put_map(client, session, map_fixtures, tokens):
    response = client.put(
        f"/maps/{map_fixtures[1].id}",
        json={'id': 4, 'name': "Changed name"},
        headers={
            'Authorization': f"Bearer {tokens['write']}",
        },
    )
    assert response.status_code == 204

    map = Map.query.filter(Map.id == map_fixtures[1].id).one()
    assert map.name == "Changed name"


def test_delete_map(client, session, map_fixtures, tokens):
    response = client.delete(f"/maps/{map_fixtures[1].id}", headers={
        'Authorization': f"Bearer {tokens['admin']}",
    })
    assert response.status_code == 204
