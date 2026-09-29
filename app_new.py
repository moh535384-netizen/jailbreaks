import os
from pathlib import Path

import requests
from flask import Flask, jsonify, render_template, request

app = Flask(__name__)

# RunPod Endpoint ثابت
ENDPOINT_ID = "1qo88t036ztsye"

# يتم أخذ API Key من Render Environment فقط
API_KEY = os.getenv("RUNPOD_API_KEY", "")

# قراءة ملف الـ System Prompt بدون تغيير محتواه
SYSTEM_PROMPT = (
    Path(__file__).parent / "deepseek-4-1.md"
).read_text(encoding="utf-8")


@app.get("/")
def index():
    return render_template("index.html")


@app.post("/api/chat")
def chat():
    if not API_KEY:
        return jsonify({
            "error": "RUNPOD_API_KEY is not configured on the server."
        }), 500

    body = request.get_json(silent=True) or {}
    history = body.get("messages", [])

    if not isinstance(history, list):
        return jsonify({
            "error": "messages must be an array"
        }), 400

    # deepseek-4-1.md يتم إرساله كـ System Prompt
    messages = [
        {
            "role": "system",
            "content": SYSTEM_PROMPT
        }
    ]

    for m in history:
        if (
            isinstance(m, dict)
            and m.get("role") in ("user", "assistant")
            and isinstance(m.get("content"), str)
        ):
            messages.append({
                "role": m["role"],
                "content": m["content"]
            })

    payload = {
        "input": {
            "messages": messages,
            "max_tokens": 1000
        }
    }

    try:
        url = f"https://api.runpod.ai/v2/{ENDPOINT_ID}/runsync"

        r = requests.post(
            url,
            headers={
                "Authorization": f"Bearer {API_KEY}",
                "Content-Type": "application/json"
            },
            json=payload,
            timeout=180
        )

        r.raise_for_status()
        data = r.json()

        output = data.get("output")

        if isinstance(output, list) and output:
            item = output[0]
        elif isinstance(output, dict):
            item = output
        else:
            item = {}

        choices = (
            item.get("choices", [])
            if isinstance(item, dict)
            else []
        )

        if choices:
            choice = choices[0]
            msg = choice.get("message")

            if isinstance(msg, dict):
                content = msg.get("content", "")
            else:
                content = choice.get("text", "")

            return jsonify({
                "reply": content,
                "raw_status": data.get("status")
            })

        return jsonify({
            "error": "No model reply found.",
            "raw": data
        }), 502

    except requests.RequestException as e:
        detail = ""

        if getattr(e, "response", None) is not None:
            detail = e.response.text

        return jsonify({
            "error": str(e),
            "detail": detail[:2000]
        }), 502


if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=int(os.getenv("PORT", "8080"))
    )
