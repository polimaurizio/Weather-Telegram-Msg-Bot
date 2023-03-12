from requests_html import HTMLSession
from dotenv import load_dotenv
import os
import requests
import schedule
import time

s = HTMLSession()
load_dotenv() #Load .env variable


def send_msg(text):
    token = os.getenv("TOKEN")
    chat_id = os.getenv("CHAT_ID")

    url_req = "https://api.telegram.org/bot" + token + "/sendMessage" + "?chat_id=" + chat_id + "&text=" + text
    
    #Send the message in telegram
    result = requests.get(url_req)
    
    #Print on terminal the result
    print(result.json())



def scraping():
    query = 'italy'
    url = f'https://www.google.com/search?q=weather+{query}'
    user_agent = os.getenv("USER_AGENT")

    r = s.get(url, headers={'User-Agent': user_agent})

    # Request
    temp = r.html.find('span#wob_tm', first=True).text
    unit = r.html.find('div.vk_bk.wob-unit span.wob_t', first=True).text
    desc = r.html.find('div.VQF4g', first=True).find('span#wob_dc', first=True).text


    msg = query.capitalize() + ": " + temp + unit + " " + desc + "\n" + url
    send_msg(msg)



# Start every 10 seconds
schedule.every(10).seconds.do(scraping)
# schedule.every(24).hours.do(scraping)

while True:
    schedule.run_pending()
    time.sleep(1)