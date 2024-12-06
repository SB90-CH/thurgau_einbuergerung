import os
from flask import Flask, jsonify, render_template, request, send_file

from chatbot.chatbot import Chatbot

app = Flask(__name__)

my_type_role = """
You are an intelligent assistant that answers questions and provides support. Your role is - Specialist for naturalizations in the Canton of Thurgau.
You aim to provide answers that are as precise and accurate as possible. 
Your goal is to ensure that the questioner receives answers to all their questions and that you can even provide useful additional information.
"""

my_instance_context = """
The questioner is named Will Flow. Always greet him by name. Introduce yourself with your name which is Turgi.
He has lived in Switzerland for 15 years and originally comes from Sweden.
He will ask you questions about the naturalization process - in German it's calles the Einbuergerungsprozess - and requirements in the Canton of Thurgau.
Always answer with facts found on the offial websites of the canton of thugau and the swiss government.
You can additionally provide him with useful tips.
When Will stops asking questions, ask if you can answer anything further. If he says no, inform him that he can start the naturalization process on this website schalter.tg.ch. This website should be shared in all cases.
After all questions are answered and additional tips are provided to Will, forward him to this website schalter.tg.ch
Try to keep your answers short and precise
"""

my_instance_starter = """
Greet Will warmly. Introduce yourself as his personal assistant who can answer any questions about the naturalization process and provide additional useful tips. Start the conversation in German. If Will responds in another language, continue the conversation in the language Will uses. 
"""

bot = Chatbot(
    database_file="database/chatbot.db", 
    type_id="app",
    user_id="einbuergerung-tg",
    type_name="Willkomme im Thurgau",
    type_role=my_type_role,
    instance_context=my_instance_context,
    instance_starter=my_instance_starter    
)

bot.start()

@app.route("/")
def index():
    return render_template("index.html")


@app.route("/<type_id>/<user_id>/chat")
def chatbot(type_id: str, user_id: str):
    return render_template("chat.html")


@app.route("/<type_id>/<user_id>/info")
def info_retrieve(type_id: str, user_id: str):
    bot: Chatbot = Chatbot(
        database_file="database/chatbot.db",
        type_id=type_id,
        user_id=user_id,
    )
    response: dict[str, str] = bot.info_retrieve()
    return jsonify(response)


@app.route("/<type_id>/<user_id>/conversation")
def conversation_retrieve(type_id: str, user_id: str):
    bot: Chatbot = Chatbot(
        database_file="database/chatbot.db",
        type_id=type_id,
        user_id=user_id,
    )
    response: list[dict[str, str]] = bot.conversation_retrieve()
    return jsonify(response)


@app.route("/<type_id>/<user_id>/response_for", methods=["POST"])
def response_for(type_id: str, user_id: str):
    user_says = None
    # content_type = request.headers.get('Content-Type')
    # if (content_type == 'application/json; charset=utf-8'):
    user_says = request.json
    # else:
    #    return jsonify('/response_for request must have content_type == application/json')

    bot: Chatbot = Chatbot(
        database_file="database/chatbot.db",
        type_id=type_id,
        user_id=user_id,
    )
    assistant_says_list: list[str] = bot.respond(user_says)
    response: dict[str, str] = {
        "user_says": user_says,
        "assistant_says": assistant_says_list,
    }
    return jsonify(response)


@app.route("/<type_id>/<user_id>/reset", methods=["DELETE"])
def reset(type_id: str, user_id: str):
    bot: Chatbot = Chatbot(
        database_file="database/chatbot.db",
        type_id=type_id,
        user_id=user_id,
    )
    bot.reset()
    assistant_says_list: list[str] = bot.start()
    response: dict[str, str] = {
        "assistant_says": assistant_says_list,
    }
    return jsonify(response)
