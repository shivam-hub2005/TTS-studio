from flask import Flask, render_template, request, jsonify, send_file
import edge_tts
import asyncio
import uuid
from pathlib import Path

app = Flask(__name__)
AUDIO_DIR = Path("generated_audio")
AUDIO_DIR.mkdir(exist_ok=True)

VOICES = {
    "English - Female": "en-US-JennyNeural",
    "English - Male": "en-US-GuyNeural",
    "Hindi - Female": "hi-IN-SwaraNeural",
    "Hindi - Male — Deep Documentary": "hi-IN-MadhurNeural",
    "Chinese - Female": "zh-CN-XiaoxiaoNeural",
    "Chinese - Male": "zh-CN-YunxiNeural",
}

async def synthesize(text, voice, rate):
    filename = f"{uuid.uuid4().hex}.mp3"
    path = AUDIO_DIR / filename
    communicate = edge_tts.Communicate(text, voice, rate=rate)
    await communicate.save(str(path))
    return path

@app.get("/")
def index():
    return render_template("index.html", voices=VOICES)

@app.post("/api/synthesize")
def synthesize_api():
    data = request.get_json(silent=True) or {}
    text = (data.get("text") or "").strip()
    voice_key = data.get("voice")
    rate = data.get("rate", "-8%")

    if not text:
        return jsonify({"error": "Please enter some text."}), 400
    if len(text) > 5000:
        return jsonify({"error": "Text is limited to 5000 characters in this demo."}), 400
    if voice_key not in VOICES:
        return jsonify({"error": "Invalid voice selected."}), 400

    try:
        path = asyncio.run(synthesize(text, VOICES[voice_key], rate))
        return jsonify({
            "success": True,
            "audio_url": f"/audio/{path.name}",
            "download_url": f"/download/{path.name}"
        })
    except Exception as e:
        return jsonify({"error": f"TTS generation failed: {e}"}), 500

@app.get("/audio/<filename>")
def audio(filename):
    path = AUDIO_DIR / filename
    if not path.exists():
        return "Not found", 404
    return send_file(path, mimetype="audio/mpeg")

@app.get("/download/<filename>")
def download(filename):
    path = AUDIO_DIR / filename
    if not path.exists():
        return "Not found", 404
    return send_file(path, as_attachment=True, download_name="tts_audio.mp3")

if __name__ == "__main__":
    app.run(debug=True, host="127.0.0.1", port=5000)
