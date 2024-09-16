from quart import Quart
import logging

logging.basicConfig(level="DEBUG")

app = Quart(__name__)

users = {"42": {"id": "42", "position": None}}


@app.route("/users")
async def users_get():
    logging.debug("GET /users %s")
    users_list = [user for user in users]
    return {"users": users_list}
