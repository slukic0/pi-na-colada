import requests
import pyrebase

config = {
    "apiKey": "AIzaSyA8VEoX-GbUJMJCQKwc8mLBbKdEeuEfZ1M",
    "authDomain": "pi-na-colada.firebaseapp.com",
    "databaseURL": "https://pi-na-colada-default-rtdb.firebaseio.com/",
    "storageBucket": "pi-na-colada.appspot.com"
}

firebase = pyrebase.initialize_app(config)
db = firebase.database()

BACKEND_IP = "192.168.242.151:5000"


def test_end_to_end_demo():
    # Trigger test endpoint
    response = requests.post(
        'http://' +
        BACKEND_IP +
        '/systemTest',
        json={
            "drink": {
                "name": "coronaTest"},
            "ingredientName": "limeTest"}).json()
    print(str(response))
    ingredientId = response['ingredientId']
    drinkId = response['drinkId']

    drinkResult = db.child('drinks').child(drinkId).get().val()
    # print(drinkResult)
    ingredientResult = db.child('ingredients').child(ingredientId).get().val()
    # print(ingredientResult)

    assert drinkResult == {"name": "coronaTest"}
    assert ingredientResult == {"name": "limeTest"}
    assert response['levels'] == {
        "distance": "20 cm",
        "status": "OK"
    }
    assert response['pour'] == {
        "1": "2 seconds",
        "status": "OK"
    }
    assert response['buzzer'] == {
        "status": "OK"
    }
