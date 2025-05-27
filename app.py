from flask import Flask, render_template, request, jsonify
import os
from dotenv import load_dotenv
from openai import OpenAI
from prompt import generate_prompt
from main import transcribe_audio
from main import generate_note
from main import get_score_from_llm
from datetime import datetime
import sqlite3

from phoenix.otel import register
from openinference.instrumentation.openai import OpenAIInstrumentor
from db.note_repository import NoteRepository

app = Flask(__name__)
repo = NoteRepository()
UPLOAD_FOLDER = "uploads"
TRANSCRIPTION_FOLDER = "output"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(TRANSCRIPTION_FOLDER, exist_ok=True)

#conn = sqlite3.connect("database.db")
#cursor = conn.cursor()

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/analyze", methods=["POST"])
def analyze():
    print(" Doing proccess for transcription ")
    file = request.files["audio"]
    filepath = os.path.join(UPLOAD_FOLDER, file.filename)
    file.save(filepath)
    transcription = transcribe_audio(filepath)
    #transcription = "Good morning, how can I help you today? Hello, doctor. Since last night, I've had abdominal pain, vomiting, and diarrhea. I'm not feeling well. I'm sorry to hear that. How many times have you vomited or had diarrhea since the symptoms started? I vomited about three times and gone to the bathroom maybe six times. It all started around 11 PM. Have you had any fever or chills? Yes, I had a fever this morning. I think it reached 38 degrees Celsius. Have you noticed any blood in your stools or vomit? No, just very watery and yellowish. Did you eat anything outside the house in the last 24 hours? Maybe something that didn't seem right? I had lunch at a restaurant yesterday. I ate chicken and rice, but it tasted a bit strange. I see. Do you have any significant medical history? Are you on any regular medications? No, I'm generally healthy. I'm only allergic to penicillin. Okay, have you been able to stay hydrated? Are you drinking water or oral rehydration? I've tried drinking."
    prompt = generate_prompt("v4", transcription)
    print(" Generating Note ------------------------ ")
    note = generate_note(prompt, prompt_version="v4")
    #transcription = "Good morning, how can I help you today? Hello, doctor. Since last night, I've had abdominal pain, vomiting, and diarrhea. I'm not feeling well. I'm sorry to hear that. How many times have you vomited or had diarrhea since the symptoms started? I vomited about three times and gone to the bathroom maybe six times. It all started around 11 PM. Have you had any fever or chills? Yes, I had a fever this morning. I think it reached 38 degrees Celsius. Have you noticed any blood in your stools or vomit? No, just very watery and yellowish. Did you eat anything outside the house in the last 24 hours? Maybe something that didn't seem right? I had lunch at a restaurant yesterday. I ate chicken and rice, but it tasted a bit strange. I see. Do you have any significant medical history? Are you on any regular medications? No, I'm generally healthy. I'm only allergic to penicillin. Okay, have you been able to stay hydrated? Are you drinking water or oral rehydration? I've tried drinking."
    return jsonify({
        "result": note,
        "transcription": transcription,
        "filename": file.filename
    })
@app.route("/save", methods=["POST"])
def save():
    final_note = request.form["text"]
    draft_note = request.form["draft_note"]
    transcription = request.form["transcription"]
    #print(transcription)
    filename = request.form.get("filename", f"note_{datetime.now().strftime('%Y%m%d_%H%M%S')}.mp3")
    score = get_score_from_llm(draft_note, final_note)
    repo.save_note(filename, transcription, draft_note, final_note, score)
    return jsonify({"message": "Note saved.", "score": score})

if __name__ == "__main__":
    app.run(debug=True)
