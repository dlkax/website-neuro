from flask import Flask, request, jsonify, render_template, session, redirect
from flask_cors import CORS
from openai import OpenAI
from dotenv import load_dotenv
from utils.database import create_tables
from routes.auth import auth_bp
import os

load_dotenv()

app = Flask(__name__)

app.config["SECRET_KEY"] = "atlas-neurogen-secret"

#CORS(app)

client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY")
)

SYSTEM_PROMPT = """
Você é o Atlas AI da NeuroGen.
Missão:
Mapeando o futuro da humanidade.

Áreas:
- Inteligência Artificial
- Biotecnologia
- Engenharia Aeroespacial

Projetos:
- NeuroGen Atlas
- AURORA-X
- Genesis AI
- Projeto Helix
- Nova Interface
- QuantumCore

Responda sempre em português brasileiro.
"""

@app.route("/chat", methods=["POST"])
def chat():

    data = request.json
    user_message = data.get("message", "")

    response = client.responses.create(
        model="gpt-5",
        instructions=SYSTEM_PROMPT,
        input=user_message
    )

    return jsonify({
        "reply": response.output_text
    })

@app.route("/")
def login_page():
    return render_template("login.html")


@app.route("/register-page")
def register_page():
    return render_template("register.html")

@app.route("/dashboard")
def dashboard():

    if "user_id" not in session:
        return redirect("/")

    return render_template(
        "dashboard.html",
        username=session["username"]
    )

@app.route("/test-session")
def test_session():

    print("SESSION TESTE:")
    print(dict(session))

    return {
        "user_id": session.get("user_id"),
        "username": session.get("username")
    }

@app.route("/set-test")
def set_test():

    session["user_id"] = 999
    session["username"] = "atlas"

    return "OK"

@app.route("/logout")
def logout():

    session.clear()

    return redirect("/")

app.register_blueprint(auth_bp)

if __name__ == "__main__":
    create_tables()
    app.run(debug=True)