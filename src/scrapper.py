import requests
from bs4 import BeautifulSoup
from config import TRACK_URL, PREFIX


def scrap_tracking_info(airwaybills):
    result = []
    for awb in airwaybills:
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
        result.append(status_history)

    return result
