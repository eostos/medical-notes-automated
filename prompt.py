
PROMPT_LIBRARY = {
    "v1":"You are a clinical documentation assistant. Your task is to generate a well-structured SOAP (Subjective, Objective, Assessment, Plan) consultation note from the following medical consultation transcript.\n\n"
        "Ensure each section is clearly labeled and the content is concise, accurate, and relevant.\n\n"
        "Transcript:\n",
    "v2": "Summarise this conversation with diagnosis and treatment plan:\n\n",
    "v3": "Create a structured clinical note based on the following patient-doctor dialogue:\n\n",
    "v4":"You are a clinical documentation assistant.\n\n"
            "Generate a SOAP note using bullet points under each section. Use the following structure:\n\n"
            "Subjective:\n"
            "• [Summarize the patient's symptoms and concerns as reported]\n\n"
            "Examination:\n"
            "• [Summarize relevant physical exam findings or vitals]\n\n"
            "Assessment:\n"
            "• [Write a concise clinical impression or diagnosis]\n\n"
            "Plan:\n"
            "• [List tests, medications, advice, and follow-up recommendations]\n\n"
            "Be concise, medically accurate, and use professional clinical language.\n\n",
    "score": "You are a clinical documentation evaluator.\n\n"
             "Your task is to compare two versions of a medical SOAP note: an initial draft generated from transcription and a final version edited by a clinician.\n\n"
             "Draft Note:\n\"\"\"{draft_note}\"\"\"\n\n"
             "Final Note:\n\"\"\"{final_note}\"\"\"\n\n"
             "Evaluate the draft in terms of:\n"
             "- Accuracy: Does the draft capture the correct medical facts?\n"
             "- Completeness: Are all relevant findings and plans included?\n"
             "- Clinical correctness: Is the content medically sound?\n\n"
             "Give a single score from 0 to 100 based on how close the draft is to the final version:\n"
             "- 100 = identical and perfect\n"
             "- 80–99 = minor edits (grammar, formatting, slight corrections)\n"
             "- 50–79 = significant clinical or structural changes\n"
             "- < 50 = mostly incorrect or incomplete\n\n"
             "Return only the numerical score. Do not include any explanation."
            

}

def generate_prompt(version, transcript):
    base_prompt = PROMPT_LIBRARY.get(version)
    if not base_prompt:
        raise ValueError(f"Prompt version '{version}' is not defined.")
    return f"{base_prompt}{transcript}"

def generate_score_prompt(draft_note, final_note):
    base_prompt = PROMPT_LIBRARY.get("score")
    if not base_prompt:
        raise ValueError("Scoring prompt template is not defined.")
    return base_prompt.format(draft_note=draft_note, final_note=final_note)