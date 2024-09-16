from iw_maradeurs_map.server import app


def main():
    app.run(debug=True, host="0.0.0.0", port=3042)
