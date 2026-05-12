import json
import os
from urllib import error, request

from flask import Flask, jsonify, render_template, request as flask_request

from chatbot_engine import ChatbotKnowledgeBase


app = Flask(__name__)
knowledge_base = ChatbotKnowledgeBase.from_json("data/legal_knowledge.json")


def load_env_file(path=".env"):
    """Load simple KEY=VALUE pairs without requiring python-dotenv."""
    if not os.path.exists(path):
        return

    with open(path, "r", encoding="utf-8") as env_file:
        for line in env_file:
            line = line.strip()
            if not line or line.startswith("#") or "=" not in line:
                continue

            key, value = line.split("=", 1)
            os.environ.setdefault(key.strip(), value.strip().strip('"').strip("'"))


load_env_file()


def openai_response(message):
    if os.getenv("ENABLE_OPENAI", "").lower() != "true":
        return None

    api_key = os.getenv("OPENAI_API_KEY")
    model = os.getenv("OPENAI_MODEL")

    if not api_key or not model:
        return None

    context = knowledge_base.context_for_prompt(message)
    payload = {
        "model": model,
        "messages": [
            {
                "role": "system",
                "content": (
                    "You are a careful assistant for a Pakistan workplace harassment legal "
                    "information chatbot. Use the provided knowledge base context when relevant. "
                    "Give concise, practical, trauma-informed information. Do not claim to be a "
                    "lawyer. Encourage urgent safety steps for danger. End with a short "
                    "legal-information disclaimer."
                ),
            },
            {"role": "user", "content": f"Knowledge base context:\n{context}\n\nQuestion: {message}"},
        ],
        "temperature": 0.3,
    }

    api_request = request.Request(
        "https://api.openai.com/v1/chat/completions",
        data=json.dumps(payload).encode("utf-8"),
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        },
        method="POST",
    )

    try:
        with request.urlopen(api_request, timeout=20) as response:
            data = json.loads(response.read().decode("utf-8"))
            return data["choices"][0]["message"]["content"].strip()
    except (error.URLError, error.HTTPError, KeyError, IndexError, json.JSONDecodeError):
        return None


def get_response(user_input):
    user_input = user_input or ""
    ai_reply = openai_response(user_input)
    if ai_reply:
        return ai_reply

    return knowledge_base.answer(user_input)


@app.route("/")
def home():
    return render_template("index.html", suggested_prompts=knowledge_base.suggested_prompts)


@app.route("/chat", methods=["POST"])
def chat():
    data = flask_request.get_json(silent=True) or {}
    user_input = data.get("message", "")
    return jsonify({"reply": get_response(user_input)})


@app.route("/health")
def health():
    return jsonify(
        {
            "status": "ok",
            "topics": len(knowledge_base.topics),
            "matching": knowledge_base.matching_mode,
        }
    )


@app.route("/topics")
def topics():
    return jsonify(knowledge_base.topic_summaries())


if __name__ == "__main__":
    app.run(debug=True, use_reloader=False)
