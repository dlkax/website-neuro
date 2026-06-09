from flask import Blueprint, request, jsonify, session

from utils.database import get_db
from utils.security import hash_password, verify_password

auth_bp = Blueprint("auth", __name__)


# =========================
# REGISTER
# =========================
@auth_bp.route("/register", methods=["POST"])
def register():

    data = request.json

    username = data.get("username")
    email = data.get("email")
    password = data.get("password")

    if not username or not email or not password:
        return jsonify({
            "success": False,
            "message": "Preencha todos os campos."
        }), 400

    conn = get_db()

    try:

        conn.execute(
            """
            INSERT INTO users
            (
                username,
                email,
                password_hash
            )
            VALUES (?, ?, ?)
            """,
            (
                username,
                email,
                hash_password(password)
            )
        )

        conn.commit()

        return jsonify({
            "success": True,
            "message": "Usuário criado."
        }), 200

    except Exception:

        return jsonify({
            "success": False,
            "message": "Usuário ou email já existe."
        }), 400

    finally:
        conn.close()


# =========================
# LOGIN
# =========================
@auth_bp.route("/login", methods=["POST"])
def login():

    data = request.json

    email = data.get("email")
    password = data.get("password")

    if not email or not password:
        return jsonify({
            "success": False,
            "message": "Preencha todos os campos."
        }), 400

    conn = get_db()

    try:

        user = conn.execute(
            """
            SELECT *
            FROM users
            WHERE email = ?
            """,
            (email,)
        ).fetchone()

        if not user:
            return jsonify({
                "success": False,
                "message": "Usuário não encontrado."
            }), 404

        if not verify_password(password, user["password_hash"]):
            return jsonify({
                "success": False,
                "message": "Senha incorreta."
            }), 401

        session["user_id"] = user["id"]
        session["username"] = user["username"]
        session["email"] = user["email"]
        session["created_at"] = user["created_at"]
        session["role"] = user["role"]

        print("SESSION SALVA:")
        print(dict(session))

        return jsonify({
            "success": True,
            "message": "Login realizado com sucesso."
        })

    finally:
        conn.close()