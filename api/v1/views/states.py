#!/usr/bin/python3
""""""
from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage
from models.state import State


@app_views.route("/states", methods=['GET'])
def states():
    """Reterive state objects"""
    state = [obj.to_dict() for obj in storage.all('State').values()]
    return jsonify(state)


@app_views.route('/states/<state_id>', methods=['GET'])
def states_id(state_id):
    """Reterive state objects"""
    state = storage.get('State', state_id)
    if state is None:
        abort(404)
    else:
        return jsonify(state.to_dict())


@app_views.route('/states/<state_id>',
                 methods=['DELETE'])
def delete_state(state_id):
    """Delete state objects"""
    state = storage.get('State', state_id)
    if state is None:
        abort(404)
    else:
        state.delete()
        storage.save()
        return jsonify({}), 200


@app_views.route('/states', methods=['POST'])
def create_state():
    """Create a new state objects"""
    if not request.get_json():
        return jsonify({"error": "Not a JSON"}), 400
    elif "name" not in request.get_json():
        return jsonify({"error": "Missing name"}), 400
    else:
        data = request.get_json()
        obj = State(**data)
        obj.save()
        return jsonify(obj.to_dict()), 201


@app_views.route('/states/<state_id>', methods=['PUT'])
def update_state(state_id):
    """Update a state objects"""
    if not request.get_json():
        return jsonify({"error": "Not a JSON"}), 400
    state = storage.get('State', state_id)
    if state is None:
        abort(404)
    obj_data = request.get_json()
    state.name = obj_data['name']
    state.save()
    return jsonify(state.to_dict()), 200
