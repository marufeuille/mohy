from typing import List
from mohy.entities import Question, User
from flask import Flask, request, jsonify
from mohy.user_services import UserApplicationService

app = Flask(__name__)

app_service = UserApplicationService()


def list_question():
    questions: List[Question] = app_service.list_question()
    print(questions)
    return jsonify([{
        "question_id": q.question_id.question_id,
        "question_type": q.question_type.value,
        "text": q.text} for q in questions.values()]), 200


def create_question(question_text: str, question_type: str, user_name: str):
    try:
        question_id = app_service.create_question(
            question_text=question_text, question_type=question_type, create_user_name=user_name)
    except Exception as e:
        print("error")
        print(e)
        return "Error", 500
    return f"Created {question_id.question_id}", 200


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
            "question_text": question.text,
            "valid_choice": ", ".join(question.valid_choice),
            "created_at": question.created_at.strftime("%Y-%m-%d %H:%M:%S"),
            "last_modified_at": question.last_modified_at.strftime("%Y-%m-%d %H:%M:%S"),
            "deleted_at": "" if question.deleted_at is None else question.deleted_at.strftime("%Y-%m-%d %H:%M:%S"),
        }
    ), 200


def list_execution():
    executions: List[Question] = app_service.list_execution().copy()
    print(executions)
    return jsonify([{
        "execution_id": e.execution_id.execution_id,
        "question": e.question.text
    } for e in executions.values()]), 200


def create_execution(question_id: str, user_name: str):
    try:
        execution_id = app_service.create_execution(question_id, user_name)
    except Exception:
        return "Error", 500
    return f"Created {execution_id.execution_id}", 200


def answer_question(execution_id: str, answer: str, user_name: str):
    try:
        answer_id = app_service.answer_question(execution_id, answer, user_name)
    except Exception:
        return "Error", 500
    return f"Created {answer_id.answer_id}", 200


def describe_execution(execution_id: str):
    try:
        execution = app_service.describe_execution(execution_id)
    except Exception:
        return "Error", 500
    return jsonify(
        {
            "execution_id": execution.execution_id.execution_id,
            "question": execution.question.text,
            "answers": [[ans.text, ans.answering_user] for ans in execution.answers]
        }
    ), 200


@app.route("/slack_command", methods=["POST"])
def call_commands():
    data = request.form
    print(data)
    user_name = data.get("user_name")
    user_id = data.get("user_id")
    text = data.get("text").split(" ")
    if text[0] == "questions":
        if text[1] == "list":
            return list_question()
    elif text[0] == "question":
        if text[1] == "create":
            question_text = text[2]
            question_type = text[3] if len(text) > 3 else "FREE_TEXT"
            return create_question(question_text, question_type, user_name)
        elif text[1] == "describe":
            question_id = text[2]
            return describe_question(question_id)

    elif text[0] == "execution":
        if text[1] == "create":
            question_id = text[2]
            return create_execution(question_id, user_name)
        elif text[1] == "answer":
            execution_id = text[2]
            answer = text[3]
            return answer_question(execution_id, answer, user_name)
        elif text[1] == "describe":
            execution_id = text[2]
            return describe_execution(execution_id, user_name)

    elif text[0] == "executions":
        if text[1] == "list":
            return list_execution()


if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=80)
