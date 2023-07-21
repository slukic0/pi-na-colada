import pyrebase
from uuid import UUID


# Initialize the database config
config = {
    "apiKey": "AIzaSyA8VEoX-GbUJMJCQKwc8mLBbKdEeuEfZ1M",
    "authDomain": "pi-na-colada.firebaseapp.com",
    "databaseURL": "https://pi-na-colada-default-rtdb.firebaseio.com/",
    "storageBucket": "pi-na-colada.appspot.com"
}

# Global Constants
firebase = pyrebase.initialize_app(config)
db = firebase.database()


def write_drink(drink_json: dict):
    """
    Creates a new drink in the database
    and adds it to the user's saved drinks

    Args:
        drink_json (dict): a json containing a new drink

    Returns:
        drink_id int: drink id of the new drink
    """
    drink_id = db.child('drinks').push(drink_json)['name']
    user_id = drink_json['userId']

    drinks = []

    user = db.child("users").child(user_id).get().val()
    if 'savedDrinks' not in user:
        drinks.append(drink_id)
        db.child("users").child(user_id).update({"savedDrinks": drinks})
    else:
        drinks = user['savedDrinks']
        drinks.append(drink_id)
        db.child("users").child(user_id).update({"savedDrinks": drinks})

    return drink_id


def write_ingredient(name: str):
    """
    Creates a new ingredient in the database

    Args:
        name (str): name of the ingredient

    Returns:
        name str: return the name of the ingridient
    """

    result = db.child("ingredients").push({"name": name})
    return result.get('name')


def delete_ingredient(id: str):
    """
    Deletes an ingredient from a user's drink in the database

    Args:
        id: a string represenging ingredient id
    """
    drinks = db.child("drinks").get()

    for drink in drinks.each():
        for key in drink.val():
            if (key == "mixture"):
                for ing in drink.val()['mixture']:
                    if ing['ingredientId'] == id:
                        return "Cannot delete: Ingredient is in use", 209

    db.child("ingredients").child(id).remove()
    return "Deleted", 200


def create_user(userId, data: dict):
    """
    Creates a new user in the database

    Args:
        data (dict): a json payload containing user information

    Returns:
        name str: the user's name
    """

    result = db.child("users").child(userId).set(data)
    return result.get('userName')


def get_ingredient(ingredient_id: UUID):
    """\
    Gets an ingredient from the database given an id

    Args:
        ingredient_id (UUID): the id of the ingredient

    Returns:
        _type_: OrderedDict([])
    """

    ingredient = db.child("ingredients").child(ingredient_id).get()
    return ingredient.val()


def get_all_ingredients():
    """
    Returns all the ingredients in the database

    Returns:
        ingredients.val() _type_: OrderedDict([])
    """

    ingredients = db.child("ingredients").get()
    return ingredients.val()


def get_user_drinks(id: UUID):
    """
    Gets all the drinks for the given user

    Args:
        id (UUID): the id of the user

    Returns:
        drinks list: a list of all the user's drinks
    """

    user = db.child("users").child(id).get().val()
    if user is None:
        return "User does not exist", 400
    if 'savedDrinks' not in user:
        return []
    drink_ids = user['savedDrinks']

    drinks = []

    for drink_id in drink_ids:
        drink = db.child("drinks").child(drink_id).get().val()
        if drink is not None:
            drink['id'] = drink_id
            drinks.append(drink)
    return drinks


def get_drink_by_drink_id(drink_id: UUID):
    '''
    Get a drink from the database given its drinkId 
    '''
    return db.child("drinks").child(drink_id).get().val()


def get_drinks_from_ingredients(userId, ingredients):
    if len(ingredients) == 0:
        return []
    all_drinks = db.child("drinks").get()
    drinks = []

    for drink in all_drinks.each():
        drink_dict = drink.val()
        mixture = drink_dict['mixture']
        drinkIngredients = []
        for ingredient in mixture:
            drinkIngredients.append(ingredient['ingredientId'])
        if (sorted(drinkIngredients) == sorted(ingredients)
                and drink_dict['userId'] == userId):
            drinks.append({'id': drink.key(), 'name': drink.val()['name']})

    return drinks


def login_user(user_id: UUID):
    """
    Sets login field in user to True

    Args:
        user_id (UUID): the user id to be logged in

    Returns:
        response: OrderedDict([])
    """
    response = db.child("users").child(user_id).update({"loggedIn": True})
    return response


def delete_drink(drink_id: UUID, user_id: UUID):
    """
    Deletes a drink from the users saved drinks list
    and deletes the drink from the drinks table

    Args:
        drink_id (UUID): the id of the user
        user_id (UUID): the id of the drink

    Returns:
        dict: dict with the id of the deleted drink
    """

    saved_drinks = []
    db.child("drinks").child(drink_id).remove()
    user_drinks = db.child("users").get(user_id).val()

    saved_drinks = user_drinks[str(user_id)]['savedDrinks']

    saved_drinks.remove(drink_id)
    db.child("users").child(user_id).update({"savedDrinks": saved_drinks})

    return {"id": drink_id}


def update_drink(drink_id, ingredient_id, amount):

    drink = db.child("drinks").child(drink_id).get()
    ingredient_map = {}

    for field in drink.each():
        if (type(field.val()) == type(ingredient_map)):
            ingredient_map = field.val()

    ingredient_map.update({ingredient_id: amount})
    db.child("drinks").child(drink_id).child(
        "mixture").update(ingredient_map)

    return ingredient_map
