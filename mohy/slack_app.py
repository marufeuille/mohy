import os
from slack_bolt import App
import json

from mohy.user_services import UserApplicationService

app = App(
    token=os.environ.get("SLACK_BOT_TOKEN"),
    signing_secret=os.environ.get("SLACK_SIGNING_SECRET")
)

app_service = UserApplicationService()


@app.shortcut("open-freetext-editor")
def open_freetext_question_editor_modal(ack, body, client):
    ack()
    with open("mohy/block/freetext.json") as f:
        view = json.loads(f.read())

    client.views_open(
        trigger_id=body["trigger_id"],
        view=view
    )


@app.view("create_freetext_view")
def handle_create_question(ack, body, client, view):

    team_domain = body["team"]["domain"]
    team_id = body["team"]["id"]
    username = body["user"]["username"]
    user_id = body["user"]["id"]
    question_string = view["state"]["values"]["question"]["question-action"]["value"]

    errors = {}
    if question_string is None:
        errors["block_c"] = "question string is empty"
    if len(errors) > 0:
        ack(response_action="errors", errors=errors)
        return

    ack()
    msg = ""
    try:
        app_service.create_question("FREE_TEXT", question_text=question_string, user_id=user_id,
                                    username=username, team_id=team_id, team_domain=team_domain)
        msg = "Successfully saved!"
    except Exception as e:
        msg = "There was an error with your submission"
    finally:
        client.chat_postMessage(channel=user_id, text=msg)


@app.shortcut("open-execution")
def open_execution_modal(ack, body, client):
    team_id = body["team"]["id"]
    user_id = body["user"]["id"]
    ack()
    with open("mohy/block/execution.json") as f:
        view = json.loads(f.read())

    template = {
        "text": {
            "type": "plain_text",
            "text": "",
            "emoji": True
        },
        "value": ""
    }
    view["blocks"][0]["accessory"]["options"] = []
    for q in app_service.get_questions(user_id=user_id, team_id=team_id):
        select = template.copy()
        select["text"]["text"] = q.text
        select["value"] = q.question_id
        view["blocks"][0]["accessory"]["options"].append(select)

    client.views_open(
        trigger_id=body["trigger_id"],
        view=view
    )


@app.view("create_execution")
def handle_create_execution(ack, body, client, view):

    team_domain = body["team"]["domain"]
    team_id = body["team"]["id"]
    username = body["user"]["username"]
    user_id = body["user"]["id"]
    question_id = view["state"]["values"]["select_question"]["select_question-action"]["selected_option"]["value"]
    channel_ids = view["state"]["values"]["select_channel"]["select_channel-action"]["selected_conversations"]

    ack()
    msg = ""
    try:
        question = app_service.get_question(question_id)
    except Exception as e:
        msg = "There was an error with your submission"
    finally:
        with open("mohy/block/freetext_answer.json") as f:
            blocks = json.loads(f.read())
        blocks[0]["text"]["text"] = f"*質問*: {question.text}"

        for channel_id in channel_ids:
            print(channel_id)
            client.chat_postMessage(channel=channel_id, blocks=blocks, text="test")


if __name__ == "__main__":
    app.start(port=int(os.environ.get("PORT", 80)))
