from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage, SourceUser, SourceGroup, SourceRoom, TemplateSendMessage, ConfirmTemplate, MessageAction, ButtonsTemplate, ImageCarouselTemplate, ImageCarouselColumn, URIAction, PostbackAction, DatetimePickerAction, CameraAction, CameraRollAction, LocationAction, CarouselTemplate, CarouselColumn, PostbackEvent, StickerMessage, StickerSendMessage, LocationMessage, LocationSendMessage, ImageMessage, VideoMessage, AudioMessage, FileMessage, UnfollowEvent, FollowEvent, JoinEvent, LeaveEvent, BeaconEvent, MemberJoinedEvent, MemberLeftEvent, FlexSendMessage, BubbleContainer, ImageComponent, BoxComponent, TextComponent, IconComponent, ButtonComponent, SeparatorComponent, QuickReply, QuickReplyButton, ImageSendMessage


class BotApi(LineBotApi):

    def __init__(self, access_token, channel_secret):
        super().__init__(access_token)
        self.web_handler = (channel_secret)

    @property
    def web_handler(self):
        return self._web_handler

    @web_handler.setter
    def web_handler(self, secret):
        self._web_handler = WebhookHandler(secret)

    def exception(self):
        return InvalidSignatureError

    def reply_text_message(self, token, msg):
        text_send_msg = TextSendMessage(msg)
        self.reply_message(token, text_send_msg)

    def reply_img_message(self, token):
        img_message = ImageSendMessage(
            original_content_url='https://upload.wikimedia.org/wikipedia/commons/thumb/b/b6/Chateaubriand_roast.jpg/800px-Chateaubriand_roast.jpg',
            preview_image_url='https://upload.wikimedia.org/wikipedia/commons/thumb/b/b6/Chateaubriand_roast.jpg/800px-Chateaubriand_roast.jpg'
        )
        self.reply_message(token, img_message)

    def reply_sticker_message(self, token, package_id, sticker_id):
        sticker_msg = MessageTemplate.get_sticker_msg(package_id, sticker_id)
        self.reply_message(token, sticker_msg)

    def reply_carousel_message(self, token):
        carousel_data = MessageTemplate.get_carousel_template()
        carousel_msg = MessageTemplate.get_carousel_msg(carousel_data)
        self.reply_message(token, carousel_msg)


class MessageTemplate():
    def __init__():
        pass

    def get_text_msg(msg):
        return TextSendMessage(msg)

    def get_sticker_msg(package_id, sticker_id):
        return StickerSendMessage(
            package_id,
            sticker_id
        )

    def get_carousel_msg(carousel_data):
        columns = []
        for item in carousel_data:
            columns.append(CarouselColumn(
                thumbnail_image_url=item["img"],
                title=item["title"],
                text=item["text"],
                actions=item["actions"]
            ))

        alt_text = 'carousel Template'
        template = CarouselTemplate(columns)

        return TemplateSendMessage(alt_text, template)

    def get_carousel_template():

        carousel_data = [
            {"img": "https://upload.wikimedia.org/wikipedia/commons/thumb/9/9a/Big_Mac_hamburger.jpg/800px-Big_Mac_hamburger.jpg",
             "title": "this is menu1",
             "text": "descrirption1",
             "actions": [
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
                 )]
             }, {
                "img": "https://upload.wikimedia.org/wikipedia/commons/thumb/9/9a/Big_Mac_hamburger.jpg/800px-Big_Mac_hamburger.jpg",
                "title": "this is menu1",
                "text": "descrirption1",
                "actions": [
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
            }
        ]
        return carousel_data
