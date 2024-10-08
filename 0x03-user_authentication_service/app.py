#!/usr/bin/env python3
""" Basic Flask App
"""

from flask import Flask, jsonify, request, abort, make_response, redirect
from flask import url_for
from auth import Auth


app = Flask(__name__)
AUTH = Auth()


@app.route('/', methods=['GET'], strict_slashes=False)
def index():
    """ Index route
    """
    return jsonify({"message": "Bienvenue"}), 200


@app.route('/users', methods=['POST'], strict_slashes=False)
def users():
    """ Users /POST route
    """
    email = request.form.get("email")
    password = request.form.get("password")
    try:
        new_user = AUTH.register_user(email=email, password=password)
        return jsonify(
            {"email": f"{new_user.email}", "message": "user created"}
        )
    except ValueError:
        return jsonify({"message": "email already registered"}), 400


@app.route('/sessions', methods=['POST'], strict_slashes=False)
def login():
    """ User Login /POST route
    """
    email = request.form.get("email")
    password = request.form.get("password")

    if not AUTH.valid_login(email=email, password=password):
        abort(401)

    new_session = AUTH.create_session(email=email)
    response = make_response(jsonify(
        {"email": email, "message": "logged in"}
    ))
    response.set_cookie("session_id", new_session)

    return response, 200


@app.route('/sessions', methods=['DELETE'], strict_slashes=False)
def logout():
    """ User logout /DELETE route
    """
    session_id = request.cookies.get("session_id")
    if not session_id:
        abort(403)
    user = AUTH.get_user_from_session_id(session_id)
    if user:
        AUTH.destroy_session(user.id)
        return redirect(url_for("index"))
    abort(403)


@app.route('/profile', methods=['GET'], strict_slashes=False)
def profile():
    """ User profile /GET route
    """
    session_id = request.cookies.get("session_id")
    user = AUTH.get_user_from_session_id(session_id=session_id)
    if not user or not session_id:
        abort(403)
    return jsonify({"email": f"{user.email}"}), 200


@app.route('/reset_password', methods=['POST'], strict_slashes=False)
def get_reset_password_token():
    """ Password reset /POST route
    """
    email = request.form.get("email")

    try:
        token = AUTH.get_reset_password_token(email=email)
        if token:
            return jsonify({"email": email, "reset_token": token}), 200
    except ValueError:
        abort(403)


@app.route('/reset_password', methods=['PUT'], strict_slashes=False)
def update_password():
    """ Update password /PUT route
    """
    email = request.form.get("email")
    reset_token = request.form.get("reset_token")
    new_password = request.form.get("new_password")

    try:
        AUTH.update_password(reset_token, new_password)
        return jsonify({"email": email, "message": "Password updated"}), 200
    except ValueError:
        abort(403)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int("5000"))
