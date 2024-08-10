import requests
from bs4 import BeautifulSoup


def scrap_track_info(airwaybills, prefix, track_url):
    headers = {
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.186 Safari/537.36",
        "Content-Type": "application/x-www-form-urlencoded",
        "Accept-Encoding": "gzip, deflate",
        "Accept-Language": "en-GB,en;q=0.9,en-US;q=0.8,zh-TW;q=0.7,zh;q=0.6,zh-CN;q=0.5",
    }
    for awb in airwaybills:
        session = requests.session()
        response = session.get(
            track_url,
            headers={
                "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.186 Safari/537.36"
            },
        )
        soup = BeautifulSoup(response.content, "html.parser")
        payload = {
            "__VIEWSTATE": soup.find("input", {"name": "__VIEWSTATE"}).get("value"),
            "txtPrefix": prefix,
            "TextBoxAWBno": awb,
        }
        response = session.post(track_url, data=payload, headers=headers)
        return response
