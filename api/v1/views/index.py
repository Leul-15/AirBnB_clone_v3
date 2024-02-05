#!/usr/bin/python3
""""""
from api.v1.views import app_views
from flask import jsonify
from models import storage
from models.state import State
from models.amenity import Amenity
from models.city import City
from models.place import Place
from models.review import Review
from models.user import User


@app_views.route("/status", methods=["GET"])
def status():
    """"""
    return jsonify({"status": "OK"})


@app_views.route("/stats", methods=["GET"])
def stats():
    """"""
    classes = {
        "amenities": Amenity,
        "cities": City,
        "places": Place,
        "reviews": Review,
        "states": State,
        "users": User,
    }
    return jsonify(
        {key: storage.count(value) for key, value in classes.items()}
    )
