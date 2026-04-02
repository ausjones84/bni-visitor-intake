import gspread
from google.oauth2.service_account import Credentials
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from datetime import datetime, timedelta
import json
import os

REPORT_EMAIL = os.environ["REPORT_EMAIL"]
GMAIL_USER   = os.environ["GMAIL_USER"]
GMAIL_PASS   = os.environ["GMAIL_APP_PASSWORD"]
SHEET_NAME   = os.environ["SHEET_NAME"]
GOOGLE_CREDS = os.environ["GOOGLE_CREDS"]

HEADERS = [
    "Timestamp", "First Name", "Last Name", "Email", "Phone",
    "City", "Website", "LinkedIn", "Instagram", "Facebook", "X/Twitter",
    "Business Name", "Industry", "Elevator Pitch", "Years in Business",
    "Ideal Referral", "Top Clients", "How Heard", "Invited By",
    "Looking For", "BNI Experience", "Biggest Challenge", "Interest Level", "Notes"
]

def get_this_weeks_visitors():
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
    cutoff = datetime.now() - timedelta(days=7)
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

def interest_color(level):
    return {
        "Ready to apply!": "#27ae60",
        "Very interested":  "#2980b9",
        "Somewhat interested": "#f39c12",
        "Just exploring":  "#95a5a6"
    }.get(level, "#95a5a6")

def build_email_html(visitors):
    date_str = datetime.now().strftime("%B %d, %Y")
    if not visitors:
        return f"""
        <div style="font-family:Arial,sans-serif; max-width:700px; margin:auto; padding:20px;">
            <div style="background:#C8102E; color:white; padding:20px; border-radius:8px;">
                <h1 style="margin:0;">BNI Weekly Visitor Report</h1>
                <p style="margin:4px 0 0;">{date_str}</p>
            </div>
            <p style="padding:20px; color:#555;">No new visitors this week. Keep spreading the word!</p>
        </div>
        """

    cards = ""
    for v in visitors:
        socials = []
        if v.get("LinkedIn"):   socials.append(f'<a href="{v["LinkedIn"]}" style="color:#0077b5;">LinkedIn</a>')
        if v.get("Instagram"):  socials.append(f'<span style="color:#E1306C;">IG: {v["Instagram"]}</span>')
        if v.get("Facebook"):   socials.append(f'<span style="color:#4267B2;">FB: {v["Facebook"]}</span>')
        if v.get("X/Twitter"):  socials.append(f'<span style="color:#1DA1F2;">X: {v["X/Twitter"]}</span>')
        social_html = " &nbsp;|&nbsp; ".join(socials) if socials else "<em>None provided</em>"

        color = interest_color(v.get("Interest Level", ""))
        cards += f"""
        <div style="border:1px solid #e0e0e0; border-radius:10px; padding:18px; margin-bottom:20px;
                    font-family:Arial,sans-serif; box-shadow:0 2px 6px rgba(0,0,0,0.06);">
            <div style="display:flex; justify-content:space-between; align-items:flex-start; flex-wrap:wrap;">
                <div>
                    <h2 style="color:#C8102E; margin:0 0 4px;">{v.get("First Name","")} {v.get("Last Name","")}</h2>
                    <p style="margin:0; font-size:1.05em; font-weight:600;">{v.get("Business Name","")}</p>
                    <p style="margin:2px 0; color:#666;">{v.get("Industry","")}</p>
                </div>
                <span style="background:{color}; color:white; padding:5px 14px; border-radius:20px;
                             font-size:0.85em; font-weight:600; white-space:nowrap; margin-top:4px;">
                    {v.get("Interest Level","")}
                </span>
            </div>
            <hr style="border:none; border-top:1px solid #f0f0f0; margin:12px 0;">
            <table style="width:100%; border-collapse:collapse; font-size:0.93em;">
                <tr>
                    <td style="padding:4px 8px; color:#888; width:140px;"><strong>Elevator Pitch</strong></td>
                    <td style="padding:4px 8px;"><em>"{v.get("Elevator Pitch","")}"</em></td>
                </tr>
                <tr style="background:#fafafa;">
                    <td style="padding:4px 8px; color:#888;"><strong>Email</strong></td>
                    <td style="padding:4px 8px;"><a href="mailto:{v.get("Email","")}">{v.get("Email","")}</a></td>
                </tr>
                <tr>
                    <td style="padding:4px 8px; color:#888;"><strong>Phone</strong></td>
                    <td style="padding:4px 8px;">{v.get("Phone","N/A")}</td>
                </tr>
                <tr style="background:#fafafa;">
                    <td style="padding:4px 8px; color:#888;"><strong>City</strong></td>
                    <td style="padding:4px 8px;">{v.get("City","N/A")}</td>
                </tr>
                <tr>
                    <td style="padding:4px 8px; color:#888;"><strong>Social Media</strong></td>
                    <td style="padding:4px 8px;">{social_html}</td>
                </tr>
                <tr style="background:#fafafa;">
                    <td style="padding:4px 8px; color:#888;"><strong>Website</strong></td>
                    <td style="padding:4px 8px;">{v.get("Website","N/A")}</td>
                </tr>
                <tr>
                    <td style="padding:4px 8px; color:#888;"><strong>Ideal Referral</strong></td>
                    <td style="padding:4px 8px;">{v.get("Ideal Referral","N/A")}</td>
                </tr>
                <tr style="background:#fafafa;">
                    <td style="padding:4px 8px; color:#888;"><strong>Top Clients</strong></td>
                    <td style="padding:4px 8px;">{v.get("Top Clients","N/A")}</td>
                </tr>
                <tr>
                    <td style="padding:4px 8px; color:#888;"><strong>BNI Experience</strong></td>
                    <td style="padding:4px 8px;">{v.get("BNI Experience","")}</td>
                </tr>
                <tr style="background:#fafafa;">
                    <td style="padding:4px 8px; color:#888;"><strong>Invited By</strong></td>
                    <td style="padding:4px 8px;">{v.get("Invited By","N/A")}</td>
                </tr>
                <tr>
                    <td style="padding:4px 8px; color:#888;"><strong>Challenge</strong></td>
                    <td style="padding:4px 8px;">{v.get("Biggest Challenge","")}</td>
                </tr>
                <tr style="background:#fafafa;">
                    <td style="padding:4px 8px; color:#888;"><strong>Notes</strong></td>
                    <td style="padding:4px 8px;">{v.get("Notes","")}</td>
                </tr>
            </table>
        </div>
        """

    return f"""
    <div style="font-family:Arial,sans-serif; max-width:740px; margin:auto;">
        <div style="background:#C8102E; color:white; padding:20px 24px; border-radius:10px 10px 0 0;">
            <h1 style="margin:0; font-size:1.5em;">BNI Weekly Visitor Report</h1>
            <p style="margin:5px 0 0; opacity:0.9;">{date_str} &nbsp;·&nbsp; {len(visitors)} visitor(s) this week</p>
        </div>
        <div style="background:#f9f9f9; padding:20px; border-radius:0 0 10px 10px;">
            {cards}
        </div>
        <p style="text-align:center; color:#bbb; font-size:0.8em; margin-top:10px;">
            Auto-generated by the BNI Visitor Intake System
        </p>
    </div>
    """

def send_report(html_body, count):
    msg = MIMEMultipart("alternative")
    msg["Subject"] = f"BNI Visitor Report — {count} new visitor(s) this week"
    msg["From"] = GMAIL_USER
    msg["To"] = REPORT_EMAIL
    msg.attach(MIMEText(html_body, "html"))
    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
        server.login(GMAIL_USER, GMAIL_PASS)
        server.sendmail(GMAIL_USER, REPORT_EMAIL, msg.as_string())
    print(f"Report sent to {REPORT_EMAIL} — {count} visitors")

if __name__ == "__main__":
    visitors = get_this_weeks_visitors()
    html = build_email_html(visitors)
    send_report(html, len(visitors))
