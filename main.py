""""""
from flask import Flask, render_template, request
from locations import create_map, followers_coordinates, get_friends_locations

app = Flask(__name__)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/map_app", methods=["POST"])
def map_app():
    user_name = request.form.get("Screen_Name")
    user_token = request.form.get("Bearer_Token")
    if not user_token or not user_name:
        return render_template("failure.html")

    return render_template("followers_map.html")


@app.route('/errors_found')
def errors_found():
    return render_template("error.html")


if __name__ == "__main__":
    app.run(debug=False)
