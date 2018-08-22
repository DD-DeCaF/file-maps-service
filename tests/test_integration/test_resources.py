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


def test_list(client):
    response = client.get('/list')
    assert response.status_code == 200


def test_model_success(client):
    response = client.get('/model?model=iMM904')
    assert response.status_code == 200


def test_map_success(client):
    response = client.get('/map?map=e_coli_core.Core metabolism.json')
    assert response.status_code == 200


def test_model_fail(client):
    response = client.get('/model?model=ass')
    assert response.status_code == 400


def test_map_success(client):
    response = client.get('/map?map=e_coli_core.Core fail.json')
    assert response.status_code == 400

