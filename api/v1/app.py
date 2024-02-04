#!/usr/bin/python3
""""""
import os
from flask import Flask, jsonify, make_response
from flask_cors import CORS
from models import storage
from api.v1.views import app_views

app = Flask(__name__)
app.url_map.strict_slashes = False
cors = CORS(app, resources={r"/*": {"origins": "0.0.0.0"}})


@app.teardown_appcontext
def teardown(self):
    """Closes storage"""
    storage.close()


@app.errorhandler(404)
def not_found(error):
    """404 error"""
    return make_response(jsonify({"error": "Not found"}), 404)


app.register_blueprint(app_views)

if __name__ == "__main__":
    host = os.getenv("HBNB_API_HOST", default="0.0.0.0")
    port = os.getenv("HBNB_API_PORT", default=5000)
    app.run(debug=True, host=host, port=port, threaded=True)
