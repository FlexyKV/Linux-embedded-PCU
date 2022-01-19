import json
from flask import request, Flask, jsonify

app = Flask(__name__)


@app.route('/pcu', methods=['POST'])
def test():
    response = {
        "status": 200,
        "test": "test122223"
    }
    return jsonify(response)


@app.route('/ports', methods=['PUT'])
def put_port_control():
    payload = json.loads(request.get_data())
    return 'empty.'


@app.route('/events', methods=['GET'])
def get_events():
    payload = json.loads(request.get_data())
    return 'empty.'


@app.route('/ports', methods=['GET'])
def get_ports_states():
    return 'empty.'


@app.route('/ports/power', methods=['GET'])
def get_ports_powers():
    return 'empty.'


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8989)
