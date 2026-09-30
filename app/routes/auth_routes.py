import re

from flask import Blueprint, jsonify, request

from app.services.auth_service import login_user, signup_user

auth_bp = Blueprint("auth", __name__)
EMAIL_PATTERN = re.compile(r"^[^\s@]+@[^\s@]+\.[^\s@]+$")


def _validate_credentials(data, signup=False):
    if not isinstance(data, dict):
        return "A JSON object is required"

    name = data.get("name")
    email = data.get("email")
    password = data.get("password")
    if signup and (not isinstance(name, str) or not name.strip()):
        return "name is required"
    if not isinstance(email, str) or not EMAIL_PATTERN.fullmatch(email.strip()):
        return "A valid email address is required"
    if not isinstance(password, str) or not password:
        return "password is required"

    if signup:
        if len(name.strip()) > 20:
            return "name must be at most 20 characters"
        if len(email.strip()) > 50:
            return "email must be at most 50 characters"
        if len(password) < 8 or len(password.encode("utf-8")) > 72:
            return "password must be at least 8 characters and at most 72 UTF-8 bytes"
    return None


@auth_bp.route("/signup", methods=["POST"])
def signup():
    data = request.get_json(silent=True)
    error = _validate_credentials(data, signup=True)
    if error:
        return jsonify({"error": error}), 400

    user, error = signup_user(data)
    if error:
        return jsonify({"error": error}), 409
    return jsonify(user), 201


@auth_bp.route("/login", methods=["POST"])
def login():
    data = request.get_json(silent=True)
    error = _validate_credentials(data)
    if error:
        return jsonify({"error": error}), 400

    result, error = login_user(data)
    if error:
        return jsonify({"error": error}), 401
    return jsonify(result), 200
