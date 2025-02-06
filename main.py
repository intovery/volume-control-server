from flask import Flask, request, jsonify, render_template
import volume as Volume

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("./index.html")

@app.route("/volume/up", methods=["POST"])
def post_volume_up():
    return jsonify({"volume": Volume.volume_up()})

@app.route("/volume/down", methods=["POST"])
def post_volume_down():
    return jsonify({"volume": Volume.volume_down()})

@app.route("/volume", methods=["POST"])
def post_volume():
    data = request.get_json()
    if "volume" not in data:
        return jsonify({"error": "volume parameter required"}), 400
    
    try:
        volume_value = int(data["volume"])
        if Volume.set_volume(volume_value) == True:
            return jsonify({"volume": volume_value})
        else:
            return jsonify({"error": "volume have to be number between 0~100"}), 400
    except ValueError:
        return jsonify({"error": "please enter correct number."}), 400
    
@app.route("/volume/mute", methods=["POST"])
def mute_volume():
    return jsonify({"mute": Volume.mute() })

@app.route("/volume/status", methods=["GET"])
def get_volume_status():
    current_volume, is_muted = Volume.get_volume_status()
    return jsonify({"volume": current_volume, "mute": is_muted})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)