from flask import Flask, request, jsonify
from flask_cors import CORS
import whisper
from pathlib import Path
from summarizer import summarize_transcript, generate_action_items
import re

app = Flask(__name__)
CORS(app)

# -----------------------------
# Paths
# -----------------------------
BASE_DIR = Path(__file__).resolve().parent
AUDIO_DIR = BASE_DIR / "data" / "audio"
TRANSCRIPT_DIR = BASE_DIR / "data" / "transcript"
TRANSCRIPT_FILE = TRANSCRIPT_DIR / "transcript.txt"

AUDIO_DIR.mkdir(parents=True, exist_ok=True)
TRANSCRIPT_DIR.mkdir(parents=True, exist_ok=True)

# -----------------------------
# Load Whisper model
# -----------------------------
print("🔄 Loading Whisper model...")
model = whisper.load_model("base")

def format_as_conversation(raw_text):
    sentences = re.split(r'(?<=[.?!])\s+', raw_text.strip())
    formatted_lines = []
    speaker_num = 1
    for sentence in sentences:
        if sentence.strip():
            formatted_lines.append(f"Speaker {speaker_num}: {sentence.strip()}")
            speaker_num += 1
            if speaker_num > 5:
                speaker_num = 1
    return "\n".join(formatted_lines)

# -----------------------------
# API Endpoint
# -----------------------------
@app.route('/upload', methods=['POST'])
def upload_audio():
    if 'file' not in request.files:
        return jsonify({"error": "No file part"}), 400

    file = request.files['file']
    if file.filename == "":
        return jsonify({"error": "No selected file"}), 400

    audio_path = AUDIO_DIR / file.filename
    file.save(audio_path)

    print(f"🎧 Transcribing audio: {file.filename}")
    result = model.transcribe(str(audio_path))
    transcript = result.get("text", "").strip()

    # Save raw transcript
    with open(TRANSCRIPT_FILE, "w", encoding="utf-8") as f:
        f.write(transcript)

    formatted_transcript = format_as_conversation(transcript)

    print("🧠 Generating summary...")
    summary = summarize_transcript(transcript)

    print("📝 Generating action items...")
    action_items = generate_action_items(transcript)

    return jsonify({
        "transcript": formatted_transcript,
        "summary": summary,
        "action_items": action_items
    })

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
