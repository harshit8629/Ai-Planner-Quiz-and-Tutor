from flask import Flask, render_template, request, jsonify, session
import os
from dotenv import load_dotenv
from planner import generate_study_plan
from ai_services import generate_quiz, get_chat_response

load_dotenv()
app = Flask(__name__)
app.secret_key = "studyai-super-secret-2025"

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/planner")
def planner_page():
    return render_template("planner.html")

@app.route("/quiz")
def quiz_page():
    return render_template("quiz.html")

@app.route("/chat")
def chat_page():
    if "chat_history" not in session:
        session["chat_history"] = []
    return render_template("chat.html")

# ==================== API ENDPOINTS ====================

@app.route("/generate_plan", methods=["POST"])
def generate_plan():
    data = request.get_json()
    plan = generate_study_plan(
        data["subjects"],
        data["exam_date"],
        int(data["daily_hours"])
    )
    return jsonify(plan)

@app.route("/generate_quiz", methods=["POST"])
def generate_quiz_route():
    topic = request.get_json()["topic"]
    quiz = generate_quiz(topic)
    return jsonify(quiz)

@app.route("/chat", methods=["POST"])
def chat_route():
    user_message = request.get_json()["message"]
    
    if "chat_history" not in session:
        session["chat_history"] = []
    
    # Add user message
    session["chat_history"].append({"role": "user", "content": user_message})
    
    # Get AI response
    response = get_chat_response(session["chat_history"])
    
    # Add assistant message
    session["chat_history"].append({"role": "assistant", "content": response})
    
    return jsonify({"response": response})

if __name__ == "__main__":
    print("🚀 StudyAI running at http://127.0.0.1:5000")
    app.run(debug=True)