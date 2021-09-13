import tweepy
import pytz
import smtplib
import time
import schedule
import os
from email.message import EmailMessage
from datetime import datetime, timedelta

consumer_key = os.environ['consumer_key']
consumer_secret = os.environ['consumer_secret']
access_token = os.environ['access_token']
access_token_secret = os.environ['access_token_secret']

gmail_user = os.environ['gmail_user']
gmail_password = os.environ['gmail_password']

mail = os.environ['email']

sent_from = gmail_user
to = ['me@gmail.com', mail]
subject = 'OMG Super Important Message'
toronto = pytz.timezone("Canada/Eastern")

information = []

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth)

userID = "680NEWStraffic"


def send_traffic():
    tweets = api.user_timeline(screen_name=userID,
                               # 200 is the maximum allowed count
                               count=200,
                               include_rts=False,
                               # Necessary to keep full_text
                               # otherwise only the first 140 words are extracted
                               tweet_mode='extended'
                               )

    for info in tweets[:30]:

        if info.created_at > datetime.today() - timedelta(hours=6):
            server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
            server.login(gmail_user, gmail_password)

            information.append(
                f"{pytz.utc.localize(info.created_at, is_dst=None).astimezone(toronto)}, {info.full_text}")

    msg = EmailMessage()
    msg.set_content("\n\n".join(information))

    msg['Subject'] = 'Your Ontario Traffic Data'
    msg['From'] = "me@gmail.com"
    msg['To'] = mail

    server.send_message(msg)
    server.close()

# 12:15 20:45
for i in ["12:15", "20:45"]:
    schedule.every().monday.at(i).do(send_traffic, i)
    schedule.every().tuesday.at(i).do(send_traffic, i)
    schedule.every().wednesday.at(i).do(send_traffic, i)
    schedule.every().thursday.at(i).do(send_traffic, i)
    schedule.every().friday.at(i).do(send_traffic, i)

while True:
    schedule.run_pending()
    time.sleep(1)
