# Twitter AI Agent

This project is a **Twitter AI Agent** designed to track XRP-related news, generate tweets using OpenAI, and post them to X. The agent also sends SMS notifications via Twilio for user approval before posting. The agent checks for updates and generates tweets every 5 hours.

## How It Works
- The Flask server listens for incoming requests from Twilio (via Ngrok) and handles SMS responses.
- The agent checks for XRP-related news and generates tweets using OpenAI API.
- An SMS is sent to the user for approval with the generated tweet. If the user responds with "Yes", the tweet is posted to X using the Twitter API.
- After posting, the agent waits for the next cycle to repeat the process (every 6 hours).

## Features

- **XRP News Updates**: The agent monitors and fetches real-time XRP news.
- **AI-Generated Tweets**: The agent generates tweets using OpenAI’s GPT model based on the latest XRP news.
- **User Approval via SMS**: The agent sends an SMS through **Twilio** to request approval before posting a tweet.
- **Automatic Posting**: Once the user approves, the agent automatically posts the tweet to **X**.
- **Scheduled Task**: The agent runs every 6 hours to check for updates and generate new tweets.

## Technologies Used

- **Python**: The main programming language used for the project.
- **OpenAI API**: Used for generating tweet content from XRP news.
- **Twitter API**: Allows the agent to post tweets and interact with X.
- **Twilio API**: Used to send SMS messages to the user to get approval for posting tweets.
- **Ngrok**: Exposes the local server to the internet, allowing it to receive webhook requests.
- **Flask**: A lightweight Python web framework to handle requests and manage the agent’s actions.
- **BeautifulSoup**: A Python library used for **web scraping**. It allows you to parse and extract data from HTML or XML documents.
- **APScheduler**: A Python library for scheduling tasks.
- **Git**: For version control.

## Setup Instructions

Before setting up the project, make sure you have:

- Python 3.8+ installed.
- Accounts and API keys for **OpenAI**, **Twilio**, and **X**.

### Step 1: Clone the Repository

```bash
git clone https://github.com/gwoodard9/twitter-ai-agent.git
cd twitter-ai-agent
```
### Step 2: Set Up Dependencies

```bash
pip install -r requirements.txt
```
### Step 3: Set Up Environment Variables

Create a .env file in the root directory and add the required API keys.

### Step 4: Set Up Ngrok
**Ngrok** will expose your local server to the internet.

1. Download Ngrok and follow the installation instructions.
2. Run Ngrok to create a secure tunnel to your local server:
```bash
ngrok http 5000
```
This will provide a public URL (e.g., http://abcd1234.ngrok.io) that can be used for webhooks from Twilio and other services.

### Step 5: Set Up Twilio

To send SMS messages for tweet approval:

1. Sign up at Twilio, and get your Account SID and Auth Token.
2. Use the free trial number works for testing (or purchase a phone number ).
3. Add your Twilio credentials to the .env file.

### Step 6: Set Up Twitter API
To post tweets:

1. Sign up for a developer account at Twitter Developer Portal.
2. Create an app to get your API Key, API Secret, Access Token, and Access Token Secret.
2. Add the Twitter credentials to the .env file.

### Step 7: Run the Agent

1. Start the Flask server:
```bash
python app.py
or
python main.py
```
2. The server will run on http://localhost:5000. Open Ngrok to expose the server to the internet. Use the Ngrok URL for setting up webhooks in Twilio and Twitter.

3. The agent will fetch XRP updates and generate tweets every hour. It will send an SMS to the Twilio number for user approval before posting.

## Contributing

Feel free to fork this repository and submit pull requests for improvements or fixes. Please ensure your code follows the project’s style and is well-tested.

