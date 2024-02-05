#!/usr/bin/python3
""""""
from api.v1.views import app_views
from flask import jsonify, abort, make_response, request
from models import storage
from models.place import Place
from models.city import City
from models.user import User


@app_views.route("/cities/<city_id>/places", methods=["GET"],
                 strict_slashes=False)
def places(city_id):
    """Retrieves the list of all Place objects of a City"""
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    places = []
    for place in city.places:
        places.append(place.to_dict())
    return jsonify(places)


@app_views.route("/places/<place_id>", methods=["GET"],
                 strict_slashes=False)
def place(place_id):
    """Retrieves a Place object"""
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    return jsonify(place.to_dict())


@app_views.route("/places/<place_id>", methods=["DELETE"],
                 strict_slashes=False)
def delete_place(place_id):
    """Deletes a Place object"""
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    place.delete()
    storage.save()
    return jsonify({}), 200


@app_views.route("/cities/<city_id>/places", methods=["POST"],
                 strict_slashes=False)
def create_place(city_id):
    """"""
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    place = request.get_json()
    if place is None:
        return make_response(jsonify({'error': 'Not a JSON'}), 400)
    if "user_id" not in place:
        return make_response(jsonify({'error': 'Missing user_id'}), 400)
    user = storage.get(User, place["user_id"])
    if user is None:
        abort(404)
    if "name" not in place:
        return make_response(jsonify({'error': 'Missing name'}), 400)
    place["city_id"] = city_id
    place = Place(**place)
    place.save()
    return jsonify(place.to_dict()), 201


@app_views.route("/places/<place_id>", methods=["PUT"],
                 strict_slashes=False)
def update_place(place_id):
    """"""
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    data = request.get_json()
    if data is None:
        return make_response(jsonify({'error': 'Not a JSON'}), 400)
    for key, value in data.items():
        if key not in ["id", "user_id", "city_id", "created_at", "updated_at"]:
            setattr(place, key, value)

    place.save()
    return jsonify(place.to_dict()), 200
