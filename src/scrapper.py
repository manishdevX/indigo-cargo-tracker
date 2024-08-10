import requests
from bs4 import BeautifulSoup


def scrap_tracking_info(airwaybills, prefix, track_url):
    result = []
    for awb in airwaybills:
        session = requests.session()
        response = session.get(track_url)
        soup = BeautifulSoup(response.content, "html.parser")

        payload = {
            "__VIEWSTATE": soup.find("input", {"name": "__VIEWSTATE"}).get("value"),
            "txtPrefix": prefix,
            "TextBoxAWBno": awb,
        }

        response = session.post(track_url, data=payload)
        soup = BeautifulSoup(response.content, "html.parser")

        # Extract status history table
        status_history = soup.find("table", id="GridViewAwbTracking")
        result.append(status_history)

    return result
