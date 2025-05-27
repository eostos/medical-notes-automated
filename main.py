
import os
from dotenv import load_dotenv
from openai import OpenAI
from prompt import generate_prompt
from prompt import generate_score_prompt


# ✅ Phoenix & OpenInference integration (latest method)
from phoenix.otel import register
from openinference.instrumentation.openai import OpenAIInstrumentor

# Set up tracing
tracer_provider = register()
OpenAIInstrumentor().instrument(tracer_provider=tracer_provider)


# Load environment variables
load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# --- Function: Transcribe Audio ---
def transcribe_audio(file_path: str) -> str:
    print(" Transcribing audio...")
    with open(file_path, "rb") as audio_file:
        response = client.audio.transcriptions.create(
            model="whisper-1",
            file=audio_file,
            response_format="text"
        )
    print(" Transcription complete.\n")
    print("--------------------------------------------------")
    #print(response)
    print("--------------------------------------------------")
    return response.strip()

# --- Function: Generate Note from Prompt ---
def generate_note(prompt: str, prompt_version: str, model="gpt-4") -> str:
    print(f"🤖 Generating note with LLM using prompt version: {prompt_version}")
    response = client.chat.completions.create(
        model=model,
        messages=[{"role": "user", "content": prompt}],
        temperature=0
    )


    note = response.choices[0].message.content.strip()
    print(" Note generated.\n")
    #print(note)


    return note
#### get the score 
def get_score_from_llm(draft_note: str, final_note: str) -> float:
    prompt = generate_score_prompt(draft_note, final_note)

    response = client.chat.completions.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}],
        temperature=0
    )

    score_text = response.choices[0].message.content.strip()

    try:
        return float(score_text)
    except ValueError:
        return -1.0

# --- MAIN ---
def main():
    # Step 1: Transcribe (replace with actual audio if needed)
    # transcription = transcribe_audio("audio_1.mp3")
    transcription = "Good morning, how can I help you today? Hello, doctor. Since last night, I've had abdominal pain, vomiting, and diarrhea. I'm not feeling well. I'm sorry to hear that. How many times have you vomited or had diarrhea since the symptoms started? I vomited about three times and gone to the bathroom maybe six times. It all started around 11 PM. Have you had any fever or chills? Yes, I had a fever this morning. I think it reached 38 degrees Celsius. Have you noticed any blood in your stools or vomit? No, just very watery and yellowish. Did you eat anything outside the house in the last 24 hours? Maybe something that didn't seem right? I had lunch at a restaurant yesterday. I ate chicken and rice, but it tasted a bit strange. I see. Do you have any significant medical history? Are you on any regular medications? No, I'm generally healthy. I'm only allergic to penicillin. Okay, have you been able to stay hydrated? Are you drinking water or oral rehydration? I've tried drinking."

    # Step 2: Generate and evaluate prompts
    for version in ["v1", "v2", "v3"]:
        prompt = generate_prompt(version, transcription)
        print("testing **** ",prompt)
        note = generate_note(prompt, prompt_version=version)
        print(f"\n Output for Prompt {version}:\n{note}")
        #print(f"\n Output for Prompt {version}",prompt)
        print("\n" + "="*50 + "\n")

if __name__ == "__main__":
    main()
