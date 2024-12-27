from openai import OpenAI
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from bs4 import BeautifulSoup
import requests, time, os, tweepy, openai
from twilio.rest import Client
from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse
from apscheduler.schedulers.background import BackgroundScheduler

app = Flask(__name__)

load_dotenv()

url = 'https://www.coindesk.com/latest-crypto-news'

def scrape_xrp_news(url):
    response = requests.get(url)
    if response.status_code != 200:
        print('Error: Failed to retrieve the webpage')
        return "Failed to retrieve the webpage."
    
    soup = BeautifulSoup(response.text, "html.parser")
    titles = soup.find_all("h3")
    filtered_title_text = []

    for title in titles:
        title_text = title.get_text(strip=True)
        if "Bitcoin" in title_text:
            filtered_title_text.append(title_text)
            break

    if not filtered_title_text:
        print("No titles found with 'XRP'.")
        return "No relevant news found."
    
    return filtered_title_text

result = scrape_xrp_news(url)

client_openai = ChatOpenAI(model="gpt-4", openai_api_key=os.getenv("OPENAI_API_KEY"))

def write_tweet(filtered_title_text):
    if filtered_title_text == "No relevant news found.":
        print("No news found to tweet.")
        return None    
    try:
        completion = openai.chat.completions.create(
           model="gpt-4",
            messages=[
                {"role": "system", "content": "You are a content creator that owns an X page for XRP updates."},
                {"role": "user", "content": f'Write a quick intriguing tweet informing people on the news about:\n{filtered_title_text}'}
            ],
            max_tokens=100,
            temperature=0.7 
        ) 
        tweet_content = completion.choices[0].message.content.strip()
        print(completion.choices[0].message.content)
        return tweet_content
    
    except Exception as e:
        print(f"Error generating tweet: {e}")
        return None

account_sid = os.getenv('ACCOUNT_SID')
twilio_auth_token = os.getenv('TWILIO_AUTH_TOKEN')
my_phone = os.getenv('MY_PHONE')
twilio_phone = os.getenv('TWILIO_PHONE')
client = Client(account_sid, twilio_auth_token)

def send_text(tweet_content):
    try:
        message = client.messages.create(
            body=f"Approve this tweet?\n\n{tweet_content}\n\nReply 'YES' to approve or 'NO' to reject.",
            from_=twilio_phone,
            to=my_phone
        )
        print(f"Message SID: {message.sid}")
        return message.sid
    except Exception as e:
        print(f"Error sending message: {e}")
        return None

tweet_content = None

@app.route("/incoming_sms", methods=["POST"])
def incoming_sms():
    global tweet_content
    response = MessagingResponse()

    if response.lower() == 'yes':
        post_tweet(tweet_content)
        response.message("Tweet approved and posted!")
    elif response.lower() == 'no':
        response.message("Tweet rejected.")

    return str(response)

@app.route("/run_code", methods=["POST"])
def run_code():
    url = 'https://www.coindesk.com/latest-crypto-news'
    filtered_title_text = scrape_xrp_news(url)
    
    if filtered_title_text:
        tweet_content = write_tweet(filtered_title_text)
    
    send_text(tweet_content)
    return str('good')

def call_run_code():
    try:
        requests.post("http://127.0.0.1:5000/run_code")
    except Exception as e:
        print(f"Error calling /run_code: {e}")

consumer_key = os.getenv('CONSUMER_KEY')
consumer_secret = os.getenv('CONSUMER_SECRET')
access_token = os.getenv('ACCESS_TOKEN')
access_token_secret = os.getenv('ACCESS_TOKEN_SECRET')
twitter_bearer_token = os.getenv('TWITTER_BEARER_TOKEN')

def post_tweet(tweet_content):
    tweet_content
    twitter_client = tweepy.Client(
        consumer_key=consumer_key,
        consumer_secret=consumer_secret,
        access_token=access_token,
        access_token_secret=access_token_secret
    )
    
    try:
        response = twitter_client.create_tweet(text=tweet_content)
        print(f"Tweet successfully posted: {response.data['text']}")
    except tweepy.errors.TooManyRequests as e:
        print(f"Rate limit exceeded. Retry after some time: {e}")
        time.sleep(10)
    except Exception as e:
        print(f"Error posting tweet: {e}")

if __name__ == "__main__":
    scheduler = BackgroundScheduler()
    scheduler.add_job(call_run_code, 'interval', hours=6)
    scheduler.start()
    app.run(debug=True)