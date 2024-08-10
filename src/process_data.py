import os
import json
import pandas as pd
from config import AWB_FILE_PATH, RESULT_FILE_PATH, RESULT_FILE_FORMAT


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


def handle_result_storage(result):
    print("result len ", len(result))
    if not RESULT_FILE_PATH:
        os.makedirs("../results", exist_ok=True)
        path = os.path.join("../results", f"output.{RESULT_FILE_FORMAT}")
    else:
        path = os.path.join(RESULT_FILE_PATH, f"output.{RESULT_FILE_FORMAT}")

    parsed_data = []

    for data in result:
        rows = data.find_all("tr")[1:]
        for row in rows:
            cols = [ele.text.strip() for ele in row.find_all("td")]
            parsed_data.append(
                {
                    "Station": cols[0],
                    "Milestone": cols[1],
                    "Pcs": cols[2],
                    "Weight": cols[3],
                    "Flight#": cols[4],
                    "Flight Date": cols[5],
                    "Org": cols[6],
                    "Dest": cols[7],
                    "ULD": cols[8],
                    "Event Date-Time": cols[9],
                }
            )

    df = pd.DataFrame(parsed_data)

    if RESULT_FILE_FORMAT == "csv":
        df.to_csv(path, index=False)
    elif RESULT_FILE_FORMAT in ["xls", "xlsx"]:
        df.to_excel(path, index=False)
    elif RESULT_FILE_FORMAT == "json":
        with open(path, "w") as f:
            json.dump(parsed_data, f, indent=4)
    else:
        raise ValueError(
            f'Unsupported file format "{RESULT_FILE_FORMAT}". Allowed file formats are csv, xls, xlsx and json.'
        )
