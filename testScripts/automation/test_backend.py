import requests
import pyrebase
import pytest
import json
from collections import OrderedDict

config = {
    "apiKey": "AIzaSyA8VEoX-GbUJMJCQKwc8mLBbKdEeuEfZ1M",
    "authDomain": "pi-na-colada.firebaseapp.com",
    "databaseURL": "https://pi-na-colada-default-rtdb.firebaseio.com/",
    "storageBucket": "pi-na-colada.appspot.com"
}

BACKEND_IP = "127.0.0.1:5000"

firebase = pyrebase.initialize_app(config)
db = firebase.database()


def test_createUser():
    user = {
        "firstName": "todelete",
        "lastName": "todelete",
        "username": "todelete",
        "email": "todelete@gmail.com",
        "phoneNumber": "442-242-4434",
        "devices": ["todeleteDevice2"],
        "savedDrinks": ["testDrink"],
        "loggedIn": bool("false")
    }

    user_key = ""

    response = requests.post('http://' + BACKEND_IP + '/createUser', json=user)
    db_response = db.child("users").order_by_key().limit_to_last(1).get().val()

    for key in db_response:
        user_key = key

    assert user == json.loads(json.dumps(db_response))[user_key]


def test_writeIngredient():
    name = "ing_test2"
    ing_key = ""
    response = requests.post(
        'http://' +
        BACKEND_IP +
        '/createIngredient',
        json={
            "name": name})
    db_response = db.child(
        "ingredients").order_by_key().limit_to_last(1).get().val()

    for key in db_response:
        ing_key = key

    assert name == json.loads(json.dumps(db_response))[ing_key]['name']


def test_getAllIngredients():
    response = requests.get('http://' + BACKEND_IP + '/getIngredients')
    dbResponse = db.child("ingredients").get().val()

    assert dbResponse == json.loads(response.text)


def test_getIngredient():
    ing_id = "-NQ7KewvYmiD3bip6vnf"
    name = "limeTest"
    response = requests.post(
        'http://' +
        BACKEND_IP +
        '/getIngredient',
        json={
            "ingredients": [ing_id]})

    print(response.text)

    assert name == json.loads(response.text)[ing_id]['name']


def test_writeDrink():
    user_id = "-NR9iy7yIFHPVAMKx3h_"
    response = requests.post(
        'http://' + BACKEND_IP + '/createDrink',
        json={
            "description": "todelete",
            "mixture": ["-NQq01pcTXiOqwOImdPB"],
            "name": "todelete",
            "userId": user_id})
    drink = response.text
    data = db.child("drinks").child(drink).get().val()
    jsonTest = json.dumps(data)

    testJson = {
        "description": "todelete",
        "mixture": ["-NQq01pcTXiOqwOImdPB"],
        "name": "todelete",
        "userId": user_id}
    assert testJson == json.loads(jsonTest)


def test_deleteIngredient():
    ing_id = ""
    key = ""
    ids = db.child("ingredients").order_by_key().limit_to_last(
        1).get().val()  # Get latest ingredient added

    for key in ids:
        ing_id = key

    response = requests.post(
        'http://' +
        BACKEND_IP +
        '/deleteIngredient',
        json={
            "id": ing_id})
    dbResponse = db.child("ingredients").child(key).get().val()

    assert None is dbResponse


def test_getUserDrinks():
    id = "-NR9iy7yIFHPVAMKx3h_"
    drink_id = "-NR9jLWt11d1KdD2yPCo"
    response = requests.post(
        'http://' +
        BACKEND_IP +
        '/getUserDrinks',
        json={
            "id": id})
    db_response = db.child("users").child(id).get().val()

    db_json = json.dumps(db_response)
    db_json = json.loads(db_json)

    assert "-NR9jLWt11d1KdD2yPCo" == db_json['savedDrinks'][0]


# Test seperately -----

# def test_deleteDrink():
#    drink_id = "-NR9ummducUqUBTpjJqL"
#    user_id = "-NR9iy7yIFHPVAMKx3h_"

#    response = requests.delete('http://'+BACKEND_IP+'/deleteDrink/'+drink_id+"/"+user_id)
#    dB_response = db.child("drinks").child(drink_id).get().val()

#    assert {"id": drink_id} == json.loads(response.text)

# def test_loginUser():
#    is_logged_in = True
#    user_id = "-NR9iy7yIFHPVAMKx3h_"
#    response = requests.put('http://'+BACKEND_IP+'/loginUser/'+ user_id)
#    dbResponse = db.child("users").child(user_id).get().val()

#    print(dbResponse)

#    assert is_logged_in == dbResponse['loggedIn']


# def test_updateDrink():
#    name = "ing_test"
#    ing_key = ""
#    response = requests.post('http://'+BACKEND_IP+'/createIngredient', json={"name":"ing_test"})
#    dbResponse = db.child("ingredients").order_by_key().limit_to_last(1).get().val()

#    for key in dbResponse.keys():
#       ing_key = key

#    print(ing_key)
#    print(dbResponse)
#    assert name == dbResponse[str(ing_key)]['name']
