from flask import Flask, request, jsonify
from flask_cors import CORS
from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv()

app = Flask(__name__)
CORS(app)

@app.route("/")
def home():
    return "Atlas Backend Online"

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

if __name__ == "__main__":
    app.run(debug=True)