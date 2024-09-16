from quart import Quart
import logging

logging.basicConfig(level="DEBUG")

app = Quart(__name__)


@app.route("/")
async def root():
    logging.debug("GET /root %s", bool(client.qr_code_url))

    if client.qr_code_url is not None:
        qr_code_image = get_qr_code_image(client.qr_code_url)
        return await render_template("qr_code.html", qr_code=qr_code_image)

    feeds = await Feed.all()
    logging.debug("GET /root -> feeds %s", len(feeds))

    return await render_template("feeds.html", user=client.user, feeds=feeds)
