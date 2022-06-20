from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from bs4 import BeautifulSoup
import json
import requests

def endpoint_isvalid(subdir):

    url = f"https://sports.sportingbet.com{subdir}"
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:102.0) Gecko/20100101 Firefox/102.0"}
    
    return requests.get(url, headers=headers).ok

def retrieve_html(subdir):

    if not endpoint_isvalid(subdir):
        return False

    options = Options()
    options.headless = True
    
    driver = webdriver.Firefox(options=options)
    driver.get(f"https://sports.sportingbet.com{subdir}")

    return driver.page_source

def create_json(events):

    events_ = []

    for event in events:
    
        event_ = {}
        event_["name"] = event.find(class_="title").text
        matches = []
        
        event = event.find_all("ms-event")

        for container in event:

            match = {}
            match["players"] = [player.text for player in container.find_all(class_="participant")]
            
            container = container.find_all(class_="grid-group-container")
            for odds in container:
                
                odds = odds.find_all("ms-font-resizer")
                match["odds"] = [odd.text for odd in odds]
                matches.append(match)

                event_["games"] = matches
                events_.append(event_)

    return events_

def return_content(subdir):

    html = retrieve_html(subdir)

    if not html:
        return {"error": "Subdirectory not found"}

    soup = BeautifulSoup(html, "html.parser")
    root = soup.find(id="main-view")
    events = root.find_all("ms-event-group")

    event_list = create_json(events)

    return {"response": event_list}
    #return json.dumps({"response": event_list}, ensure_ascii=False)
