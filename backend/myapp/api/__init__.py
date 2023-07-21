from flask import Flask
from flask_cors import CORS
from .router import routerApp

app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

app.register_blueprint(routerApp)