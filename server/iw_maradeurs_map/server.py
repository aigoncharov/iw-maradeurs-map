from quart import Quart, request
from quart_cors import cors
import logging
import asyncio
import json
from logging.config import dictConfig

dictConfig(
    {
        "version": 1,
        "loggers": {
            "quart.app": {
                "level": "ERROR",
            },
        },
    }
)

logging.basicConfig(level="DEBUG")

app = Quart(__name__)
app = cors(app, allow_origin="*")

# users = {"42": {"id": "42", "position": {"x": 37.35960, "y": 55.69850}}}
users = {"42": {"id": "42", "position": {"x": 0.5, "y": 0.5}}}

sensors = {
    "MARADEUR1": {
        "x": 37.35950,
        "y": 55.69854,
    },
    "MARADEUR2": {
        "x": 37.35962,
        "y": 55.69854,
    },
    "MARADEUR3": {
        "x": 37.35958,
        "y": 55.69844,
    },
}

# sensors = [
#     {
#         "id": "MARADEUR1",
#         "position": {"x": 37.35950, "y": 55.69854},
#     },
#     {
#         "id": "MARADEUR2",
#         "position": {"x": 37.35962, "y": 55.69854},
#     },
#     {
#         "id": "MARADEUR3",
#         "position": {"x": 37.35958, "y": 55.69844},
#     },
# ]

running_task = None
cnt = 0
eps = 0.00001


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
    logging.debug(f"{json.dumps(users)}")
    # logging.debug("GET /users")
    # logging.debug("UPDATE POSITION !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
    users_list = [users[id] for id in users]
    return {"users": users_list}


# @app.route("/map")
# async def map_get():
#     logging.debug("GET /map")
#     return {"sensors": sensors}


@app.route("/location", methods=["POST"])
async def location_post():
    # logging.debug("POST /location")
    data = await request.get_json()
    logging.debug(f"POST /location -> data {json.dumps(data)}")
    sensors_signal = adjust_data(data["sensors"])
    location_x, location_y = triangulate(sensors_signal)
    if location_x is not None and location_y is not None:
        # if (
        #     abs(location_x - users["42"]["position"]["x"]) > eps
        #     or abs(location_y - users["42"]["position"]["y"]) > eps
        # ):
        #     logging.warning(f"FOUND NEW POSITION x {str(location_x)}")
        #     logging.warning(f"FOUND NEW POSITION y {str(location_y)}")

        # users["42"]["position"] = {
        #     "x": location_x,
        #     "y": location_y,
        # }
        update_location(location_x, location_y)
    return "", 204

def update_location(x, y):
    x_min = None
    x_max = None
    y_min = None
    y_max = None
    for beacon in sensors:
        if x_min is None:
            x_min = sensors[beacon]['x']
            x_max = sensors[beacon]['x']
            y_min = sensors[beacon]['y']
            y_max = sensors[beacon]['y']
            continue
        x_min = min(x_min, sensors[beacon]['x'])
        x_max = max(x_max, sensors[beacon]['x'])
        y_min = min(y_min, sensors[beacon]['y'])
        y_max = max(y_max, sensors[beacon]['y'])
    # x_min -= 0.00002
    # x_min += 0.00002
    # y_min -= 0.00003
    # y_max += 0.00003
    
    new_x = (x - x_min) / (x_max - x_min)
    new_y = (y - y_min) / (y_max - y_min)
    users["42"]["position"] = {
        "x": new_x,
        "y": new_y,
    }

def adjust_data(signals):
    for i in range(len(signals)):
        idx = signals[i]["id"]
        signals[i]["x"] = sensors[idx]["x"]
        signals[i]["y"] = sensors[idx]["y"]
    return signals


def get_distance(signal):
    return signal + 128


def triangulate(signals):
    if len(signals) < 3:
        return None, None

    signals.sort(key=lambda x: -x["signal"])
    # return signals[0]['x'], signals[0]['y']

    x1 = signals[0]["x"]
    y1 = signals[0]["y"]
    dist1 = get_distance(signals[0]["signal"]) ** 5

    x2 = signals[1]["x"]
    y2 = signals[1]["y"]
    dist2 = get_distance(signals[1]["signal"]) ** 5

    if len(signals) == 2:
        coef1 = dist2 / (dist1 + dist2)
        coef2 = dist1 / (dist1 + dist2)
        res_x1 = x1 * coef1 + x2 * coef2
        res_y1 = y1 * coef1 + y2 * coef2
        return res_x1, res_y1

    x3 = signals[2]["x"]
    y3 = signals[2]["y"]
    dist3 = get_distance(signals[2]["signal"]) ** 5

    coef1 = dist2 / (dist1 + dist2)
    coef2 = dist1 / (dist1 + dist2)
    res_x1 = x1 * coef1 + x2 * coef2
    res_y1 = y1 * coef1 + y2 * coef2
    # logging.debug(f"ZHOPA {coef1}, {coef2}")

    coef1 = dist3 / (dist2 + dist3)
    coef2 = dist2 / (dist2 + dist3)
    res_x2 = x2 * coef1 + x3 * coef2
    res_y2 = y2 * coef1 + y3 * coef2
    # logging.debug(f"ZHOPA {coef1}, {coef2}")

    coef1 = dist3 / (dist1 + dist3)
    coef2 = dist1 / (dist1 + dist3)
    res_x3 = x1 * coef1 + x3 * coef2
    res_y3 = y1 * coef1 + y3 * coef2
    # logging.debug(f"ZHOPA {coef1}, {coef2}")

    res_x = (res_x1 + res_x2 + res_x3) / 3
    res_y = (res_y1 + res_y2 + res_y3) / 3
    # logging.debug(f"FINAL X {res_x1}, {res_x2}, {res_x3}, {res_x}")
    # logging.debug(f"FINAL Y {res_y1}, {res_y2}, {res_y3}, {res_y}")
    return res_x, res_y
