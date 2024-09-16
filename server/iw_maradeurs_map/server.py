from quart import Quart
import logging

logging.basicConfig(level="DEBUG")

app = Quart(__name__)

users = {"42": {"id": "42", "position": None}}
sensors = [{"id": "tbd1"}, {"id": "tbd2"}, {"id": "tbd3"}]


@app.route("/users")
async def users_get():
    logging.debug("GET /users")
    users_list = [user for user in users]
    return {"users": users_list}


@app.route("/map")
async def map_get():
    logging.debug("GET /map")
    return {"sensors": sensors}
