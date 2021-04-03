from typing import List
from mohy.entities import Question
from flask import Flask, request, jsonify
from mohy.user_services import UserApplicationService

app = Flask(__name__)

app_service = UserApplicationService()


@app.route("/question", methods=["POST"])
def create_question():
    data = request.json
    print(data)
    try:
        app_service.create_question(
            question_text=data["question"], question_type=data["question_type"], create_user_name=data["user_name"])
    except Exception as e:
        print("error")
        print(e)
        return "Error", 500
    return "Success", 200


@app.route("/question/<question_id>", methods=["GET"])
def describe_question(question_id):
    try:
        question = app_service.describe_question(question_id)
    except KeyError:
        return "Question Not Found", 500
    return jsonify(
        {
            "question_id": question.question_id.question_id,
            "question_type": question.question_type.value,
            "create_user": question.create_user.name,
            "text": question.text,
            "valid_choice": ", ".join(question.valid_choice),
            "created_at": question.created_at.strftime("%Y-%m-%d %H:%M:%S"),
            "last_modified_at": question.last_modified_at.strftime("%Y-%m-%d %H:%M:%S"),
            "deleted_at": "" if question.deleted_at is None else question.deleted_at.strftime("%Y-%m-%d %H:%M:%S"),
        }
    ), 200


@app.route("/questions", methods=["GET"])
def list_question():
    questions: List[Question] = app_service.list_question()
    print(questions)
    return jsonify([{
        "question_id": q.question_id.question_id,
        "question_type": q.question_type.value,
        "text": q.text} for q in questions.values()]), 200


@app.route("/execution", methods=["POST"])
def create_execution():
    data = request.json
    try:
        app_service.create_execution(data["question_id"], data["user_name"])
    except Exception:
        return "Error", 500
    return "Success", 200


@app.route("/answer", methods=["POST"])
def answer_question():
    data = request.json
    try:
        app_service.answer_question(data["execution_id"], data["answer"], data["user_name"])
    except Exception:
        return "Error", 500
    return "Success", 200


if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=80)
