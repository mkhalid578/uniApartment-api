from flask import Flask
from flask_cors import CORS
from peewee import PostgresqlDatabase

import config

app = Flask(__name__)
cors = CORS(app, resources={r"/*": {"origins": "*"}})
db = PostgresqlDatabase(
    database=config.DB_NAME,
    user=config.DB_USERNAME, password=config.DB_PASSWORD, host=config.DB_LOCATION, port=config.DB_PORT)
# host=config.DB_LOCATION, port=config.DB_PORT,


from app.models.user import User
from app.models.property import Property
db.create_tables([
	User,
	Property], safe = True)


from app.controller.user import user
app.register_blueprint(user)

from app.controller.property import property
app.register_blueprint(property)
