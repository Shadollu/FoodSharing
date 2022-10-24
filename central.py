import random
from flask import Flask, request, abort
from linebot_service.core import BotApi, WebhookHandler, InvalidSignatureError, MessageEvent, TextMessage, MessageAction, URIAction, PostbackAction, StickerMessage

app = Flask(__name__)
app.config.from_object('config')

# LINE 聊天機器人的基本資料
bot = BotApi(app.config['CHANNEL_ACCESS_TOKEN'])
handler = WebhookHandler(app.config['CHANNEL_SECRET'])


@app.route("/", methods=['POST'])
def callback():

    signature = request.headers['X-Line-Signature']

    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    try:
        print(body, signature)
        handler.handle(body, signature)

    except InvalidSignatureError:
        abort(400)

    return 'OK'


@handler.add(MessageEvent, message=TextMessage)
def handle_text_message(event):
    if event.message.text == '不想動腦':
        bot.reply_img_message(event.reply_token)

    # 自選某式 -> Template message：Carousel template
    elif event.message.text == '自選某式':
        bot.reply_carousel_message(event.reply_token)

    # 選購食材 -> Sticker message
    elif event.message.text == '添購食材':
        package_id = 1
        sticker_id = 12
        bot.reply_sticker_message(event.reply_token, package_id, sticker_id)

    else:
        # 學你說話外加彩色的愛
        pretty_note = '❤🧡💛💚💙💜🤎🖤🤍'
        pretty_text = ''

        for i in event.message.text:
            pretty_text += i
            pretty_text += random.choice(pretty_note)

        bot.reply_text_message(event.reply_token, pretty_text)


@handler.add(MessageEvent, message=StickerMessage)
def handle_sticker_message(event):

    package_id = event.message.package_id
    sticker_id = event.message.sticker_id

    bot.reply_sticker_message(event.reply_token, package_id, sticker_id)


if __name__ == "__main__":
    app.debug = True
    app.run()
