import gspread
from google.oauth2.service_account import Credentials
from datetime import datetime, timedelta
import json
import os
import urllib.request

# Telegram credentials — stored as GitHub Secrets
TELEGRAM_TOKEN = os.environ["TELEGRAM_BOT_TOKEN"]
TELEGRAM_CHAT_ID = os.environ["TELEGRAM_CHAT_ID"]
GOOGLE_CREDS = os.environ["GOOGLE_CREDS"]
SHEET_NAME = os.environ["SHEET_NAME"]

HEADERS = [
    "Timestamp", "First Name", "Last Name", "Email", "Phone",
    "City", "Website", "LinkedIn", "Instagram", "Facebook", "X/Twitter",
    "Business Name", "Industry", "Elevator Pitch", "Years in Business",
    "Ideal Referral", "Top Clients", "How Heard", "Invited By",
    "Looking For", "BNI Experience", "Biggest Challenge", "Interest Level", "Notes"
]


def send_telegram(message):
    """Send a message to Austin via Telegram bot."""
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    payload = json.dumps({
        "chat_id": TELEGRAM_CHAT_ID,
        "text": message,
        "parse_mode": "HTML"
    }).encode("utf-8")
    req = urllib.request.Request(
        url,
        data=payload,
        headers={"Content-Type": "application/json"}
    )
    with urllib.request.urlopen(req) as response:
        return response.read()


def get_sheet_data():
    """Connect to Google Sheets and return all rows."""
    creds = Credentials.from_service_account_info(
        json.loads(GOOGLE_CREDS),
        scopes=[
            "https://spreadsheets.google.com/feeds",
            "https://www.googleapis.com/auth/drive"
        ]
    )
    client = gspread.authorize(creds)
    sheet = client.open(SHEET_NAME).sheet1
    return sheet.get_all_values()


def get_recent_visitors(all_rows, days=1):
    """Get visitors from the last N days."""
    if len(all_rows) <= 1:
        return []
    cutoff = datetime.now() - timedelta(days=days)
    visitors = []
    for row in all_rows[1:]:
        try:
            row_dict = dict(zip(HEADERS, row + [""] * (len(HEADERS) - len(row))))
            ts = datetime.strptime(row_dict["Timestamp"], "%Y-%m-%d %H:%M:%S")
            if ts >= cutoff:
                visitors.append(row_dict)
        except Exception:
            continue
    return visitors


def get_total_visitors(all_rows):
    """Return total count of all visitors ever."""
    return max(0, len(all_rows) - 1)


if __name__ == "__main__":
    today = datetime.now().strftime("%A, %B %d, %Y")

    try:
        all_rows = get_sheet_data()
        recent = get_recent_visitors(all_rows, days=1)
        total = get_total_visitors(all_rows)
    except Exception as e:
        send_telegram(f"<b>MrCeesAI Morning Report</b>\n{today}\n\nCould not load BNI data: {e}")
        exit(1)

    hot_leads = [v for v in recent if v.get("Interest Level") in ["Ready to apply!", "Very interested"]]

    msg = f"<b>Good morning, Austin!</b> \U0001f31e\n"
    msg += f"<b>MrCeesAI Daily Report</b>\n"
    msg += f"{today}\n"
    msg += "\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\n"
    msg += f"\U0001f465 <b>New BNI Visitors (24hrs):</b> {len(recent)}\n"
    msg += f"\U0001f525 <b>Hot Leads:</b> {len(hot_leads)}\n"
    msg += f"\U0001f4ca <b>Total All-Time Visitors:</b> {total}\n"

    if hot_leads:
        msg += "\n<b>\U0001f6a8 HOT LEADS — Follow Up NOW:</b>\n"
        for v in hot_leads:
            fn = v.get("First Name", "")
            ln = v.get("Last Name", "")
            biz = v.get("Business Name", "")
            lvl = v.get("Interest Level", "")
            eml = v.get("Email", "")
            ph = v.get("Phone", "N/A")
            msg += f"  \u2022 <b>{fn} {ln}</b> | {biz}\n"
            msg += f"    Level: {lvl}\n"
            msg += f"    Email: {eml}\n"
            msg += f"    Phone: {ph}\n"
    elif recent:
        msg += "\nNo hot leads overnight — keep building the pipeline!\n"
    else:
        msg += "\nNo new visitors in last 24 hours. Share your form link at the next meeting!\n"

    msg += "\n<b>\U0001f4cb Your Priorities Today:</b>\n"
    msg += "  1. Follow up with hot leads within 1 hour\n"
    msg += "  2. Check Gmail for outreach replies\n"
    msg += "  3. Review new SAM.gov contracts\n"
    msg += "  4. Approve today\'s YouTube AI twin script\n"
    msg += "  5. Check no-website outreach replies\n"
    msg += "\nLet\'s get it, Austin! \U0001f4aa\U0001f3fe"

    send_telegram(msg)
    print(f"Morning report sent to Telegram — {len(recent)} new visitors, {len(hot_leads)} hot leads")
