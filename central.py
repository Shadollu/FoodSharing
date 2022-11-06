from flask import Flask, request, abort
from linebot_service.core import BotApi, MessageEvent, TextMessage, StickerMessage
import configparser


def gateway(bot):
    app = Flask(__name__)

    # LINE 聊天機器人的基本資料
    handler = bot.web_handler

    @app.route("/", methods=['POST'])
    def callback():

        signature = request.headers['X-Line-Signature']

        body = request.get_data(as_text=True)
        app.logger.info("Request body: " + body)

        try:
            print(body, signature)
            handler.handle(body, signature)

        except bot.exception():
            abort(400)

        return 'OK'

    @handler.add(MessageEvent, message=TextMessage)
    def handle_text_message(event):

        try:
            bot.text_process(event)
        except bot.exception():
            abort(401)

    @handler.add(MessageEvent, message=StickerMessage)
    def handle_sticker_message(event):

        package_id = event.message.package_id
        sticker_id = event.message.sticker_id

        bot.reply_sticker_message(event.reply_token, package_id, sticker_id)

    return app


if __name__ == "__main__":
    config = configparser.ConfigParser()
    config.read('config.ini')
    token = config.get('line-bot', 'channel_access_token')
    secret = config.get('line-bot', 'channel_secret')

    app = gateway(BotApi(token, secret))
    app.debug = True
    app.run()
