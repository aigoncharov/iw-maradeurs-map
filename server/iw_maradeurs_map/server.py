from quart import Quart, request
from quart_cors import cors
import logging
import asyncio

logging.basicConfig(level="DEBUG")

app = Quart(__name__)
app = cors(app, allow_origin="*")

users = {"42": {"id": "42", "position": {"x": 37.35960, "y": 55.69850}}}

sensors = [
    {
        "id": "b6b734c1-1dc5-4d7f-b8da-3def1ee6b530",
        "position": {"x": 37.35950, "y": 55.69854},
    },
    {
        "id": "d24635bf-5843-4086-aaeb-a60c1be948eb",
        "position": {"x": 37.35962, "y": 55.69854},
    },
    {
        "id": "85374a27-6206-4711-bf17-f1066ee3dd7e",
        "position": {"x": 37.35958, "y": 55.69844},
    },
]

running = True


@app.before_serving
async def startup():
    global running

    cnt = 0
    while running:
        if cnt % 4 == 0:
            users["42"]["position"]["x"] += 0.00003
        elif cnt % 4 == 1:
            users["42"]["position"]["y"] += 0.00003
        elif cnt % 4 == 2:
            users["42"]["position"]["x"] -= 0.00003
        elif cnt % 4 == 3:
            users["42"]["position"]["y"] -= 0.00003
        await asyncio.sleep(2)


@app.after_serving
async def cleanup():
    global running

    running = False


@app.route("/users")
async def users_get():
    logging.debug("GET /users")
    users_list = [users[id] for id in users]
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
