from quart import Quart, request
from quart_cors import cors
import logging

logging.basicConfig(level="DEBUG")

app = Quart(__name__)
app = cors(app, allow_origin="*")

users = {"42": {"id": "42", "position": None}}
sensors = [
    {"id": "tbd1", "position": {"x": 37.35950, "y": 55.69854}},
    {"id": "tbd2", "position": {"x": 37.35962, "y": 55.69854}},
    {"id": "tbd3", "position": {"x": 37.35958, "y": 55.69844}},
]


@app.route("/users")
async def users_get():
    logging.debug("GET /users")
    users_list = [user for user in users]
    return {"users": users_list}


@app.route("/map")
async def map_get():
    logging.debug("GET /map")
    return {"sensors": sensors}


@app.route("/location", methods=["POST"])
async def location_post():
    logging.debug("POST /location")
    data = await request.get_json()
    sensors_signal = data["sensors"]
    triangulate(sensors_signal)
    return None, 204


def triangulate(sensors_signal):
    pass
