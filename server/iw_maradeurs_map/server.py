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
        "id": "MARADEUR1",
        "position": {"x": 37.35950, "y": 55.69854},
    },
    {
        "id": "MARADEUR2",
        "position": {"x": 37.35962, "y": 55.69854},
    },
    {
        "id": "MARADEUR3",
        "position": {"x": 37.35958, "y": 55.69844},
    },
]

running_task = None
cnt = 0


@app.before_serving
async def startup():
    global running_task

    async def schedule():
        global running_task
        global cnt

        # if cnt % 4 == 0:
        #     users["42"]["position"]["x"] += 0.00003
        # elif cnt % 4 == 1:
        #     users["42"]["position"]["y"] += 0.00003
        # elif cnt % 4 == 2:
        #     users["42"]["position"]["x"] -= 0.00003
        # elif cnt % 4 == 3:
        #     users["42"]["position"]["y"] -= 0.00003
        # cnt += 1
        await asyncio.sleep(2)

        loop = asyncio.get_event_loop()
        running_task = loop.create_task(schedule())

    loop = asyncio.get_event_loop()
    running_task = loop.create_task(schedule())


@app.after_serving
async def cleanup():
    global running_task
    running_task.cancel()


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
    return "", 204


def triangulate(sensors_signal):
    pass
