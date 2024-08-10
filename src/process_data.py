import pandas as pd
from bs4 import BeautifulSoup
from config import AWB_FILE_PATH

def load_awb_data():
    """
    Load air waybill data from the specified file path in the config.
    If no path is provided, prompt the user for comma-separated input of air waybill.
    """
    if AWB_FILE_PATH:
        ext = AWB_FILE_PATH.split(".")[-1].lower()
        if ext == "csv":
            df = pd.read_csv(AWB_FILE_PATH)
        elif ext in ["xls", "xlsx"]:
            df = pd.read_excel(AWB_FILE_PATH)
        else:
            raise ValueError("Unsupported file format. Please use a CSV or Excel file.")

        awb_list = df["AirwayBill"].tolist()
    else:
        awb_data = input("Enter Indigo Air Waybills (space-separated): ")
        awb_list = awb_data.split(" ")

    return awb_list


def validate_airwaybills(airwaybills):
    """
    Validate that the air waybills contain only numeric values.
    """
    for bill in airwaybills:
        if not bill.isdigit():
            raise ValueError(f'Invalid AWB Number "{bill}". Please enter numbers only')


def process_airwaybills():
    """
    Process the airway bills by loading, validating, and returning them.
    """
    airwaybills = load_awb_data()
    validate_airwaybills(airwaybills)
    return airwaybills


def process_response(response):
    soup = BeautifulSoup(response.content, "html.parser")
    # Extract status history table
    s = soup.find("table", id="GridViewAwbTracking")
    print("s is ",s.prettify())
