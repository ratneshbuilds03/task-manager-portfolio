from app import db
from app.models.user import User
from flask_jwt_extended import create_access_token
from sqlalchemy.exc import IntegrityError


def signup_user(data):
    email = data["email"].strip().casefold()
    existing_user = User.query.filter_by(email=email).first()
    if existing_user:
        return None, "Email already registered"
    new_user = User(
        name=data["name"].strip(),
        email=email,
    )
    new_user.set_password(data.get("password"))

    db.session.add(new_user)
    try:
        db.session.commit()
    except IntegrityError:
        db.session.rollback()
        return None, "Email already registered"

    return new_user.to_dict(),None


def login_user(data):
    email = data["email"].strip().casefold()
    password = data["password"]
    user = User.query.filter_by(email=email).first()

    if not user or not user.check_password(password):
        return None, "Invalid email or password"

    access_token = create_access_token(identity=str(user.id))
    return {"access_token": access_token, "user": user.to_dict()}, None