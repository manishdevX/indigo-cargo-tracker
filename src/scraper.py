import requests
import time
import random
from bs4 import BeautifulSoup
from config import TRACK_URL, PREFIX


def scrap_tracking_info(airwaybills):
    result = []
    for ind, awb in enumerate(airwaybills):
        session = requests.session()
        response = session.get(TRACK_URL)
        soup = BeautifulSoup(response.content, "html.parser")

        payload = {
            "__VIEWSTATE": soup.find("input", {"name": "__VIEWSTATE"}).get("value"),
            "txtPrefix": PREFIX,
            "TextBoxAWBno": awb,
        }

        response = session.post(TRACK_URL, data=payload)
        soup = BeautifulSoup(response.content, "html.parser")

        # Extract status history table
        status_history = soup.find("table", id="GridViewAwbTracking")
        result.append((awb, status_history))

        # Add random sleep for every 10 requests to avoid rate limiting blocking
        if (ind + 1) % 10 == 0:
            time.sleep(random.randint(1, 3))

    return result
