import os

from flask_kafka import Kafka
from flask_marshmallow import Marshmallow
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy(session_options={"autocommit": True})

kafka = Kafka()

marshmallow = Marshmallow()

migrate = Migrate(directory=os.path.join(os.path.dirname(os.path.abspath(__file__)), "migrations"))
