from flask import Flask, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage, ImageSendMessage, TemplateSendMessage, CarouselTemplate, CarouselColumn, PostbackAction, MessageAction, URIAction, StickerSendMessage
import configparser
import random

app = Flask(__name__)

# LINE 聊天機器人的基本資料
config = configparser.ConfigParser()
config.read('config.ini')

line_bot_api = LineBotApi(config.get('line-bot', 'channel_access_token'))
handler = WebhookHandler(config.get('line-bot', 'channel_secret'))


# 接收 LINE 的資訊
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
def pretty_echo(event):
    # 不想動腦 -> Image message
    if event.message.text == '不想動腦':
        # 呼叫get_img_message function 取得Image message 訊息物件
        reply_obj = get_img_message()

    # 自選某式 -> Template message：Carousel template
    elif event.message.text == '自選某式':
        # 呼叫 get_carousel_template function 取得 carousel template 物件
        reply_obj = get_carousel_template()

    # 選購食材 -> Sticker message
    elif event.message.text == '添購食材':
        # 呼叫get_sticker_template function 取得 sticker message 物件
        reply_obj = get_sticker_template()

    else:
        # 學你說話外加彩色的愛
        pretty_note = '❤🧡💛💚💙💜🤎🖤🤍'
        pretty_text = ''

        for i in event.message.text:
            pretty_text += i
            pretty_text += random.choice(pretty_note)

        # 原本的寫法是直接assign到reply_message當中,改成放在reply_obj
        reply_obj = TextSendMessage(pretty_text)

    # 第一個參數 = 要回應的token, 第二個參數 = 要回的訊息物件(訊息物件有很多種,根據不同Template有不同的物件)
    line_bot_api.reply_message(
        event.reply_token,
        reply_obj
    )


def get_img_message():
    '''
    參考SDK文件, 第六行的Import 多加 ImageSendMessage 這個功能
    在這個function建構這個功能 並 return 回去

    @param
    original_content_url = 點開圖片後的詳細大圖
    preview_image_url = 在對話視窗內的預覽

    所以可以放不同張照片,做出預覽圖跟詳細大圖不一樣的效果
    '''
    image_message = ImageSendMessage(
        original_content_url='https://upload.wikimedia.org/wikipedia/commons/thumb/b/b6/Chateaubriand_roast.jpg/800px-Chateaubriand_roast.jpg',
        preview_image_url='https://upload.wikimedia.org/wikipedia/commons/thumb/b/b6/Chateaubriand_roast.jpg/800px-Chateaubriand_roast.jpg'
    )

    return image_message


def get_carousel_template():
    '''
    參考SDK文件, 第六行的Import 多加 TemplateSendMessage 這個功能(後面會發現很多Template都用這個,因為它們都繼承這個功能)
    在這個function建構這個功能 並 return 回去

    @param
    alt_text = 顯示失敗時出現的替代文字
    template = 要調用的Template,以這個範例我們使用CarouselTemplate (請記得一樣要Import)

    CarouselTemplate 的參數:
    這個功能只需要放一個陣列型別的參數,
    陣列裡面的資料都是 CaruselColumn (請記得一樣要Import)

    CaruselColumn 的參數:
        thumbnail_image_url = 預覽圖
        title = 標題
        text = 描述
        actions = 陣列,裡面可以放多個action (就是下方的選項,你可以讓按鈕發postback or 訊息 or 轉導網站, 請參考sdk內的 action部分)
    '''

    carousel_template_message = TemplateSendMessage(
        alt_text='Carousel template',
        template=CarouselTemplate(
            columns=[
                CarouselColumn(
                    thumbnail_image_url='https://upload.wikimedia.org/wikipedia/commons/thumb/9/9a/Big_Mac_hamburger.jpg/800px-Big_Mac_hamburger.jpg',
                    title='this is menu1',
                    text='description1',
                    actions=[
                        PostbackAction(
                            label='postback1',
                            display_text='postback text1',
                            data='action=buy&itemid=1'
                        ),
                        MessageAction(
                            label='message1',
                            text='message text1'
                        ),
                        URIAction(
                            label='uri1',
                            uri='http://example.com/1'
                        )
                    ]
                ),
                CarouselColumn(
                    thumbnail_image_url='https://upload.wikimedia.org/wikipedia/commons/thumb/f/f7/McDonald%27s_Filet-O-Fish_sandwich_%281%29.jpg/1024px-McDonald%27s_Filet-O-Fish_sandwich_%281%29.jpg',
                    title='this is menu2',
                    text='description2',
                    actions=[
                        PostbackAction(
                            label='postback2',
                            display_text='postback text2',
                            data='action=buy&itemid=2'
                        ),
                        MessageAction(
                            label='message2',
                            text='message text2'
                        ),
                        URIAction(
                            label='uri2',
                            uri='http://example.com/2'
                        )
                    ]
                )
            ]
        )
    )

    return carousel_template_message


def get_sticker_template():
    '''
    參考SDK文件, 第六行的Import 多加 StickerSendMessage 這個功能
    在這個function建構這個功能 並 return 回去

    @param
    package_id = 哪一套貼圖的 id (line也沒提供 你只能自己踹 用數字去玩玩看吧)
    sticker_id = 第幾張貼圖

    這個付費貼圖不能用,所以不能用懶得鳥的貼圖
    '''

    sticker_message = StickerSendMessage(
        package_id='1',
        sticker_id='12'
    )

    return sticker_message


if __name__ == "__main__":
    app.debug = True
    app.run()
