import json
from flask import Flask, request, jsonify
from .operations import check_fluid_level, pour_selected_pump, sound_buzzer, \
    display_sense_hat_msg_success, display_sense_hat_msg_failure

from .sql import read_SQL_table

config = {


}

app = Flask(__name__)


@app.route('/')
def hello():
    return "Hardware Server OK"


@app.route('/pourPump', methods=['POST'])
def pourPump():
    data = json.loads(request.data)  # type: ignore
    pump_num = int(data['pump'])
    if (pump_num < 1 or pump_num > 4):
        return "Pump number not in range", 400
    pour_time = int(data['time'])
    pour_selected_pump(pump_num, pour_time)
    return {'status': 'OK', str(pump_num): str(pour_time) + ' seconds'}


@app.route('/checkLevel', methods=['POST'])
def checkLevel():
    data = json.loads(request.data)  # type: ignore
    pump_num = int(data['pump'])
    if (pump_num < 1 or pump_num > 4):
        return "Pump number not in range", 400
    level = check_fluid_level(pump_num)
    return {'status': 'OK', 'distance': str(level), 'units': ' mm'}


@app.route('/soundBuzzer', methods=['GET', 'POST'])
def callSoundBuzzer():
    print("Playing buzzer")
    sound_buzzer()
    return {'status': 'OK'}


@app.route('/showSenseHatSuccess', methods=['POST'])
def showSenseHatSuccess():
    display_sense_hat_msg_success()
    return {'status': 'OK'}


@app.route('/showSenseHatFailure', methods=['POST'])
def showSenseHatFailure():
    display_sense_hat_msg_failure()
    return {'status': 'OK'}


@app.route('/get_SQL_table/<severity>', methods=['GET'])
def get_table(severity):
    '''
    READ local SQL table
    severity: INFO, WARN, or ERROR
    '''
    response = read_SQL_table(severity)
    return jsonify(response)
