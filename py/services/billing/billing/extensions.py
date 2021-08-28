import os

from flask_marshmallow import Marshmallow

from flask_migrate import Migrate

from flask_sqlalchemy import SQLAlchemy

from . import settings

__all__ = ["db", "ma", "migrate"]

db = SQLAlchemy(session_options={"autocommit": True})

marshmallow = Marshmallow()

migrate = Migrate(directory=os.path.join(os.path.dirname(os.path.abspath(__file__)), "migrations"))
