from flask import Flask, request, jsonify, render_template, session, redirect
from flask_cors import CORS
from openai import OpenAI
from dotenv import load_dotenv
from utils.database import create_tables
from routes.auth import auth_bp
import os

load_dotenv()

app = Flask(__name__)

app.config["SECRET_KEY"] = os.getenv("SECRET_KEY", "atlas-neurogen-secret")

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

    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": user_message}
        ]
    )

    return jsonify({
        "reply": response.choices[0].message.content
    })

@app.route("/")
def home():
    return render_template("index.html", username=session.get("username"))

@app.route("/divisoes")
def divisoes():
    return render_template("divisoes.html", username=session.get("username"))

@app.route("/projetos")
def projetos():
    return render_template("projetos.html", username=session.get("username"))

@app.route("/atlas")
def atlas():
    return render_template("atlas.html", username=session.get("username"))

@app.route("/dashboard")
def dashboard():

    if "user_id" not in session:
        return redirect("/login")

    return render_template(
        "dashboard.html",
        username=session.get("username"),
        email=session.get("email"),
        created_at=session.get("created_at"),
        role=session.get("role")
    )

@app.route("/login")
def login_page():
    return render_template("login.html")

@app.route("/register")
def register_page():
    return render_template("register.html")

@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")

app.register_blueprint(auth_bp)

if __name__ == "__main__":
    create_tables()
    app.run(debug=True)