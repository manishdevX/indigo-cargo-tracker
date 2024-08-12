import smtplib
from io import BytesIO
import pandas as pd
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
from process_data import load_awb_data, handle_result_storage, process_result
from src.scraper import scrap_tracking_info
from config import (
    RESULT_STORAGE_ENABLED,
    RESULT_EMAIL_ENABLED,
    EMAIL_ATTACHMENT_FORMAT,
    EMAIL_HOST,
    EMAIL_PASSWORD,
    EMAIL_PORT,
    SENDER_EMAIL,
    RECIPIENT_EMAILS,
)


def send_email(result):
    msg = MIMEMultipart()
    msg["From"] = SENDER_EMAIL
    msg["To"] = RECIPIENT_EMAILS
    msg["Subject"] = "Processed Air wayBill Data"

    body = "Please find the attached tracking data."
    msg.attach(MIMEText(body, "plain"))

    buffer = BytesIO()
    df = pd.DataFrame(result)

    if EMAIL_ATTACHMENT_FORMAT == "csv":
        df.to_csv(buffer, index=False)
        attachment = "output.csv"
    elif EMAIL_ATTACHMENT_FORMAT in ["xls", "xlsx"]:
        df.to_excel(buffer, index=False, engine="xlsxwriter")
        attachment = "output.xlsx"
    else:
        raise ValueError(
            f'Unsupported attachment format "{EMAIL_ATTACHMENT_FORMAT}". Allowed formats are csv, xls, xlsx and json.'
        )

    buffer.seek(0)

    # Attach the file
    part = MIMEBase("application", "octet-stream")
    part.set_payload(buffer.read())
    encoders.encode_base64(part)
    part.add_header("Content-Disposition", f"attachment; filename={attachment}")

    msg.attach(part)

    server = smtplib.SMTP(EMAIL_HOST, EMAIL_PORT)
    server.starttls()
    server.login(SENDER_EMAIL, EMAIL_PASSWORD)
    text = msg.as_string()
    server.sendmail(SENDER_EMAIL, RECIPIENT_EMAILS, text)
    server.quit()


def main():
    airwaybills = load_awb_data()
    result = scrap_tracking_info(airwaybills)
    parsed_result = process_result(result)

    if not (RESULT_STORAGE_ENABLED or RESULT_EMAIL_ENABLED):
        raise ValueError(
            "Either RESULT_STORAGE_ENABLED or RESULT_EMAIL_ENABLED must be enabled."
        )

    if RESULT_STORAGE_ENABLED:
        handle_result_storage(parsed_result)

    if RESULT_EMAIL_ENABLED:
        send_email(parsed_result)


if __name__ == "__main__":
    main()
