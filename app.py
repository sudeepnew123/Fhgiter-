from flask import Flask, request
import telegram
import os
import random
import re

TOKEN = "8134414526:AAEETxc6-4gRx2-2qGmNKjstSVyMMUPAPDI"
bot = telegram.Bot(token=TOKEN)

app = Flask(__name__)

ACTION_GIFS = {
    "slap": [
        "https://media.giphy.com/media/Gf3AUz3eBNbTW/giphy.gif",
        "https://media.giphy.com/media/fO6UtDy5pWYwM/giphy.gif"
    ],
    "punch": [
        "https://media.giphy.com/media/l3YSimA8CV1k41b1u/giphy.gif",
        "https://media.giphy.com/media/fU4el8E4BVC0Q/giphy.gif"
    ],
    "kick": [
        "https://media.giphy.com/media/xUNd9HZq1itMkiK652/giphy.gif",
        "https://media.giphy.com/media/TkDX9bkIROf8/giphy.gif"
    ]
}

ACTION_TEXTS = {
    "slap": "ne {target} ko zor ka thappad maara!",
    "punch": "ne {target} ko seedha muh pe mukka maara!",
    "kick": "ne {target} ko laat maar di!"
}

@app.route(f"/{TOKEN}", methods=["POST"])
def webhook():
    update = telegram.Update.de_json(request.get_json(force=True), bot)
    message = update.message

    if not message or not message.text:
        return "ok"

    text = message.text.lower().strip()
    command = text.split()[0][1:]

    if command not in ACTION_GIFS:
        return "ok"

    actor = message.from_user.first_name
    target_user = None

    # Case 1: Reply
    if message.reply_to_message:
        target_user = message.reply_to_message.from_user.first_name

    # Case 2: Mention like @username
    elif message.entities:
        for entity in message.entities:
            if entity.type == "mention":
                username_mention = message.text[entity.offset:entity.offset + entity.length]
                target_user = username_mention
                break

    # No valid target
    if not target_user:
        bot.send_message(chat_id=message.chat.id, text="Kisi ko reply ya tag karo bhai!")
        return "ok"

    action_text = ACTION_TEXTS[command].format(target=target_user)
    gif_url = random.choice(ACTION_GIFS[command])

    final_msg = f"<b>{actor}</b> {action_text}"

    # Single message with GIF + caption
    bot.send_animation(
        chat_id=message.chat.id,
        animation=gif_url,
        caption=final_msg,
        parse_mode=telegram.ParseMode.HTML
    )

    return "ok"

@app.route("/")
def index():
    return "Bot is running!"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
