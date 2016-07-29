# -*- coding: utf-8 -*-
from flask import Flask
app = Flask(__name__)
from flask import request
from FBBlib.fbbot import FBBot
from FBBlib.order import FBOrder
from FBBlib.attachment import FBAttachment
from FBBlib.AirlineFlightUpdate import AirlineFlightUpdate
from FBBlib.AirlineCheckin import AirlineCheckin
#import FBBlib

token = ""
verify_token = ""

bot = FBBot(token, verify_token)

@app.route('/', methods=['GET', 'POST'])
def webhook():
    return bot.webhook(request, on_message, on_postback, on_linked, on_unlinked)

def on_linked(sender, login, requestInfo):
    print("link")
    print(sender+" "+ login)

def on_unlinked(sender, requestInfo):
    print("unlink")
    print(sender+" unlink")

def on_postback(sender, text, requestInfo):
    print("post")
    bot.send_text_message(sender, 'Received postback "{0}"'.format(text))

def on_message(sender, text, requestInfo):
    print("message")
    if(text == "Video"):
        bot.send_message_file_attachment(sender, FBAttachment.File.video, "http://img-9gag-fun.9cache.com/photo/adXLy8N_460sv.mp4")
    elif(text == "Image"):
        bot.send_message_file_attachment(sender, FBAttachment.File.image, "http://img-9gag-fun.9cache.com/photo/aEnxQve_460s_v1.jpg")
    elif(text == "Generic"):
        bot.send_message_generic(sender, "Generic message", "with image and button", "https://scontent.xx.fbcdn.net/t39.3138-6/p128x128/12056981_908479762570256_1493516739_n.jpg", 
                                 [ 
                                     FBAttachment.button_account_unlink()
                                 ])

    elif(text == "Receipt"):
        message = FBOrder(
            "Stephane Crozatier",
            "125352345",
            "USD",
            "Visa",
            [
                FBOrder.one_purchase("T-Shirt", 1,"yellow", 5, "USD", "http://cdn01.shopclues.net/images/detailed/19936/yellowtshirt_1434534567.jpg"),
                FBOrder.one_purchase("Baseball cap", 2,"white",  2, "USD", "http://i01.i.aliimg.com/img/pb/630/860/383/383860630_626.jpg")
            ],
            FBOrder.price_summary(9, 0, 1, 8),
            "http://google.com",
            FBOrder.address("1 Hacker Way", "", "Menlo Park", "94025", "CA", "US"),
            "427561765",
            [
                FBOrder.price_one_adjustment("2$ Off coupon", 2)
            ]
        )
        bot.send_message_TypeC(sender, message)

    elif(text == "FirstAirline"):
        message = AirlineCheckin(
            "Checkin",
            "ru_RU",
            "12356",
            [
                AirlineCheckin.make_flight_info(
                    "4142",
                    AirlineCheckin.make_airport("SIN","Singapore"),
                    AirlineCheckin.make_airport("DME","Moscow"),
                    AirlineCheckin.make_flight_schedule("2016-01-05T15:05","2016-01-06T15:05")
                )
            ]
            ,"https://google.com")
        bot.send_message_TypeC(sender, message)

    elif(text == "SecondAirline"):
        message = AirlineFlightUpdate(
            "UPD",
            "delay",
            "ru_RU",
            "12356",
            AirlineFlightUpdate.make_update_flight_info(
                "4142",
                AirlineFlightUpdate.make_airport("SIN","Singapore"),
                AirlineFlightUpdate.make_airport("DME","Moscow"),
                AirlineFlightUpdate.make_flight_schedule("2016-01-05T15:05","2016-01-07T15:05")
            )
        )
        bot.send_message_TypeC(sender, message)
    else:
        #bot.send_text_message(sender, str(requestInfo))
        #return 0
        bot.send_text_message(sender, "Hello, What do you want?",[ 
            FBAttachment.quick_reply("Video"),
            FBAttachment.quick_reply("SecondAirline"),
            FBAttachment.quick_reply("FirstAirline"),
            FBAttachment.quick_reply("Receipt")
        ])
