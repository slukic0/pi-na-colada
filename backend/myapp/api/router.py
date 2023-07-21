from flask import Blueprint, request, json
from flask_cors import cross_origin
import requests
from .constants import HARDWARE_HOST, MOCK_HOST
from . import database as db
from . import email_notification as notif

routerApp = Blueprint('routerApp', __name__)


@routerApp.route('/')
def hello():
    return 'My First API !!'

# Database Functions--------------------------------


@routerApp.route('/createIngredient', methods=['POST'])
@cross_origin()
def create_new_ingredient():

    data = json.loads(request.data)
    ingredientId = db.write_ingredient(data['name'])

    return ingredientId


@routerApp.route('/createDrink', methods=['POST'])
@cross_origin()
def create_new_drink():

    data = json.loads(request.data)
    drinkId = db.write_drink(data)

    return drinkId


@routerApp.route('/createUser/<userId>', methods=['POST'])
@cross_origin()
def create_new_user(userId):
    print("Creating user " + userId)
    data = json.loads(request.data)
    db.create_user(userId, data)

    return "Created", 200


@routerApp.route('/getUserDrinks', methods=['POST'])
@cross_origin()
def get_drinks():

    data = json.loads(request.data)
    drinks = db.get_user_drinks(data['id'])

    return drinks


@routerApp.route('/getDrinksFromIngredients', methods=['POST'])
@cross_origin()
def get_drinks_from_ingredients():
    data = json.loads(request.data)
    ingredients = data['ingredients']
    userId = data['userId']
    drinks = db.get_drinks_from_ingredients(userId, ingredients)

    return drinks


@routerApp.route('/getIngredients', methods=['GET'])
@cross_origin()
def get_ingredients():

    ingredients = db.get_all_ingredients()

    return ingredients


@routerApp.route('/getIngredient', methods=['POST'])
@cross_origin()
def get_ingredients_post():
    data = json.loads(request.data)
    ids = data['ingredients']

    ingredients = {}
    for id in ids:
        ingredients[str(id)] = db.get_ingredient(id)
    return ingredients


@routerApp.route('/deleteIngredient/<id>', methods=['DELETE'])
@cross_origin()
def delete_ing(id):
    print("Got request to delete ingreident with id ", id)
    response = db.delete_ingredient(id)

    return response


@routerApp.route('/deleteDrink/<drink_id>/<user_id>', methods=['DELETE'])
@cross_origin()
def del_drink(drink_id, user_id):
    print("Deleting drink with drinkId: " + drink_id + ", userId: " + user_id)
    response = db.delete_drink(drink_id, user_id)
    return response


@routerApp.route('/updateDrink', methods=['PUT'])
@cross_origin()
def update_user_drink():

    drink = json.loads(request.data)
    drink_id = drink['drinkId']
    ingredient_id = drink['ingredientId']
    amount = drink['amount']

    return db.update_drink(drink_id, ingredient_id, amount)


@routerApp.route('/loginUser', methods=['PUT'])
@cross_origin()
def user_login():

    login = json.loads(request.data)
    return db.login_user(login['userId'])


# Hardware Functions --------------------------
@routerApp.route('/pourDrink', methods=['POST'])
@cross_origin()
def pour_drink():

    data = json.loads(request.data)
    drink_id = data['drinkId']
    pumps = data['pumps']
    user_id = data['userId']
    print('Got request to pour drinkId ' + str(drink_id))

    drink = db.get_drink_by_drink_id(drink_id)
    # Get the mixture from the drink
    mixtures = drink['mixture']

    pump_info = []
    # Link an ingredient amount to a pump
    for pump in pumps:
        for mixture in mixtures:
            if (pumps[pump] == mixture['ingredientId']):
                pump_info.append({'pump': pump, 'amount': mixture['amount']})

    for element in pump_info:
        pump = element['pump']
        print("Checking level for pump " + str(pump))
        level_response = requests.post(
            'http://' +
            HARDWARE_HOST +
            '/checkLevel',
            json={
                'pump': pump,
            }
        )

        distance = float(level_response.json()['distance'])
        print('Distance: ' + str(distance))
        if float(element['amount']) > 80 - (distance):
            return {"code": "pump."+str(pump)+".low", "message": "Pump " +
                    str(pump) + " low"}, 409
    print("Levels ok")

    for element in pump_info:
        print("Pouring pump " +
              str(element['pump']) + " for " + str(element['amount']))
        requests.post(
            'http://' +
            HARDWARE_HOST +
            '/pourPump',
            json={
                'pump': element['pump'],
                'time': element['amount'],
            })

    requests.post(
        'http://' + HARDWARE_HOST + '/soundBuzzer')
    requests.post(
        'http://' + HARDWARE_HOST + '/showSenseHatSuccess')

    notif.send_notification(user_id)

    return 'Poured drink'


# Hardware Functions --------------------------
@routerApp.route('/mockPourDrink', methods=['POST'])
@cross_origin()
def mock_pour_drink():

    data = json.loads(request.data)
    drink_id = data['drinkId']
    pumps = data['pumps']
    print('Got request to pour drinkId ' + str(drink_id))

    pump_info = []
    pump_levels = {}

    drink = db.get_drink_by_drink_id(drink_id)
    # Get the mixture from the drink
    mixtures = drink['mixture']

    # Link an ingredient amount to a pump
    for pump in pumps:
        for mixture in mixtures:
            if (pumps[pump] == mixture['ingredientId']):
                pump_info.append({'pump': pump, 'amount': mixture['amount']})
    
    for element in pump_info:
        print("Checking level for pump " + str(element['pump']))
        levelResponse = requests.post(
            'http://' +
            MOCK_HOST +
            '/mockCheckLevel',
            json={
                'pump': element['pump'],
            }
        )
        pump_levels[element['pump']] = levelResponse

    for distance in pump_levels:    # Check if level is normal
        if int(distance) > 20:
            return f'Drink level too low for {distance}', 400

    print("Levels ok")

    # Pour pump
    for element in pump_info:
        print("Pouring pump " +
              str(element['pump']) + " for " + str(element['amount']))
        requests.post(
            'http://' +
            MOCK_HOST +
            '/mockPourPump',
            json={
                'pump': element['pump'],
                'time': element['amount'],
            })

    requests.post(
        'http://' + MOCK_HOST + '/mockSoundBuzzer')
    requests.post(
        'http://' + MOCK_HOST + '/mockShowSenseHatSuccess')

    # notif.send_notification(user_id)
    return 'Poured drink'


@routerApp.route('/getLogging/<severity>', methods=['GET'])
@cross_origin()
def get_logging(severity):

    log_response = requests.get(
        'http://' + HARDWARE_HOST + '/get_SQL_table/' + severity)

    return log_response.json()


@routerApp.route('/checkLevel', methods=['POST'])
@cross_origin()
def check_level():

    data = json.loads(request.data)
    level_response = requests.post(
        'http://' +
        HARDWARE_HOST +
        '/checkLevel',
        json={
            'pump': data['pump']})

    return level_response.json()


@routerApp.route('/displayIcon', methods=['POST'])
@cross_origin()
def display_icon():

    data = json.loads(request.data)
    display_icon_response = requests.post(
        'http://' +
        HARDWARE_HOST +
        '/displayIcon',
        json={
            'icon': data['icon']})

    return display_icon_response.json()


@routerApp.route('/soundBuzzer', methods=['POST'])
@cross_origin()
def sound_buzzer():

    data = json.loads(request.data)
    sound_buzzer_response = requests.post(
        'http://' +
        HARDWARE_HOST +
        '/soundBuzzer',
        json={
            'notificationType': data['notificationType']})

    return sound_buzzer_response.json()


@routerApp.route('/send_email', methods=['POST'])
@cross_origin()
def send_email():
    data = json.loads(request.data)
    response = notif.send_notification(data['userId'])
    return response


# E2E Test
@routerApp.route('/systemTest', methods=['POST'])
def systemTest():

    data = json.loads(request.data)
    ingredient_name = data['ingredientName']
    drink = data['drink']

    # Create a new ingredient
    ingredient_id = db.write_ingredient(ingredient_name)

    # Create a new drink
    drink_id = db.write_drink(drink)

    pump_info = {'pump': 1, 'time': 2}

    # Call the neccessary endpoints to pour a drink
    level_response = requests.post(
        'http://' +
        HARDWARE_HOST +
        '/checkLevel',
        json={
            'pump': pump_info['pump']}).json()
    print("got levels")
    pour_pump_response = requests.post(
        'http://' + HARDWARE_HOST + '/pourPump',
        json=pump_info).json()
    print("got pour")
    sound_buzzer_response = requests.post(
        'http://' + MOCK_HOST + '/soundBuzzer').json()
    print("got buzzer")

    response = {
        'ingredientId': ingredient_id,
        'drinkId': drink_id,
        'levels': level_response,
        'pour': pour_pump_response,
        'buzzer': sound_buzzer_response,
    }

    print(str(response))
    return response
