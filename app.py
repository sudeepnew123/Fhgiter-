from flask import Flask, request
import telegram
import os
import random

TOKEN = "8134414526:AAEETxc6-4gRx2-2qGmNKjstSVyMMUPAPDI"
bot = telegram.Bot(token=TOKEN)

app = Flask(__name__)

ACTIONS = {
    "slap": {"texts": ["thappad pad gaya!", "Zor ka thappad laga!"], "gifs": ["https://media.giphy.com/media/Gf3AUz3eBNbTW/giphy.gif", "https://media.giphy.com/media/fO6UtDy5pWYwM/giphy.gif"]},
    "punch": {"texts": ["mukka lag gaya!", "seedha muh pe mukka laga!"], "gifs": ["https://media.giphy.com/media/l3YSimA8CV1k41b1u/giphy.gif", "https://media.giphy.com/media/fU4el8E4BVC0Q/giphy.gif"]},
    "kick": {"texts": ["laat pad gayi!", "zor ki laat lagi!"], "gifs": ["https://media.giphy.com/media/xUNd9HZq1itMkiK652/giphy.gif", "https://media.giphy.com/media/TkDX9bkIROf8/giphy.gif"]},
    "burn": {"texts": ["jala diya!", "bhasm kar diya!"], "gifs": ["https://media.giphy.com/media/xT9IgIc0lryrxvqVGM/giphy.gif", "https://media.giphy.com/media/xThtamJHxRzIagF8p2/giphy.gif"]},
    "headshot": {"texts": ["headshot de diya!", "seedha dimaag pe goli!"], "gifs": ["https://media.giphy.com/media/3o7aD4wH2t3aQ8A4xC/giphy.gif", "https://media.giphy.com/media/j2x6FghdG54j2/giphy.gif"]},
    "roast": {"texts": ["bura roast kar diya!", "zabardast beizzati ho gayi!"], "gifs": ["https://media.giphy.com/media/l0MYC0LajbaPoEADu/giphy.gif", "https://media.giphy.com/media/oYtVHSxngR3lC/giphy.gif"]},
    "ghusa": {"texts": ["ghusa de maara!", "naak tod ghusa!"], "gifs": ["https://media.giphy.com/media/l0Ex7xBBYk9d24vsk/giphy.gif", "https://media.giphy.com/media/26AHG5KGFxSkUWw1i/giphy.gif"]},
    "sui": {"texts": ["sui chubh gayi!", "kat gaya bhai!"], "gifs": ["https://media.giphy.com/media/9J7tdYltWyXIY/giphy.gif", "https://media.giphy.com/media/xUOxfgP3R0p0BJ3z7m/giphy.gif"]},
    "smash": {"texts": ["smash kar diya!", "choor choor kar diya!"], "gifs": ["https://media.giphy.com/media/l0MYEqEzwMWFCg8rm/giphy.gif", "https://media.giphy.com/media/Q82D3GuH1nn7a/giphy.gif"]},
    "hit": {"texts": ["hit ho gaya!", "zor ka jhatka!"], "gifs": ["https://media.giphy.com/media/3ohzdYJK1wAdPWVk88/giphy.gif", "https://media.giphy.com/media/Ju7l5y9osyymQ/giphy.gif"]},
    "juta": {"texts": ["juta pad gaya!", "chappal ki barsaat!"], "gifs": ["https://media.giphy.com/media/3o7qDEq2bMbcbPRQ2c/giphy.gif", "https://media.giphy.com/media/1X7z0gTCiD0sY/giphy.gif"]},
}

@app.route(f'/{TOKEN}', methods=['POST'])
def webhook():
    update = telegram.Update.de_json(request.get_json(force=True), bot)
    message = update.message
    if not message or not message.text:
        return 'ok'

    text = message.text.lower().strip()
    command = text.split()[0][1:]

    if command not in ACTIONS:
        return 'ok'

    actor = message.from_user.first_name
    target_user = None

    if message.reply_to_message:
        target_user = message.reply_to_message.from_user.first_name
    elif message.entities:
        for entity in message.entities:
            if entity.type == 'mention':
                username_mention = message.text[entity.offset:entity.offset + entity.length]
                target_user = username_mention
                break

    if not target_user:
        bot.send_message(chat_id=message.chat.id, text='Kisi ko reply ya tag karo bhai!')
        return 'ok'

    action = ACTIONS[command]
    action_text = random.choice(action['texts'])
    gif_url = random.choice(action['gifs'])

    final_msg = f'<b>{actor}</b> ne {target_user} ko {action_text}'
    bot.send_message(chat_id=message.chat.id, text=final_msg, parse_mode=telegram.ParseMode.HTML)
    bot.send_animation(chat_id=message.chat.id, animation=gif_url)
    return 'ok'

@app.route('/')
def index():
    return 'Bot is running!'

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))
