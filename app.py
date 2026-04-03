import streamlit as st
import gspread
from google.oauth2.service_account import Credentials
from datetime import datetime
import json
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

st.set_page_config(
    page_title="BNI Visitor Registration",
    page_icon="\U0001f91d",
    layout="centered"
)

st.markdown("""
<style>
 [data-testid="stAppViewContainer"] { background: #ffffff; }
 .stButton > button {
  background-color: #C8102E !important;
  color: white !important;
  font-weight: 700 !important;
  border-radius: 8px !important;
  padding: 0.65em 2em !important;
  font-size: 1.05em !important;
  width: 100% !important;
  border: none !important;
  margin-top: 8px !important;
 }
 .stButton > button:hover { background-color: #a00d24 !important; }
 .intro-box {
  background: #fff5f5;
  border-left: 5px solid #C8102E;
  padding: 1em 1.5em;
  border-radius: 0 8px 8px 0;
  margin-bottom: 1.5em;
  font-size: 1.02em;
 }
 h2 { color: #C8102E !important; border-bottom: 2px solid #f0f0f0; padding-bottom: 6px; }
 .success-card {
  background: #f0fff4;
  border: 1.5px solid #27ae60;
  border-radius: 10px;
  padding: 1.5em;
  margin-top: 1em;
 }
</style>
""", unsafe_allow_html=True)

st.markdown("""
<div style='text-align:center; padding: 10px 0 4px 0;'>
 <div style='display:inline-block; background:#C8102E; color:white; font-size:2.2em; font-weight:900; padding:6px 22px; border-radius:8px; letter-spacing:3px; font-family:Arial,sans-serif;'>BNI</div>
 <h1 style='color:#C8102E; margin:10px 0 2px 0; font-size:1.9em;'>Welcome to Our BNI Chapter!</h1>
 <p style='color:#666; margin:0; font-size:1em;'>Business Network International — Where Referrals Are Our Business</p>
</div>
""", unsafe_allow_html=True)

st.markdown("""
<div class='intro-box'>
 <strong>Thanks for visiting today!</strong> Take 2 minutes to fill out this quick form
 and our members will follow up to help grow your business. We cannot wait to connect!
</div>
""", unsafe_allow_html=True)


def send_visitor_welcome(first_name, visitor_email, business_name, interest_level, gmail_user, gmail_pass):
    try:
        msg = MIMEMultipart("alternative")
        msg["Subject"] = f"Great connecting with you at BNI, {first_name}!"
        msg["From"] = gmail_user
        msg["To"] = visitor_email
        html_body = f"""
        <div style="font-family:Arial,sans-serif; max-width:600px; margin:auto;">
          <div style="background:#C8102E; color:white; padding:20px 24px; border-radius:10px 10px 0 0;">
            <div style="font-size:2em; font-weight:900; letter-spacing:3px;">BNI</div>
            <h2 style="margin:8px 0 0;">Thanks for Visiting Today, {first_name}!</h2>
          </div>
          <div style="background:#f9f9f9; padding:24px; border-radius:0 0 10px 10px;">
            <p>Hi {first_name},</p>
            <p>Thank you for joining us at BNI today! A chapter member will be reaching out to you shortly to connect.</p>
            <p><strong>Your business:</strong> {business_name}<br>
            <strong>Your interest level:</strong> {interest_level}</p>
            <p>We hope to see you again next week!</p>
            <hr style="border:none; border-top:1px solid #e0e0e0; margin:20px 0;">
            <p style="font-size:0.85em; color:#888;">
              <strong>P.S.</strong> Looking to automate your business with AI?
              <a href="https://mrceesai.com" style="color:#C8102E;">Austin Jones at MrCeesAI</a>
              helps small businesses save time and grow revenue. Visit
              <a href="https://mrceesai.com" style="color:#C8102E;">mrceesai.com</a>
            </p>
          </div>
        </div>"""
        msg.attach(MIMEText(html_body, "html"))
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(gmail_user, gmail_pass)
            server.sendmail(gmail_user, visitor_email, msg.as_string())
        return True
    except Exception:
        return False


def send_hot_lead_alert(first_name, last_name, visitor_email, phone, business_name,
                        industry, elevator_pitch, interest_level, gmail_user, gmail_pass, report_email):
    try:
        msg = MIMEMultipart("alternative")
        label = "READY TO APPLY" if interest_level == "Ready to apply!" else "VERY INTERESTED"
        msg["Subject"] = f"BNI HOT LEAD — {first_name} {last_name} from {business_name} is {label}"
        msg["From"] = gmail_user
        msg["To"] = report_email
        html_body = f"""
        <div style="font-family:Arial,sans-serif; max-width:600px; margin:auto;">
          <div style="background:#27ae60; color:white; padding:16px 24px; border-radius:10px 10px 0 0;">
            <h2 style="margin:0;">HOT BNI LEAD — Call Within 1 Hour!</h2>
            <p style="margin:4px 0 0; opacity:0.9;">Interest Level: <strong>{interest_level}</strong></p>
          </div>
          <div style="background:#f0fff4; padding:24px; border-radius:0 0 10px 10px; border:2px solid #27ae60;">
            <table style="width:100%; font-size:1em;">
              <tr><td style="color:#555; padding:6px 0; width:140px;"><strong>Name</strong></td><td>{first_name} {last_name}</td></tr>
              <tr style="background:#f9f9f9;"><td style="color:#555; padding:6px 0;"><strong>Business</strong></td><td>{business_name}</td></tr>
              <tr><td style="color:#555; padding:6px 0;"><strong>Industry</strong></td><td>{industry}</td></tr>
              <tr style="background:#f9f9f9;"><td style="color:#555; padding:6px 0;"><strong>Email</strong></td><td><a href="mailto:{visitor_email}">{visitor_email}</a></td></tr>
              <tr><td style="color:#555; padding:6px 0;"><strong>Phone</strong></td><td>{phone if phone else "Not provided"}</td></tr>
              <tr style="background:#f9f9f9;"><td style="color:#555; padding:6px 0; vertical-align:top;"><strong>Pitch</strong></td><td><em>"{elevator_pitch}"</em></td></tr>
            </table>
            <p style="margin-top:16px; color:#27ae60; font-weight:700;">CALL OR TEXT {first_name} NOW — they are ready!</p>
          </div>
        </div>"""
        msg.attach(MIMEText(html_body, "html"))
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(gmail_user, gmail_pass)
            server.sendmail(gmail_user, report_email, msg.as_string())
        return True
    except Exception:
        return False


with st.form("visitor_form", clear_on_submit=True):

    st.markdown("## Contact Information")
    col1, col2 = st.columns(2)
    with col1:
        first_name = st.text_input("First Name *", placeholder="Jane")
        email = st.text_input("Email Address *", placeholder="jane@example.com")
        phone = st.text_input("Phone Number", placeholder="(555) 555-5555")
    with col2:
        last_name = st.text_input("Last Name *", placeholder="Smith")
        city = st.text_input("City / Area", placeholder="Atlanta, GA")
        website = st.text_input("Website", placeholder="www.yoursite.com")

    st.markdown("## Social Media")
    col3, col4 = st.columns(2)
    with col3:
        linkedin = st.text_input("LinkedIn", placeholder="linkedin.com/in/yourname")
        instagram = st.text_input("Instagram", placeholder="@yourhandle")
    with col4:
        facebook = st.text_input("Facebook", placeholder="facebook.com/yourpage")
        twitter_x = st.text_input("X / Twitter", placeholder="@yourhandle")

    st.markdown("## Your Business")
    business_name = st.text_input("Business Name *", placeholder="Smith Consulting LLC")
    industry = st.selectbox("Industry / Profession *", [
        "Select one...",
        "Accounting / Finance", "Attorney / Legal", "Banking / Lending",
        "Chiropractor / Health", "Construction / Contracting", "Consulting / Coaching",
        "Digital Marketing", "Financial Planning", "Health & Wellness",
        "Home Services / Remodeling", "HR / Staffing", "Insurance",
        "IT / Technology / Cybersecurity", "Mortgage / Real Estate",
        "Photography / Videography", "Printing / Signage / Design",
        "Restaurant / Catering / Food", "Retail / E-Commerce",
        "Travel / Hospitality", "Other"
    ])
    other_industry = ""
    if industry == "Other":
        other_industry = st.text_input("Please describe your profession *")
    elevator_pitch = st.text_area(
        "In one sentence: what do you do and who do you help? *",
        placeholder="e.g. I help small business owners protect their assets with affordable insurance plans.",
        height=80
    )
    years_in_biz = st.select_slider(
        "How long have you been in business?",
        options=["Less than 1 year", "1-2 years", "3-5 years", "6-10 years", "10+ years"]
    )

    st.markdown("## Networking & Referrals")
    col5, col6 = st.columns(2)
    with col5:
        ideal_referral = st.text_area(
            "What does your ideal referral look like?",
            placeholder="e.g. A homeowner aged 35-55 who recently bought a house...",
            height=100
        )
    with col6:
        top_clients = st.text_area(
            "Top 3 types of clients or industries you serve?",
            placeholder="e.g. Real estate agents, small business owners, HR managers...",
            height=100
        )
    how_heard = st.selectbox("How did you hear about our chapter?", [
        "Select one...", "Invited by a member", "BNI website / Find a Chapter",
        "Social media", "Google search", "Friend / colleague", "Attended before", "Other"
    ])
    invited_by = st.text_input("If invited by a member — who invited you?", placeholder="Member name")

    st.markdown("## Goals & Interest Level")
    looking_for = st.multiselect(
        "What are you hoping to get from BNI? (select all that apply)",
        [
            "More qualified referrals", "Grow my professional network",
            "Business accountability", "Learn from other business owners",
            "Give referrals to others", "Greater brand visibility",
            "Find trusted vendors & partners", "Structured networking system"
        ]
    )
    has_bni_before = st.radio(
        "Have you visited or been a BNI member before?",
        ["No — first time!", "Visited before but never joined", "Former BNI member"],
        horizontal=True
    )
    biggest_challenge = st.text_area(
        "What is your biggest business challenge right now?",
        placeholder="e.g. Generating consistent leads, standing out from competitors...",
        height=80
    )
    ready_to_join = st.select_slider(
        "How interested are you in joining our chapter?",
        options=["Just exploring", "Somewhat interested", "Very interested", "Ready to apply!"]
    )
    notes = st.text_area("Anything else you would like us to know? (optional)", height=70)

    submitted = st.form_submit_button("Submit — We Will Be In Touch!")

if submitted:
    errors = []
    if not first_name.strip(): errors.append("First Name")
    if not last_name.strip(): errors.append("Last Name")
    if not email.strip(): errors.append("Email Address")
    if not business_name.strip(): errors.append("Business Name")
    if industry == "Select one...": errors.append("Industry / Profession")
    if industry == "Other" and not other_industry.strip(): errors.append("Profession (Other)")
    if not elevator_pitch.strip(): errors.append("One-sentence business description")

    if errors:
        st.error("Please complete these required fields: " + ", ".join(errors))
    else:
        final_industry = other_industry.strip() if industry == "Other" else industry
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        row = [
            timestamp, first_name.strip(), last_name.strip(),
            email.strip(), phone.strip(), city.strip(), website.strip(),
            linkedin.strip(), instagram.strip(), facebook.strip(), twitter_x.strip(),
            business_name.strip(), final_industry, elevator_pitch.strip(), years_in_biz,
            ideal_referral.strip(), top_clients.strip(),
            how_heard, invited_by.strip(), ", ".join(looking_for),
            has_bni_before, biggest_challenge.strip(), ready_to_join, notes.strip()
        ]

        try:
            creds_dict = json.loads(st.secrets["GOOGLE_CREDS"])
            creds = Credentials.from_service_account_info(
                creds_dict,
                scopes=[
                    "https://spreadsheets.google.com/feeds",
                    "https://www.googleapis.com/auth/drive"
                ]
            )
            client = gspread.authorize(creds)
            sheet = client.open(st.secrets["SHEET_NAME"]).sheet1
            sheet.append_row(row)
        except Exception as e:
            st.warning(f"Note: Could not save to sheet — {e}")

        try:
            gmail_user = st.secrets["GMAIL_USER"]
            gmail_pass = st.secrets["GMAIL_APP_PASSWORD"]
            report_email = st.secrets["REPORT_EMAIL"]

            send_visitor_welcome(
                first_name.strip(), email.strip(), business_name.strip(),
                ready_to_join, gmail_user, gmail_pass
            )

            if ready_to_join in ["Ready to apply!", "Very interested"]:
                send_hot_lead_alert(
                    first_name.strip(), last_name.strip(), email.strip(),
                    phone.strip(), business_name.strip(), final_industry,
                    elevator_pitch.strip(), ready_to_join,
                    gmail_user, gmail_pass, report_email
                )
        except Exception:
            pass

        st.balloons()
        st.markdown(f"""
<div class='success-card'>
<h3 style='color:#27ae60; margin-top:0;'>Thanks, {first_name}! You are all set.</h3>
<table style='width:100%; font-size:0.95em;'>
<tr><td><strong>Name</strong></td><td>{first_name} {last_name}</td></tr>
<tr><td><strong>Business</strong></td><td>{business_name}</td></tr>
<tr><td><strong>Industry</strong></td><td>{final_industry}</td></tr>
<tr><td><strong>Email</strong></td><td>{email}</td></tr>
<tr><td><strong>Interest Level</strong></td><td><strong style='color:#C8102E;'>{ready_to_join}</strong></td></tr>
</table>
<p style='margin-top:12px;'>A chapter member will reach out soon. Check your email — we sent you a welcome message!</p>
</div>
""", unsafe_allow_html=True)
