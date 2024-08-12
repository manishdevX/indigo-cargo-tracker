import os
import json
import pandas as pd
from config import AWB_FILE_PATH, RESULT_FILE_PATH, RESULT_FILE_FORMAT


def get_valid_airwaybills(df):
    valid_list = []
    for col in df.columns:
        df[col] = df[col].astype(str)
        valid_bills = [awb for awb in df[col] if len(awb) == 8 and awb.isdigit()]
        valid_list.extend(valid_bills)

    return valid_list


def load_awb_data():
    """
    Load air waybill data from the specified file path in the config.
    If no path is provided, prompt the user for comma-separated input of air waybill.
    """
    if AWB_FILE_PATH:
        awb_list = []
        ext = AWB_FILE_PATH.split(".")[-1].lower()
        if ext == "csv":
            df = pd.read_csv(AWB_FILE_PATH)
            awb_list = get_valid_airwaybills(df)
        elif ext in ["xls", "xlsx"]:
            excel_file = pd.ExcelFile(AWB_FILE_PATH)
            for sheet_name in excel_file.sheet_names:
                df = pd.read_excel(excel_file, sheet_name=sheet_name)
                valid_bills = get_valid_airwaybills(df)
                awb_list.extend(valid_bills)
        else:
            raise ValueError("Unsupported file format. Please use a CSV or Excel file.")
    else:
        awb_data = input("Enter Indigo Air Waybills (space-separated): ")
        awb_list = awb_data.split(" ")

    return awb_list


def process_result(result):
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
                    "Origin": cols[6]},
                    "Destination": cols[7],
                    "ULD": cols[8],
                    "Event Date-Time": cols[9],
                }
            )
    return parsed_data


def handle_result_storage(result):
    if not RESULT_FILE_PATH:
        os.makedirs("../results", exist_ok=True)
        path = os.path.join("../results", f"output.{RESULT_FILE_FORMAT}")
    else:
        path = os.path.join(RESULT_FILE_PATH, f"output.{RESULT_FILE_FORMAT}")

    df = pd.DataFrame(result)

    if RESULT_FILE_FORMAT == "csv":
        df.to_csv(path, index=False)
    elif RESULT_FILE_FORMAT in ["xls", "xlsx"]:
        df.to_excel(path, index=False)
    elif RESULT_FILE_FORMAT == "json":
        with open(path, "w") as f:
            json.dump(result, f, indent=4)
    else:
        raise ValueError(
            f'Unsupported file format "{RESULT_FILE_FORMAT}". Allowed file formats are csv, xls, xlsx and json.'
        )
