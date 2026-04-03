import gspread
from google.oauth2.service_account import Credentials
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from datetime import datetime, timedelta
import json
import os

REPORT_EMAIL = os.environ["REPORT_EMAIL"]
GMAIL_USER = os.environ["GMAIL_USER"]
GMAIL_PASS = os.environ["GMAIL_APP_PASSWORD"]
SHEET_NAME = os.environ["SHEET_NAME"]
GOOGLE_CREDS = os.environ["GOOGLE_CREDS"]

HEADERS = [
    "Timestamp", "First Name", "Last Name", "Email", "Phone",
    "City", "Website", "LinkedIn", "Instagram", "Facebook", "X/Twitter",
    "Business Name", "Industry", "Elevator Pitch", "Years in Business",
    "Ideal Referral", "Top Clients", "How Heard", "Invited By",
    "Looking For", "BNI Experience", "Biggest Challenge", "Interest Level", "Notes"
]


def get_visitors_for_followup():
    """Get visitors who submitted 2-4 days ago (safe 48-hour window)."""
    creds = Credentials.from_service_account_info(
        json.loads(GOOGLE_CREDS),
        scopes=[
            "https://spreadsheets.google.com/feeds",
            "https://www.googleapis.com/auth/drive"
        ]
    )
    client = gspread.authorize(creds)
    sheet = client.open(SHEET_NAME).sheet1
    all_rows = sheet.get_all_values()

    if len(all_rows) <= 1:
        return []

    now = datetime.now()
    window_start = now - timedelta(days=4)
    window_end = now - timedelta(days=2)

    visitors = []
    for row in all_rows[1:]:
        try:
            row_dict = dict(zip(HEADERS, row + [""] * (len(HEADERS) - len(row))))
            ts = datetime.strptime(row_dict["Timestamp"], "%Y-%m-%d %H:%M:%S")
            if window_start <= ts <= window_end:
                visitors.append(row_dict)
        except Exception:
            continue
    return visitors


def send_followup_email(visitor):
    """Send a 3-day follow-up email to the visitor."""
    first_name = visitor.get("First Name", "there")
    visitor_email = visitor.get("Email", "")
    business_name = visitor.get("Business Name", "your business")

    if not visitor_email:
        return False

    try:
        msg = MIMEMultipart("alternative")
        msg["Subject"] = f"Following up from BNI — {first_name}, did anyone reach out yet?"
        msg["From"] = GMAIL_USER
        msg["To"] = visitor_email

        html_body = f"""
        <div style="font-family:Arial,sans-serif; max-width:600px; margin:auto;">
          <div style="background:#C8102E; color:white; padding:20px 24px; border-radius:10px 10px 0 0;">
            <div style="font-size:1.8em; font-weight:900; letter-spacing:3px;">BNI</div>
            <h2 style="margin:8px 0 0;">Just Checking In, {first_name}!</h2>
          </div>
          <div style="background:#f9f9f9; padding:24px; border-radius:0 0 10px 10px;">
            <p>Hi {first_name},</p>
            <p>It has been a few days since you visited our BNI chapter and we wanted to personally follow up.</p>
            <p>Did any of our members reach out to connect with you? If not, we want to make sure you get the attention you deserve.</p>
            <p>If you are still interested in learning more about BNI membership and what it could do for <strong>{business_name}</strong>, we would love to connect with you this week.</p>
            <p><strong>Your next step:</strong></p>
            <ul>
              <li>Reply to this email and let us know you are still interested</li>
              <li>Come back and visit us next week — guests are always welcome</li>
              <li>Ask any questions about membership</li>
            </ul>
            <p>We hope to see you again soon!</p>
            <hr style="border:none; border-top:1px solid #e0e0e0; margin:20px 0;">
            <p style="font-size:0.85em; color:#888;">
              Powered by <a href="https://mrceesai.com" style="color:#C8102E;">MrCeesAI</a> —
              AI Automation for Small Business
            </p>
          </div>
        </div>
        """

        msg.attach(MIMEText(html_body, "html"))
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(GMAIL_USER, GMAIL_PASS)
            server.sendmail(GMAIL_USER, visitor_email, msg.as_string())
        print(f"Follow-up sent to {first_name} ({visitor_email})")
        return True
    except Exception as e:
        print(f"Failed to send follow-up to {visitor_email}: {e}")
        return False


if __name__ == "__main__":
    visitors = get_visitors_for_followup()
    print(f"Found {len(visitors)} visitors due for 3-day follow-up")
    sent = 0
    for v in visitors:
        if send_followup_email(v):
            sent += 1
    print(f"Follow-up emails sent: {sent}/{len(visitors)}")
