import json
from flask import Flask, request, jsonify

from .mock_operations import mock_check_fluid_level, mock_pour_selected_pump, \
    mock_sound_buzzer, mock_display_sense_hat_msg_success, \
    mock_display_sense_hat_msg_failure

app = Flask(__name__)


@app.route('/')
def hello():
    return "Mock Server OK"


@app.route('/mockPourPump', methods=['POST'])
def mock_pour_pump():
    data = json.loads(request.data)
    pump_num = int(data['pump'])
    if (pump_num < 1 or pump_num > 4):
        return "Pump number not in range", 400

    pourTime = int(data['time'])
    mock_pour_selected_pump(pump_num, pourTime)
    return {'status': 'OK', str(pump_num): str(pourTime) + ' seconds'}


@app.route('/mockCheckLevel', methods=['POST'])
def mock_check_level():
    data = json.loads(request.data)
    pump_num = int(data['pump'])
    if (pump_num < 1 or pump_num > 4):
        return "Pump number not in range", 400
    level = mock_check_fluid_level(pump_num)
    return {'status': 'OK', 'distance': level}


@app.route('/mockSoundBuzzer', methods=['GET', 'POST'])
def mock_call_sound_buzzer():
    print("Playing buzzer")
    mock_sound_buzzer()
    return {'status': 'OK'}


@app.route('/mockShowSenseHatSuccess', methods=['POST'])
def mock_show_sense_hat_success():
    mock_display_sense_hat_msg_success()
    return {'status': 'OK'}


@app.route('/mockShowSenseHatFailure', methods=['POST'])
def mock_show_sense_hat_failure():
    mock_display_sense_hat_msg_failure()
    return {'status': 'OK'}


# @app.route('/mock_get_SQL_table/<severity>', methods=['GET'])
# def mock_get_table(severity):
#     '''
#     READ local SQL table
#     severity: INFO, WARN, or ERROR
#     '''
#     response = read_SQL_table(severity)
#     return jsonify(response)
