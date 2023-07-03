import requests
import xml.etree.ElementTree as ET
import time
import logging
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError

slack_bot_token = 'oauthtoken'  # Replace with your actual Slack Bot User OAuth Token
slack_channel = '#network'  # Replace with the name of your Slack channel

base_url = 'http://example.com/System/index_stat.xml'  # Base URL for temperature retrieval
username = 'username'  # Replace with your actual username
password = 'password'  # Replace with your actual password

session = requests.Session()
slack_client = WebClient(token=slack_bot_token)
# Set up logging configuration
logging.basicConfig(filename='C:\Logs\script_log.txt', level=logging.INFO, format='%(asctime)s - %(levelname)s: %(message)s')
def send_slack_message(message):
    try:
        response = slack_client.chat_postMessage(channel=slack_channel, text=message)
        if not response['ok']:
            print(f"Failed to send Slack message: {response['error']}")
    except SlackApiError as e:
        print(f"Error sending Slack message: {e.response['error']}")

def check_temperature(url):
    response = session.get(url)

    # Parse the XML response
    root = ET.fromstring(response.text)

    # Find the element containing the temperature value
    temperature_element = root.find('Temps1')

    # Extract the temperature value
    temperature = float(temperature_element.text)

    return temperature

while True:
    for i in range(1, 4):
        url = base_url.format(i)
        session = requests.Session()
        login_data = {'username': username, 'password': password}
        response = session.post(url.replace('index_stat.xml', ''), data=login_data)

        # Check if login was successful
        if response.status_code != 200:
            print(f'Login failed for URL: {url}. Please check your credentials.')
            continue

        temperature = check_temperature(url)
        logging.info(f'Current temperature for URL {url}: {temperature}')  # Log the current temperature


        print(f'Current temperature for URL {url}:', temperature)

        if temperature >= 80:
            message = f"Temperature at {url} is {temperature}°F. Alert triggered!"
            send_slack_message(message)

    # Wait for 15 minutes
    time.sleep(900)  # 900 seconds = 15 minutes

