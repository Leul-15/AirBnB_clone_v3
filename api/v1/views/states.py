#!/usr/bin/python3
""""""
from models import storage
from models.state import State
from flask import jsonify, abort, make_response, request
from api.v1.views import app_views


@app_views.route("/states", methods=["GET"])
def get_states():
    """Reterive state objects"""
    states = storage.all(State).values()
    return jsonify([state.to_dict() for state in states])


@app_views.route("/states/<state_id>", methods=["GET"])
def get_state(state_id):
    """Reterive state objects with specified state_id"""
    state = storage.get(State, state_id)
    if state:
        return jsonify(state.to_dict())
    abort(404)


@app_views.route("/states/<state_id>", methods=["DELETE"])
def delete_state(state_id):
    """Deletes a State object"""
    state = storage.get(State, state_id)
    if state:
        storage.delete(state)
        storage.save()
        return jsonify({})
    abort(404)


@app_views.route("/states", methods=["POST"])
def post_state():
    """"""
    if not request.get_json():
        return make_response(jsonify({'error': 'Not a JSON'}), 400)
    if "name" not in request.get_json():
        return make_response(jsonify({'error': 'Missing name'}), 400)
    state = State(**request.get_json())
    storage.new(state)
    storage.save()
    return make_response(jsonify(state.to_dict()), 201)


@app_views.route("/states/<state_id>", methods=["PUT"])
def put_state(state_id):
    """"""
    state = storage.get(State, state_id)
    if not state:
        abort(404)
    if not request.get_json():
        return make_response(jsonify({'error': 'Not a JSON'}), 400)
    for key, value in request.json().items():
        if key not in ["id", "created_at", "updated_at"]:
            setattr(state, key, value)
    storage.save()
    return jsonify(state.to_dict())
