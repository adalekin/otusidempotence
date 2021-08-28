from sqlalchemy import or_
from talepy.steps import Step
from werkzeug.security import generate_password_hash

from users.exception import AlreadyExists
from users.extensions import db, kafka
from users.models.user import User
from schemas.user import UserRegistered


class CreateUser(Step):
    def execute(self, state):
        with db.session.begin(subtransactions=True):
            if state["phone"]:
                user_already_exists_condition = or_(User.email == state["email"], User.phone == state["phone"])
            else:
                user_already_exists_condition = User.email == state["email"]
            user_already_exists = db.session.query(User.query.filter(user_already_exists_condition).exists()).scalar()

            AlreadyExists.require_condition(
                not user_already_exists, "A user already exists with the specified email address or phone number"
            )

            if state["password"]:
                state["password"] = generate_password_hash(state["password"])

            user = User(
                email=state["email"],
                phone=state["phone"],
                first_name=state["first_name"],
                last_name=state["last_name"],
                password=state["password"],
            )
            db.session.add(user)

        state["user"] = user
        return state

    def compensate(self, state):
        with db.session.begin(subtransactions=True):
            db.session.delete(state["user"])


class SendUserRegistered(Step):
    def execute(self, state):
        user_registered = UserRegistered(user_id=state["user"].id)

        kafka.send("user-registered", user_registered.serialize())
        return state

    def compensate(self, state):
        pass
