#!/usr/bin/python3
""""""
from api.v1.views import app_views
from flask import jsonify, abort, make_response, request
from models import storage
from models.user import User


@app_views.route("/users", methods=["GET"])
def users():
    """Reterive all user objects"""
    users = []
    for user in storage.all("User").values():
        users.append(user.to_dict())
    return jsonify(users)


@app_views.route("/users/<user_id>", methods=["GET"])
def user(user_id):
    """"""
    user = storage.get(User, user_id)
    if user is None:
        abort(404)
    return jsonify(user.to_dict())


@app_views.route("/users/<user_id>", methods=["DELETE"])
def delete_user(user_id):
    """Deletes a User object"""
    user = storage.get(User, user_id)
    if user is None:
        abort(404)
    user.delete()
    storage.save()
    return jsonify({}), 200


@app_views.route("/users", methods=["POST"])
def create_user():
    """Creates a Amenity"""
    user = request.get_json()
    if user is None:
        return make_response(jsonify({'error': 'Not a JSON'}), 400)
    if "email" not in user:
        return make_response(jsonify({'error': 'Missing email'}), 400)
    if "password" not in user:
        return make_response(jsonify({'error': 'Missing password'}), 400)
    user = User(**user)
    user.save()
    return make_response(jsonify(user.to_dict()), 201)


@app_views.route("/users/<user_id>", methods=["PUT"])
def update_user(user_id):
    """Updates a User object"""
    user = storage.get(User, user_id)
    if user is None:
        abort(404)
    user_data = request.get_json()
    if user_data is None:
        return make_response(jsonify({'error': 'Not a JSON'}), 400)
    for key, value in user_data.items():
        if key not in ["id", "email", "created_at", "updated_at"]:
            setattr(user, key, value)
    user.save()
    return jsonify(user.to_dict()), 200
