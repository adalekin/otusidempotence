import datetime

from werkzeug.security import check_password_hash

from users.extensions import db, marshmallow

__all__ = ["User"]


class User(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    email = db.Column(db.String(256), nullable=True)
    phone = db.Column(db.String(30), nullable=True)
    first_name = db.Column(db.String(64), nullable=True)
    last_name = db.Column(db.String(64), nullable=True)
    password = db.Column(db.String(256))

    is_active = db.Column(db.Boolean(), default=True)

    last_login = db.Column(db.DateTime, default=datetime.datetime.utcnow)

    updated_at = db.Column(db.DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)
    created_at = db.Column(db.DateTime, default=datetime.datetime.utcnow)

    def __repr__(self):
        return f"<User {self.id}>"

    def verify_password(self, password):
        return check_password_hash(self.password, password)


class UserSchema(marshmallow.SQLAlchemyAutoSchema):
    class Meta:
        model = User
        exclude = ("password",)


user_schema = UserSchema()
users_schema = UserSchema(many=True)
