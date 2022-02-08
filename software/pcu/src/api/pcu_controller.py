import json
import datetime
import threading
from flask import request, Flask, jsonify
from software.pcu.src.service.pcu_service import PcuService
from software.pcu.src.repository.pcu_repository import PcuRepository
from software.pcu.src.adc.adc_simulator import ADCSimulator

app = Flask(__name__)
db_file_path = r"C:\Users\FlexyFlex\PycharmProjects\Linux-embeded-PCU\software\pcu\PCUDB"

pcu_service_repo = PcuRepository(db_file_path)
pcu_service_repo.create_tables()
pcu_service_repo.create_ports()

pcu_service = PcuService(pcu_service_repo)

# pcu_adc_repo = PcuRepository(db_file_path)
# pcu_adc = ADCSimulator(pcu_adc_repo)
# adc_thread = threading.Thread(target=pcu_adc.launch_simulation, args=(5,))
# adc_thread.start()


@app.route('/pcu', methods=['POST'])
def test():
    response = {
        "status": 200,
        "test": "test122223"
    }
    return jsonify(response)


@app.route('/port_measures', methods=['GET'])
def get_port_measures():
    payload = json.loads(request.get_data())
    return pcu_service.get_port_measures(payload["port_id"], payload["start_time"],
                                         payload["end_time"], payload["period"])


@app.route('/port_state', methods=['GET'])
def get_port_state():
    payload = json.loads(request.get_data())
    return pcu_service.get_port_state(payload["port_id"])


@app.route('/port_state', methods=['PUT'])
def put_port_state():
    payload = json.loads(request.get_data())
    return pcu_service.update_port_state(payload["port_id"], payload["port_state"])


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8989)
