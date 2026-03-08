import google.generativeai as genai
import os
import json
from dotenv import load_dotenv

load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

# Use flash for speed + free tier
model = genai.GenerativeModel("gemini-3.1-flash-lite-preview")

def generate_quiz(topic):
    prompt = f"""Generate a quiz on the topic: "{topic}"
Exactly this structure — return ONLY valid JSON, no extra text/explanation:

{{
  "questions": [
    {{"type": "mcq", "question": "Question text", "options": ["A. opt1", "B. opt2", "C. opt3", "D. opt4"], "correct": "A", "explanation": "Why correct"}},
    ... (exactly 4 MCQ)
    {{"type": "short", "question": "Short answer question", "answer": "Model answer", "explanation": "Explanation"}}
    ... (exactly 2 short)
  ]
}}
"""
    try:
        response = model.generate_content(prompt)
        text = response.text.strip()
        # Gemini sometimes wraps in ```json ... ```
        if text.startswith("```json"):
            text = text.split("```json")[1].split("```")[0].strip()
        return json.loads(text)
    except Exception as e:
        return {"error": f"Quiz generation failed: {str(e)}"}

def get_chat_response(history):
    # Convert to Gemini format
    gemini_history = []
    for msg in history:
        role = "user" if msg["role"] == "user" else "model"
        gemini_history.append({"role": role, "parts": [msg["content"]]})

    chat = model.start_chat(history=gemini_history)

    # System instruction (put in first message or as safety setting if needed)
    response = chat.send_message(
        "You are a friendly, patient high-school level tutor. Explain simply, use examples, be encouraging."
    )
    return response.text