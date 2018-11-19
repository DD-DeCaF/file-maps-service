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

from flask import abort, g, make_response
from flask_apispec import (
    FlaskApiSpec, MethodResource, doc, marshal_with, use_kwargs)
from sqlalchemy.orm import load_only
from sqlalchemy.orm.exc import NoResultFound

from .jwt import jwt_require_claim, jwt_required
from .models import Map as MapModel
from .models import db
from .schemas import Map, MapListFilter


@doc(description="List all the maps available")
class Maps(MethodResource):
    @use_kwargs(MapListFilter)
    @marshal_with(Map(many=True, exclude=('map',)), code=200)
    def get(self, model_id=None):
        maps = MapModel.query.options(load_only(
            MapModel.id,
            MapModel.project_id,
            MapModel.name,
            MapModel.model_id,
        )).filter(
            MapModel.project_id.in_(g.jwt_claims['prj']) |  # noqa: W504
            MapModel.project_id.is_(None)
        )
        if model_id:
            maps = maps.filter(MapModel.model_id == model_id)
        return maps.all()

    @use_kwargs(Map(exclude=('id',)))
    @marshal_with(None, code=201)
    @marshal_with(None, code=401)
    @marshal_with(None, code=403)
    @jwt_required
    def post(self, project_id, name, model_id, map):
        jwt_require_claim(project_id, 'write')
        db.session.add(MapModel(
            project_id=project_id,
            name=name,
            model_id=model_id,
            map=map,
        ))
        db.session.commit()
        return make_response('', 201)


@doc(description="Map resource")
class Map(MethodResource):
    @marshal_with(Map, code=200)
    @marshal_with(None, code=404)
    def get(self, map_id):
        try:
            return MapModel.query.filter(
                MapModel.id == map_id
            ).filter(
                MapModel.project_id.in_(g.jwt_claims['prj']) |  # noqa: W504
                MapModel.project_id.is_(None)
            ).one()
        except NoResultFound:
            abort(404, f"Cannot find map with id {map_id}")

    @marshal_with(None, code=204)
    @marshal_with(None, code=401)
    @marshal_with(None, code=403)
    @marshal_with(None, code=404)
    @jwt_required
    def delete(self, map_id):
        try:
            map = MapModel.query.filter(
                MapModel.id == map_id
            ).filter(
                MapModel.project_id.in_(g.jwt_claims['prj']) |  # noqa: W504
                MapModel.project_id.is_(None)
            ).one()
        except NoResultFound:
            abort(404, f"Cannot find map with id {map_id}")
        else:
            jwt_require_claim(map.project_id, 'admin')
            db.session.delete(map)
            db.session.commit()
            return make_response('', 204)


def init_app(app):
    """Register API resources on the provided Flask application."""
    def register(path, resource):
        app.add_url_rule(path, view_func=resource.as_view(resource.__name__))
        docs.register(resource, endpoint=resource.__name__)

    docs = FlaskApiSpec(app)
    register("/maps", Maps)
    register("/maps/<int:map_id>", Map)
