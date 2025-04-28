from flask import Flask, render_template, request, jsonify
import requests
import os

app = Flask(__name__)

# Ortam değişkeninden al, yoksa localhost kullan
OLLAMA_URL = os.getenv("OLLAMA_HOST", "http://ollama:11434") + "/api/generate"
MODEL_NAME = "llama3.1:8b"  # Veya başka bir model

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat():
    user_message = request.json.get("message", "")

    system_prompt = (
        "You are an artificial intelligence assistant and a Python code developer. "
        "You are given a code as a prompt. You take this code and develop it by making it more detailed. "
        "Then you write a title and write new written code and explain this code. "
        "Don't forget to use space and line transition to create more readable output."
    )

    full_prompt = system_prompt + "\n\n" + user_message

    payload = {
        "model": MODEL_NAME,
        "prompt": full_prompt,
        "stream": False
    }

    try:
        response = requests.post(OLLAMA_URL, json=payload)
        response.raise_for_status()
        response_json = response.json()
        model_reply = response_json.get("response", "No response from model.")
        return jsonify({"response": model_reply})
    except requests.RequestException as e:
        return jsonify({"response": f"Request error: {str(e)}"})
    except Exception as e:
        return jsonify({"response": f"Unexpected error: {str(e)}"})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)
