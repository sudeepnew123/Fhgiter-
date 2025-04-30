from flask import Flask, request
import telegram
import os
import random
import requests

TOKEN = "8134414526:AAEETxc6-4gRx2-2qGmNKjstSVyMMUPAPDI"
bot = telegram.Bot(token=TOKEN)

app = Flask(__name__)

ACTION_GIFS = {
    "slap": [
        "https://media.giphy.com/media/Gf3AUz3eBNbTW/giphy.gif"
    ],
    "punch": [
        "https://media.giphy.com/media/l3YSimA8CV1k41b1u/giphy.gif"
    ],
    "kick": [
        "https://media.giphy.com/media/xUNd9HZq1itMkiK652/giphy.gif"
    ],
    "sui": [
        "https://media.giphy.com/media/3o6MbjYgCUNquV98bK/giphy.gif"
    ],
    "juta": [
        "https://media.giphy.com/media/3o6gDWzmAzrpi5DQU8/giphy.gif"
    ],
    "burn": [
        "https://media.giphy.com/media/l0Exk8EUzSLsrErEQ/giphy.gif"
    ],
    "headshot": [
        "https://media.giphy.com/media/JqDeI2yjpSRgdh35oe/giphy.gif"
    ],
    "roast": [
        "https://media.giphy.com/media/xUPGcjGy8I928yIlAQ/giphy.gif"
    ],
    "ghusa": [
        "https://media.giphy.com/media/3o6Zt481isNVuQI1l6/giphy.gif"
    ],
    "smash": [
        "https://media.giphy.com/media/3oEjHWzCySNEkZH2yk/giphy.gif"
    ],
    "hit": [
        "https://media.giphy.com/media/MF3fYwqlGDzG0/giphy.gif"
    ],
    "throw": [
        "https://media.giphy.com/media/3oz8xLd9DJq2l2VFtu/giphy.gif"
    ],
    "hug": [
        "https://media.giphy.com/media/3o7TKxu6lO35jcVxgk/giphy.gif"
    ],
    "miss": [
        "https://media.giphy.com/media/l0NwYbVJ2Mum2wss4/giphy.gif"
    ],
    "kiss": [
        "https://media.giphy.com/media/9TdbFQnYtuHiM/giphy.gif"
    ],
    "gun": [
        "https://media.giphy.com/media/46JvxX7n4CpYubsmr6/giphy.gif"
    ]
}

ACTION_TEXTS = {
    "slap": "ne {target} ko zor ka thappad maara!",
    "punch": "ne {target} ke muh pe mukka jada!",
    "kick": "ne {target} ko laat maar di!",
    "sui": "ne {target} ko sui chubha di!",
    "juta": "ne {target} ke sar pe juta maara!",
    "burn": "ne {target} ko jala daala!",
    "headshot": "ne {target} ko headshot de diya!",
    "roast": "ne {target} ki full roast kar di!",
    "ghusa": "ne {target} ke pet me ghusa de maara!",
    "smash": "ne {target} ko zor se smash kar diya!",
    "hit": "ne {target} ko dho diya!",
    "throw": "ne {target} ko hawa me uchhaal diya!",
    "hug": "ne {target} ko hug diya!",
    "miss": "ne {target} ko miss kiya!",
    "kiss": "ne {target} ko pyaar se kiss diya!",
    "gun": "ne {target} ko goli maar diya!"
}

def is_valid_gif(url):
    try:
        response = requests.head(url, allow_redirects=True)
        return response.status_code == 200 and "image" in response.headers.get("Content-Type", "")
    except:
        return False

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
    mention_text = None

    if message.reply_to_message:
        target = message.reply_to_message.from_user
        target_user = target.first_name
        mention_text = f'<a href="tg://user?id={target.id}">{target_user}</a>'
    elif message.entities:
        for entity in message.entities:
            if entity.type == "mention":
                username_mention = message.text[entity.offset:entity.offset + entity.length]
                target_user = username_mention
                mention_text = username_mention
                break

    if not target_user:
        bot.send_message(chat_id=message.chat.id, text="Kisi ko reply ya tag karo bhai!")
        return "ok"

    valid_gifs = [url for url in ACTION_GIFS[command] if is_valid_gif(url)]
    if not valid_gifs:
        bot.send_message(chat_id=message.chat.id, text="Koi valid GIF nahi mila!")
        return "ok"

    gif_url = random.choice(valid_gifs)
    action_text = ACTION_TEXTS[command].format(target=mention_text)
    final_msg = f"<b>{actor}</b> {action_text}"

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
