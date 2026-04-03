import streamlit as st
import gspread
from google.oauth2.service_account import Credentials
from datetime import datetime
import json
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import random

st.set_page_config(
    page_title="BNI Chapter Hub",
    page_icon="\U0001f91d",
    layout="centered"
)

# ── Session state for navigation ────────────────────────────────────────────
if "page" not in st.session_state:
    st.session_state["page"] = "landing"

# ── Shared CSS ───────────────────────────────────────────────────────────────
st.markdown("""
<style>
@keyframes fadeInDown {
    from { opacity: 0; transform: translateY(-18px); }
    to   { opacity: 1; transform: translateY(0); }
}
@keyframes fadeInUp {
    from { opacity: 0; transform: translateY(18px); }
    to   { opacity: 1; transform: translateY(0); }
}
@keyframes pulse {
    0%,100% { box-shadow: 0 0 0 0 rgba(200,16,46,0.30); }
    50%      { box-shadow: 0 0 0 8px rgba(200,16,46,0); }
}
@keyframes pulseGreen {
    0%,100% { box-shadow: 0 0 0 0 rgba(39,174,96,0.30); }
    50%      { box-shadow: 0 0 0 8px rgba(39,174,96,0); }
}
@keyframes shimmer {
    0%   { background-position: -400px 0; }
    100% { background-position: 400px 0; }
}
[data-testid="stAppViewContainer"] { background: #ffffff; }
.hero-wrap { animation: fadeInDown 0.7s ease both; }
.stButton > button {
    background: linear-gradient(135deg, #C8102E 0%, #a00d24 100%) !important;
    color: white !important;
    font-weight: 700 !important;
    border-radius: 8px !important;
    padding: 0.7em 2em !important;
    font-size: 1.08em !important;
    width: 100% !important;
    border: none !important;
    margin-top: 10px !important;
    letter-spacing: 0.5px !important;
    animation: pulse 2.4s infinite !important;
    transition: transform 0.12s, opacity 0.12s !important;
}
.stButton > button:hover { transform: translateY(-2px) !important; opacity: 0.93 !important; }
.intro-box {
    background: #fff5f5; border-left: 5px solid #C8102E;
    padding: 1em 1.5em; border-radius: 0 8px 8px 0;
    margin-bottom: 1em; font-size: 1.02em;
    animation: fadeInDown 0.9s ease both;
}
.member-intro-box {
    background: #f0fff4; border-left: 5px solid #27ae60;
    padding: 1em 1.5em; border-radius: 0 8px 8px 0;
    margin-bottom: 1em; font-size: 1.02em;
    animation: fadeInDown 0.9s ease both;
}
.recording-box {
    background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%);
    border: 2px solid #e94560;
    border-radius: 14px; padding: 1.2em 1.5em;
    margin-bottom: 1em; color: white;
    animation: fadeInDown 0.9s ease both;
}
h2 { color: #C8102E !important; border-bottom: 2px solid #f0f0f0; padding-bottom: 6px; }
h2.green { color: #27ae60 !important; }
.success-card {
    background: linear-gradient(135deg, #f0fff4 0%, #e8f8ee 100%);
    border: 1.5px solid #27ae60; border-radius: 12px;
    padding: 1.5em; margin-top: 1em;
    animation: fadeInDown 0.6s ease both;
}
.member-success-card {
    background: linear-gradient(135deg, #f0f8ff 0%, #e8f0ff 100%);
    border: 1.5px solid #2980b9; border-radius: 12px;
    padding: 1.5em; margin-top: 1em;
    animation: fadeInDown 0.6s ease both;
}
.tip-box {
    background: linear-gradient(135deg, #fffbf0 0%, #fff8e1 100%);
    border-left: 4px solid #f39c12; border-radius: 0 8px 8px 0;
    padding: 0.9em 1.2em; margin: 0.5em 0 1.2em 0; font-size: 0.97em;
}
.badge-tyfcb    { background:#27ae60; color:white; border-radius:20px; padding:4px 14px; font-size:0.88em; font-weight:700; display:inline-block; margin:3px; }
.badge-referral { background:#C8102E; color:white; border-radius:20px; padding:4px 14px; font-size:0.88em; font-weight:700; display:inline-block; margin:3px; }
.badge-testimonial { background:#8e44ad; color:white; border-radius:20px; padding:4px 14px; font-size:0.88em; font-weight:700; display:inline-block; margin:3px; }
.landing-card {
    background: linear-gradient(135deg, #fff 0%, #f9f9f9 100%);
    border-radius: 16px; padding: 2em 1.5em; text-align: center;
    box-shadow: 0 8px 32px rgba(0,0,0,0.10);
    border: 2px solid transparent;
    transition: all 0.25s; cursor: pointer;
    animation: fadeInUp 0.8s ease both;
}
.landing-card:hover { transform: translateY(-4px); box-shadow: 0 12px 40px rgba(0,0,0,0.15); }
.landing-card-visitor { border-color: #C8102E !important; }
.landing-card-member  { border-color: #27ae60 !important; }
div[data-testid="stTabs"] button[data-baseweb="tab"] {
    font-size: 1.05em !important; font-weight: 600 !important; padding: 10px 24px !important;
}
.transcript-box {
    background: #0d1117; color: #58a6ff;
    font-family: monospace; font-size: 0.9em;
    border-radius: 8px; padding: 10px 14px;
    min-height: 80px; border: 1px solid #30363d;
    white-space: pre-wrap;
}
</style>
""", unsafe_allow_html=True)

# ── Hero Header ──────────────────────────────────────────────────────────────
st.markdown("""
<div class='hero-wrap' style='text-align:center; padding: 10px 0 4px 0;'>
  <div style='display:inline-block; background:linear-gradient(135deg,#C8102E 0%,#8b0000 100%); color:white;
       font-size:2.4em; font-weight:900; padding:6px 24px; border-radius:10px;
       letter-spacing:4px; font-family:Arial,sans-serif; box-shadow:0 4px 16px rgba(200,16,46,0.35);'>BNI</div>
  <h1 style='color:#C8102E; margin:10px 0 2px 0; font-size:1.85em;'>Chapter Hub</h1>
  <p style='color:#888; margin:0; font-size:0.95em;'>Business Network International — Where Referrals Are Our Business</p>
</div>
""", unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════════════════
# LANDING PAGE
# ═══════════════════════════════════════════════════════════════════════════
if st.session_state["page"] == "landing":
    st.markdown("""
    <div style='text-align:center; margin: 1.5em 0 0.5em 0;'>
      <p style='font-size:1.1em; color:#555; max-width:540px; margin:0 auto 1.5em;'>
        Welcome to your BNI Chapter Hub! Choose your role below to get started.
      </p>
    </div>
    """, unsafe_allow_html=True)

    # Auto-play landing voice
    st.components.v1.html("""
    <script>
    window.addEventListener("load", function(){
        setTimeout(function(){
            if (!window.speechSynthesis) return;
            window.speechSynthesis.cancel();
            var msg = new SpeechSynthesisUtterance(
                "Welcome to the B N I Chapter Hub! " +
                "Are you a visitor today? Tap the visitor button to sign in and connect with our members. " +
                "Are you a B N I member? Tap the member button to log your activity for this week's meeting. " +
                "Givers Gain!"
            );
            msg.rate = 0.92; msg.pitch = 1.05; msg.volume = 1.0;
            var voices = window.speechSynthesis.getVoices();
            var preferred = voices.find(function(v){
                return v.name.indexOf("Google US English") > -1 ||
                       v.name.indexOf("Samantha") > -1 || v.lang === "en-US";
            });
            if (preferred) msg.voice = preferred;
            window.speechSynthesis.speak(msg);
        }, 900);
    });
    </script>
    """, height=0)

    col_land1, col_land2 = st.columns(2, gap="large")

    with col_land1:
        st.markdown("""
        <div class='landing-card landing-card-visitor'>
          <div style='font-size:3.5em; margin-bottom:0.2em;'>&#128075;</div>
          <h2 style='color:#C8102E !important; border:none; margin:0 0 0.4em 0; font-size:1.4em;'>I am a Visitor</h2>
          <p style='color:#666; font-size:0.95em; margin-bottom:1em;'>
            Attending BNI for the first time or as a guest? Sign in here and connect with our amazing members!
          </p>
          <div style='background:#C8102E; color:white; border-radius:8px; padding:10px 0; font-weight:700; font-size:1em; letter-spacing:0.5px;'>
            &#128204; Visitor Sign-In
          </div>
        </div>
        """, unsafe_allow_html=True)
        if st.button("Go to Visitor Sign-In", key="btn_visitor"):
            st.session_state["page"] = "app"
            st.session_state["default_tab"] = 0
            st.rerun()

    with col_land2:
        st.markdown("""
        <div class='landing-card landing-card-member'>
          <div style='font-size:3.5em; margin-bottom:0.2em;'>&#127942;</div>
          <h2 style='color:#27ae60 !important; border:none; margin:0 0 0.4em 0; font-size:1.4em;'>I am a Member</h2>
          <p style='color:#666; font-size:0.95em; margin-bottom:1em;'>
            Log your TYFCB, referrals, and testimonials. Use the voice recorder to capture contributions during the meeting!
          </p>
          <div style='background:#27ae60; color:white; border-radius:8px; padding:10px 0; font-weight:700; font-size:1em; letter-spacing:0.5px;'>
            &#127908; Member Activity Log
          </div>
        </div>
        """, unsafe_allow_html=True)
        if st.button("Go to Member Activity", key="btn_member"):
            st.session_state["page"] = "app"
            st.session_state["default_tab"] = 1
            st.rerun()

    st.markdown("""
    <div style='text-align:center; margin-top:2em; padding:1em; background:#f8f9fa; border-radius:10px; font-size:0.88em; color:#888;'>
      &#128274; Your information is securely stored in the chapter's private Google Sheet.
      &nbsp;|&nbsp; &#127759; Powered by BNI Chapter Hub by Austin Jones &mdash;
      <a href='https://mrceesai.com' style='color:#C8102E;'>mrceesai.com</a>
    </div>
    """, unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════════════════
# MAIN APP (VISITOR + MEMBER TABS)
# ═══════════════════════════════════════════════════════════════════════════
elif st.session_state["page"] == "app":

    # Back to landing
    if st.button("\u2190 Back to Home"):
        st.session_state["page"] = "landing"
        st.rerun()

    default_tab_idx = st.session_state.get("default_tab", 0)

    # ── Email helper functions ────────────────────────────────────────────────
    def send_visitor_welcome(first_name, visitor_email, business_name, interest_level, gmail_user, gmail_pass):
        try:
            msg = MIMEMultipart("alternative")
            msg["Subject"] = f"Great connecting with you at BNI, {first_name}!"
            msg["From"] = gmail_user
            msg["To"] = visitor_email
            html_body = f"""
            <div style="font-family:Arial,sans-serif; max-width:600px; margin:auto;">
              <div style="background:linear-gradient(135deg,#C8102E 0%,#8b0000 100%); color:white; padding:20px 24px; border-radius:10px 10px 0 0;">
                <div style="font-size:2em; font-weight:900; letter-spacing:3px;">BNI</div>
                <h2 style="margin:8px 0 0; color:white !important;">Thanks for Visiting Today, {first_name}!</h2>
              </div>
              <div style="background:#f9f9f9; padding:24px; border-radius:0 0 10px 10px;">
                <p>Hi {first_name},</p>
                <p>Thank you for joining us at BNI! A chapter member will reach out shortly.</p>
                <p><strong>Your business:</strong> {business_name}<br>
                <strong>Your interest level:</strong> {interest_level}</p>
                <p>We hope to see you again next week!</p>
                <hr style="border:none; border-top:1px solid #e0e0e0; margin:20px 0;">
                <p style="font-size:0.85em; color:#888;">
                  <strong>P.S.</strong> Need to automate and grow your business with AI?
                  <a href="https://mrceesai.com" style="color:#C8102E;">Austin Jones at MrCeesAI</a> helps small businesses save time and grow revenue.
                  Visit <a href="https://mrceesai.com" style="color:#C8102E;">mrceesai.com</a>
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

    def send_hot_lead_alert(first_name, last_name, visitor_email, phone, business_name, industry,
                             elevator_pitch, interest_level, gmail_user, gmail_pass, report_email):
        try:
            msg = MIMEMultipart("alternative")
            label = "READY TO APPLY" if interest_level == "Ready to apply!" else "VERY INTERESTED"
            msg["Subject"] = f"BNI HOT LEAD \u2014 {first_name} {last_name} from {business_name} is {label}"
            msg["From"] = gmail_user
            msg["To"] = report_email
            html_body = f"""
            <div style="font-family:Arial,sans-serif; max-width:600px; margin:auto;">
              <div style="background:#27ae60; color:white; padding:16px 24px; border-radius:10px 10px 0 0;">
                <h2 style="margin:0; color:white !important;">&#128293; HOT BNI LEAD \u2014 Call Within 1 Hour!</h2>
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
                <p style="margin-top:16px; color:#27ae60; font-weight:700;">CALL OR TEXT {first_name} NOW \u2014 they are ready!</p>
              </div>
            </div>"""
            msg.attach(MIMEText(html_body, "html"))
            with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
                server.login(gmail_user, gmail_pass)
                server.sendmail(gmail_user, report_email, msg.as_string())
            return True
        except Exception:
            return False

    def send_meeting_report(meeting_date_str, member_rows, visitor_rows, gmail_user, gmail_pass, recipients):
        """Send Thursday 8:30am meeting summary report to Austin, Joel and Elana."""
        try:
            msg = MIMEMultipart("alternative")
            msg["Subject"] = f"BNI Weekly Meeting Report \u2014 {meeting_date_str}"
            msg["From"] = gmail_user
            msg["To"] = ", ".join(recipients)
            tyfcb_count    = sum(1 for r in member_rows if "TYFCB"       in str(r.get("Activity Types","")))
            referral_count = sum(1 for r in member_rows if "Referral"    in str(r.get("Activity Types","")))
            testimonial_count = sum(1 for r in member_rows if "Testimonial" in str(r.get("Activity Types","")))
            member_rows_html = "".join([
                f"<tr style='background:{'#f9f9f9' if i%2 else 'white'};'>"
                f"<td style='padding:6px 8px;'>{r.get('Member Name','')}</td>"
                f"<td style='padding:6px 8px;'>{r.get('Activity Types','')}</td>"
                f"<td style='padding:6px 8px;'>{r.get('TYFCB Value','')}</td>"
                f"<td style='padding:6px 8px; font-size:0.85em; color:#666;'>{r.get('TYFCB Description','')[:60]}...</td>"
                f"</tr>"
                for i, r in enumerate(member_rows)
            ])
            visitor_rows_html = "".join([
                f"<tr style='background:{'#f9f9f9' if i%2 else 'white'};'>"
                f"<td style='padding:6px 8px;'>{r.get('First Name','')} {r.get('Last Name','')}</td>"
                f"<td style='padding:6px 8px;'>{r.get('Business Name','')}</td>"
                f"<td style='padding:6px 8px;'>{r.get('Industry','')}</td>"
                f"<td style='padding:6px 8px;'><strong style='color:#C8102E;'>{r.get('Interest Level','')}</strong></td>"
                f"</tr>"
                for i, r in enumerate(visitor_rows)
            ])
            html_body = f"""
            <div style="font-family:Arial,sans-serif; max-width:700px; margin:auto;">
              <div style="background:linear-gradient(135deg,#C8102E 0%,#8b0000 100%); color:white; padding:22px 28px; border-radius:12px 12px 0 0;">
                <div style="font-size:1.8em; font-weight:900; letter-spacing:3px; margin-bottom:4px;">BNI</div>
                <h2 style="margin:0; color:white !important; font-size:1.4em;">Weekly Meeting Report</h2>
                <p style="margin:6px 0 0; opacity:0.85; font-size:0.95em;">Meeting Date: <strong>{meeting_date_str}</strong></p>
              </div>
              <div style="background:#f9f9f9; padding:24px 28px; border-radius:0 0 12px 12px;">
                <!-- KPI Summary -->
                <table style="width:100%; border-collapse:collapse; margin-bottom:24px;">
                  <tr>
                    <td style="text-align:center; background:#27ae60; color:white; padding:16px; border-radius:10px; width:25%;">
                      <div style="font-size:2em; font-weight:900;">{tyfcb_count}</div>
                      <div style="font-size:0.85em; opacity:0.9;">TYFCBs</div>
                    </td>
                    <td style="width:4%;"></td>
                    <td style="text-align:center; background:#C8102E; color:white; padding:16px; border-radius:10px; width:25%;">
                      <div style="font-size:2em; font-weight:900;">{referral_count}</div>
                      <div style="font-size:0.85em; opacity:0.9;">Referrals</div>
                    </td>
                    <td style="width:4%;"></td>
                    <td style="text-align:center; background:#8e44ad; color:white; padding:16px; border-radius:10px; width:25%;">
                      <div style="font-size:2em; font-weight:900;">{testimonial_count}</div>
                      <div style="font-size:0.85em; opacity:0.9;">Testimonials</div>
                    </td>
                    <td style="width:4%;"></td>
                    <td style="text-align:center; background:#2980b9; color:white; padding:16px; border-radius:10px; width:17%;">
                      <div style="font-size:2em; font-weight:900;">{len(visitor_rows)}</div>
                      <div style="font-size:0.85em; opacity:0.9;">Visitors</div>
                    </td>
                  </tr>
                </table>
                <!-- Member Activity -->
                <h3 style="color:#27ae60; margin-top:0;">&#127942; Member Activity This Week ({len(member_rows)} members)</h3>
                <table style="width:100%; border-collapse:collapse; font-size:0.92em; margin-bottom:24px;">
                  <thead>
                    <tr style="background:#27ae60; color:white;">
                      <th style="padding:8px; text-align:left;">Member</th>
                      <th style="padding:8px; text-align:left;">Activities</th>
                      <th style="padding:8px; text-align:left;">TYFCB Value</th>
                      <th style="padding:8px; text-align:left;">Details</th>
                    </tr>
                  </thead>
                  <tbody>{member_rows_html if member_rows_html else "<tr><td colspan='4' style='padding:12px; color:#999; text-align:center;'>No member activity logged this week</td></tr>"}</tbody>
                </table>
                <!-- Visitors -->
                <h3 style="color:#C8102E; margin-top:0;">&#128075; Visitors This Week ({len(visitor_rows)} visitors)</h3>
                <table style="width:100%; border-collapse:collapse; font-size:0.92em; margin-bottom:24px;">
                  <thead>
                    <tr style="background:#C8102E; color:white;">
                      <th style="padding:8px; text-align:left;">Name</th>
                      <th style="padding:8px; text-align:left;">Business</th>
                      <th style="padding:8px; text-align:left;">Industry</th>
                      <th style="padding:8px; text-align:left;">Interest</th>
                    </tr>
                  </thead>
                  <tbody>{visitor_rows_html if visitor_rows_html else "<tr><td colspan='4' style='padding:12px; color:#999; text-align:center;'>No visitors this week</td></tr>"}</tbody>
                </table>
                <p style="font-size:0.8em; color:#aaa; margin-top:20px; text-align:center;">
                  Automated by BNI Chapter Hub &mdash; <a href="https://mrceesai.com" style="color:#C8102E;">mrceesai.com</a>
                </p>
              </div>
            </div>"""
            msg.attach(MIMEText(html_body, "html"))
            with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
                server.login(gmail_user, gmail_pass)
                server.sendmail(gmail_user, recipients, msg.as_string())
            return True
        except Exception as e:
            return False

    # ── BNI Tips ─────────────────────────────────────────────────────────────
    BNI_TIPS = [
        "&#128161; <strong>BNI Tip:</strong> The most successful BNI members give referrals before expecting to receive them.",
        "&#128161; <strong>BNI Tip:</strong> Your 60-second pitch should be crystal-clear — the easier you make it to refer you, the more referrals you'll get!",
        "&#128161; <strong>BNI Tip:</strong> BNI members generate an average of $50,000+ in new business per year through referrals.",
        "&#128161; <strong>BNI Tip:</strong> Givers Gain&#174; — members who give the most referrals consistently receive the most in return.",
        "&#128161; <strong>BNI Tip:</strong> Each member holds one seat per profession — securing your seat locks out competitors!",
        "&#128161; <strong>BNI Tip:</strong> 1-2-1 meetings with fellow members are the #1 driver of strong referral relationships.",
        "&#128161; <strong>BNI Tip:</strong> The average BNI chapter passes over $1 million in referrals each year.",
    ]
    random_tip = random.choice(BNI_TIPS)

    tab_visitor, tab_member = st.tabs(["\U0001f91d Visitor Sign-In", "\U0001f3c6 Member Activity Log"])

    # ═══════════════════════════════════════════════════════════════════════
    # TAB 1 — VISITOR SIGN-IN
    # ═══════════════════════════════════════════════════════════════════════
    with tab_visitor:
        # Voice Welcome Banner
        st.components.v1.html("""
        <div id="voice-banner" style="
            background: linear-gradient(135deg,#C8102E 0%,#a00d24 100%);
            color: white; border-radius: 12px; padding: 14px 20px; margin-bottom: 10px;
            display: flex; align-items: center; gap: 14px;
            box-shadow: 0 4px 16px rgba(200,16,46,0.25); cursor: pointer; transition: transform 0.15s;"
            onclick="speakWelcome()" title="Click to hear welcome message">
          <span style="font-size:2em;">&#128266;</span>
          <div>
            <div style="font-weight:700; font-size:1.05em;">Tap to hear a welcome message!</div>
            <div style="font-size:0.85em; opacity:0.85;">Click the speaker icon to have BNI greet you out loud</div>
          </div>
        </div>
        <script>
        function speakWelcome() {
            if (!window.speechSynthesis) return;
            window.speechSynthesis.cancel();
            var msg = new SpeechSynthesisUtterance(
                "Welcome to our B N I chapter! We are so excited to have you here today. " +
                "B N I stands for Business Network International, where referrals are our business. " +
                "Please take just two minutes to fill out this quick form and one of our members " +
                "will personally reach out to help grow your business. We cannot wait to connect with you!"
            );
            msg.rate = 0.92; msg.pitch = 1.05; msg.volume = 1.0;
            var voices = window.speechSynthesis.getVoices();
            var preferred = voices.find(function(v){
                return v.name.indexOf("Google US English") > -1 ||
                       v.name.indexOf("Samantha") > -1 || v.lang === "en-US";
            });
            if (preferred) msg.voice = preferred;
            window.speechSynthesis.speak(msg);
            document.getElementById("voice-banner").style.transform = "scale(0.97)";
            setTimeout(function(){ document.getElementById("voice-banner").style.transform = "scale(1)"; }, 200);
        }
        window.addEventListener("load", function(){ setTimeout(speakWelcome, 800); });
        </script>
        """, height=80)

        st.markdown(f"""
        <div class='intro-box'>
          <strong>Thanks for visiting today!</strong> Take 2 minutes to fill out this quick form
          and our members will follow up to help grow your business. We cannot wait to connect!
        </div>
        <div class='tip-box'>{random_tip}</div>
        """, unsafe_allow_html=True)

        with st.form("visitor_form", clear_on_submit=True):
            st.markdown("## Contact Information")
            col1, col2 = st.columns(2)
            with col1:
                first_name = st.text_input("First Name *", placeholder="Jane")
                email      = st.text_input("Email Address *", placeholder="jane@example.com")
                phone      = st.text_input("Phone Number", placeholder="(555) 555-5555")
            with col2:
                last_name  = st.text_input("Last Name *", placeholder="Smith")
                city       = st.text_input("City / Area", placeholder="Atlanta, GA")
                website    = st.text_input("Website", placeholder="www.yoursite.com")

            st.markdown("## Social Media")
            col3, col4 = st.columns(2)
            with col3:
                linkedin  = st.text_input("LinkedIn",  placeholder="linkedin.com/in/yourname")
                instagram = st.text_input("Instagram", placeholder="@yourhandle")
            with col4:
                facebook  = st.text_input("Facebook",  placeholder="facebook.com/yourpage")
                twitter_x = st.text_input("X / Twitter", placeholder="@yourhandle")

            st.markdown("## Your Business")
            business_name = st.text_input("Business Name *", placeholder="Smith Consulting LLC")
            industry = st.selectbox("Industry / Profession *", [
                "Select one...", "Accounting / Finance", "Attorney / Legal", "Banking / Lending",
                "Chiropractor / Health", "Construction / Contracting", "Consulting / Coaching",
                "Digital Marketing", "Financial Planning", "Health & Wellness", "Home Services / Remodeling",
                "HR / Staffing", "Insurance", "IT / Technology / Cybersecurity", "Mortgage / Real Estate",
                "Photography / Videography", "Printing / Signage / Design", "Restaurant / Catering / Food",
                "Retail / E-Commerce", "Travel / Hospitality", "Other"
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
                options=["Less than 1 year","1-2 years","3-5 years","6-10 years","10+ years"]
            )

            st.markdown("## Networking & Referrals")
            col5, col6 = st.columns(2)
            with col5:
                ideal_referral = st.text_area("What does your ideal referral look like?",
                    placeholder="e.g. A homeowner aged 35-55 who recently bought a house...", height=100)
            with col6:
                top_clients = st.text_area("Top 3 types of clients or industries you serve?",
                    placeholder="e.g. Real estate agents, small business owners, HR managers...", height=100)
            how_heard  = st.selectbox("How did you hear about our chapter?", [
                "Select one...", "Invited by a member", "BNI website / Find a Chapter",
                "Social media", "Google search", "Friend / colleague", "Attended before", "Other"
            ])
            invited_by = st.text_input("If invited by a member — who invited you?", placeholder="Member name")

            st.markdown("## Goals & Interest Level")
            looking_for = st.multiselect("What are you hoping to get from BNI? (select all that apply)", [
                "More qualified referrals","Grow my professional network","Business accountability",
                "Learn from other business owners","Give referrals to others","Greater brand visibility",
                "Find trusted vendors & partners","Structured networking system"
            ])
            has_bni_before = st.radio(
                "Have you visited or been a BNI member before?",
                ["No — first time!", "Visited before but never joined", "Former BNI member"], horizontal=True
            )
            biggest_challenge = st.text_area(
                "What is your biggest business challenge right now?",
                placeholder="e.g. Generating consistent leads, standing out from competitors...", height=80
            )
            ready_to_join = st.select_slider(
                "How interested are you in joining our chapter?",
                options=["Just exploring","Somewhat interested","Very interested","Ready to apply!"]
            )
            notes = st.text_area("Anything else you would like us to know? (optional)", height=70)

            v_submitted = st.form_submit_button("\U0001f91d Submit — We Will Be In Touch!")

        if v_submitted:
            errors = []
            if not first_name.strip():    errors.append("First Name")
            if not last_name.strip():     errors.append("Last Name")
            if not email.strip():         errors.append("Email Address")
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
                    timestamp, first_name.strip(), last_name.strip(), email.strip(), phone.strip(),
                    city.strip(), website.strip(), linkedin.strip(), instagram.strip(),
                    facebook.strip(), twitter_x.strip(), business_name.strip(), final_industry,
                    elevator_pitch.strip(), years_in_biz, ideal_referral.strip(), top_clients.strip(),
                    how_heard, invited_by.strip(), ", ".join(looking_for), has_bni_before,
                    biggest_challenge.strip(), ready_to_join, notes.strip()
                ]
                try:
                    creds_dict = json.loads(st.secrets["GOOGLE_CREDS"])
                    creds = Credentials.from_service_account_info(creds_dict, scopes=[
                        "https://spreadsheets.google.com/feeds",
                        "https://www.googleapis.com/auth/drive"
                    ])
                    client = gspread.authorize(creds)
                    sheet = client.open(st.secrets["SHEET_NAME"]).sheet1
                    sheet.append_row(row)
                except Exception as e:
                    st.warning(f"Note: Could not save to visitor sheet — {e}")
                try:
                    gmail_user_v  = st.secrets["GMAIL_USER"]
                    gmail_pass_v  = st.secrets["GMAIL_APP_PASSWORD"]
                    report_email_v = st.secrets["REPORT_EMAIL"]
                    send_visitor_welcome(first_name.strip(), email.strip(), business_name.strip(),
                                         ready_to_join, gmail_user_v, gmail_pass_v)
                    if ready_to_join in ["Ready to apply!", "Very interested"]:
                        send_hot_lead_alert(
                            first_name.strip(), last_name.strip(), email.strip(), phone.strip(),
                            business_name.strip(), final_industry, elevator_pitch.strip(),
                            ready_to_join, gmail_user_v, gmail_pass_v, report_email_v
                        )
                except KeyError:
                    pass
                except Exception:
                    pass

                st.components.v1.html("""
                <canvas id="confetti-canvas" style="position:fixed;top:0;left:0;width:100vw;height:100vh;pointer-events:none;z-index:9999;"></canvas>
                <script>
                (function(){
                    var canvas=document.getElementById("confetti-canvas");
                    var ctx=canvas.getContext("2d");
                    canvas.width=window.innerWidth; canvas.height=window.innerHeight;
                    var colors=["#C8102E","#FFD700","#27ae60","#3498db","#f39c12","#9b59b6","#ffffff","#e74c3c"];
                    var pieces=[];
                    for(var i=0;i<180;i++) pieces.push({
                        x:Math.random()*canvas.width, y:Math.random()*canvas.height-canvas.height,
                        w:Math.random()*10+6, h:Math.random()*5+4,
                        color:colors[Math.floor(Math.random()*colors.length)],
                        rot:Math.random()*360, vx:Math.random()*2-1, vy:Math.random()*4+2, vr:Math.random()*6-3
                    });
                    var frame=0;
                    function draw(){
                        ctx.clearRect(0,0,canvas.width,canvas.height);
                        pieces.forEach(function(p){
                            ctx.save(); ctx.translate(p.x,p.y); ctx.rotate(p.rot*Math.PI/180);
                            ctx.fillStyle=p.color; ctx.globalAlpha=0.87;
                            ctx.fillRect(-p.w/2,-p.h/2,p.w,p.h); ctx.restore();
                            p.x+=p.vx; p.y+=p.vy; p.rot+=p.vr;
                            if(p.y>canvas.height){p.y=-10; p.x=Math.random()*canvas.width;}
                        });
                        frame++; if(frame<220) requestAnimationFrame(draw);
                        else ctx.clearRect(0,0,canvas.width,canvas.height);
                    }
                    draw();
                    if(window.speechSynthesis){
                        window.speechSynthesis.cancel();
                        var msg=new SpeechSynthesisUtterance(
                            "Thank you for registering! A B N I member will reach out very soon. We are so excited to connect with you!");
                        msg.rate=0.93; msg.pitch=1.1;
                        window.speechSynthesis.speak(msg);
                    }
                })();
                </script>
                """, height=0)
                st.balloons()
                st.markdown(f"""
                <div class='success-card'>
                  <h3 style='color:#27ae60; margin-top:0;'>&#127881; Thanks, {first_name}! You are all set.</h3>
                  <table style='width:100%; font-size:0.95em; border-collapse:collapse;'>
                    <tr><td style='padding:5px 8px; color:#555; width:110px;'><strong>Name</strong></td><td style='padding:5px 8px;'>{first_name} {last_name}</td></tr>
                    <tr style='background:#f0fff4;'><td style='padding:5px 8px; color:#555;'><strong>Business</strong></td><td style='padding:5px 8px;'>{business_name}</td></tr>
                    <tr><td style='padding:5px 8px; color:#555;'><strong>Industry</strong></td><td style='padding:5px 8px;'>{final_industry}</td></tr>
                    <tr style='background:#f0fff4;'><td style='padding:5px 8px; color:#555;'><strong>Email</strong></td><td style='padding:5px 8px;'>{email}</td></tr>
                    <tr><td style='padding:5px 8px; color:#555;'><strong>Interest</strong></td><td style='padding:5px 8px;'><strong style='color:#C8102E;'>{ready_to_join}</strong></td></tr>
                  </table>
                  <div style='background:#fff; border:1px solid #c3e6cb; border-radius:8px; padding:10px 14px; margin-top:12px; font-size:0.9em; color:#27ae60;'>
                    <strong>What happens next?</strong><br>
                    &#10003; A BNI member contacts you within 24 hours.<br>
                    &#10003; You will be invited to a 1-2-1 coffee meeting.<br>
                    &#10003; You can apply for membership and lock in your profession!
                  </div>
                </div>
                """, unsafe_allow_html=True)

    # ═══════════════════════════════════════════════════════════════════════
    # TAB 2 — MEMBER ACTIVITY LOG (with Voice Recording)
    # ═══════════════════════════════════════════════════════════════════════
    with tab_member:
        # Voice Welcome Banner
        st.components.v1.html("""
        <div id="member-voice-banner" style="
            background: linear-gradient(135deg,#27ae60 0%,#1e8449 100%);
            color: white; border-radius: 12px; padding: 14px 20px; margin-bottom: 10px;
            display: flex; align-items: center; gap: 14px;
            box-shadow: 0 4px 16px rgba(39,174,96,0.25); cursor: pointer; transition: transform 0.15s;"
            onclick="speakMemberWelcome()" title="Click to hear member instructions">
          <span style="font-size:2em;">&#127942;</span>
          <div>
            <div style="font-weight:700; font-size:1.05em;">Member Activity Log — Tap to hear instructions!</div>
            <div style="font-size:0.85em; opacity:0.88;">Log your TYFCB, Referrals, and Testimonials for today's meeting</div>
          </div>
        </div>
        <script>
        function speakMemberWelcome() {
            if (!window.speechSynthesis) return;
            window.speechSynthesis.cancel();
            var msg = new SpeechSynthesisUtterance(
                "Welcome, B N I member! Use the voice recorder below to speak your contributions during the meeting. " +
                "Press Start Recording, say your name, and then say whether you have a thank you for closed business, " +
                "a referral to pass, or a testimonial to give. Press Stop when done. " +
                "Then verify the details in the form below and click Submit. Givers Gain!"
            );
            msg.rate = 0.92; msg.pitch = 1.0; msg.volume = 1.0;
            var voices = window.speechSynthesis.getVoices();
            var preferred = voices.find(function(v){
                return v.name.indexOf("Google US English") > -1 ||
                       v.name.indexOf("Samantha") > -1 || v.lang === "en-US";
            });
            if (preferred) msg.voice = preferred;
            window.speechSynthesis.speak(msg);
            document.getElementById("member-voice-banner").style.transform = "scale(0.97)";
            setTimeout(function(){ document.getElementById("member-voice-banner").style.transform = "scale(1)"; }, 200);
        }
        </script>
        """, height=80)

        # ── VOICE RECORDER SECTION ────────────────────────────────────────────
        st.markdown("""
        <div class='recording-box'>
          <div style='font-size:1.1em; font-weight:700; margin-bottom:6px;'>&#127908; Voice Recorder — Speak Your Meeting Contributions</div>
          <div style='font-size:0.87em; opacity:0.80; margin-bottom:12px;'>
            Press <strong>Start Recording</strong> when your turn comes during the Zoom meeting.
            Speak naturally: your name, TYFCB, referrals, and testimonials.
            Press <strong>Stop Recording</strong> when done. Your transcript appears below.
          </div>
        </div>
        """, unsafe_allow_html=True)

        st.components.v1.html("""
        <div id="recorder-wrap" style="font-family:Arial,sans-serif; padding:0 0 10px 0;">
          <!-- Status indicator -->
          <div id="rec-status" style="
              display:flex; align-items:center; gap:10px; margin-bottom:10px;
              background:#1a1a2e; border-radius:8px; padding:10px 14px; color:white; font-size:0.9em;">
            <div id="rec-dot" style="width:12px; height:12px; border-radius:50%; background:#555; flex-shrink:0;"></div>
            <span id="rec-status-text">Ready to record. Press Start when it is your turn.</span>
            <span id="rec-timer" style="margin-left:auto; font-family:monospace; color:#58a6ff;">0:00</span>
          </div>

          <!-- Buttons -->
          <div style="display:flex; gap:10px; margin-bottom:10px;">
            <button id="btn-start" onclick="startRecording()" style="
                flex:1; background:linear-gradient(135deg,#27ae60,#1e8449); color:white;
                border:none; border-radius:8px; padding:12px 0; font-size:1em; font-weight:700;
                cursor:pointer; transition:all 0.2s;">
              &#9654; Start Recording
            </button>
            <button id="btn-stop" onclick="stopRecording()" disabled style="
                flex:1; background:#555; color:white;
                border:none; border-radius:8px; padding:12px 0; font-size:1em; font-weight:700;
                cursor:not-allowed; transition:all 0.2s;">
              &#9632; Stop Recording
            </button>
          </div>

          <!-- Live transcript -->
          <div style="margin-bottom:6px; font-size:0.85em; color:#555; font-weight:600;">LIVE TRANSCRIPT:</div>
          <div id="transcript-box" style="
              background:#0d1117; color:#58a6ff; font-family:monospace; font-size:0.88em;
              border-radius:8px; padding:10px 14px; min-height:80px; border:1px solid #30363d;
              white-space:pre-wrap; margin-bottom:8px;">Press Start Recording to begin...</div>

          <!-- Copy transcript button -->
          <button id="btn-copy" onclick="copyTranscript()" style="
              background:#2c3e50; color:white; border:none; border-radius:6px;
              padding:7px 16px; font-size:0.85em; cursor:pointer; margin-bottom:4px;">
            &#128203; Copy Transcript
          </button>
          <div id="copy-status" style="font-size:0.8em; color:#27ae60; display:none; margin-left:8px;">Copied!</div>
        </div>

        <script>
        var mediaRecorder = null;
        var recognition = null;
        var fullTranscript = "";
        var timerInterval = null;
        var secondsElapsed = 0;
        var isRecording = false;

        function formatTime(s) {
            var m = Math.floor(s/60);
            var sec = s % 60;
            return m + ":" + (sec < 10 ? "0" : "") + sec;
        }

        function startRecording() {
            if (isRecording) return;
            isRecording = true;
            fullTranscript = "";
            secondsElapsed = 0;
            document.getElementById("transcript-box").textContent = "";
            document.getElementById("rec-dot").style.background = "#e74c3c";
            document.getElementById("rec-dot").style.animation = "blink 1s infinite";
            document.getElementById("rec-status-text").textContent = "Recording... speak now!";
            document.getElementById("btn-start").disabled = true;
            document.getElementById("btn-start").style.background = "#888";
            document.getElementById("btn-start").style.cursor = "not-allowed";
            document.getElementById("btn-stop").disabled = false;
            document.getElementById("btn-stop").style.background = "linear-gradient(135deg,#C8102E,#8b0000)";
            document.getElementById("btn-stop").style.cursor = "pointer";

            // Start timer
            timerInterval = setInterval(function(){
                secondsElapsed++;
                document.getElementById("rec-timer").textContent = formatTime(secondsElapsed);
            }, 1000);

            // Speech recognition
            var SpeechRec = window.SpeechRecognition || window.webkitSpeechRecognition;
            if (SpeechRec) {
                recognition = new SpeechRec();
                recognition.continuous = true;
                recognition.interimResults = true;
                recognition.lang = "en-US";
                var interimText = "";
                recognition.onresult = function(event) {
                    interimText = "";
                    for (var i = event.resultIndex; i < event.results.length; i++) {
                        if (event.results[i].isFinal) {
                            fullTranscript += event.results[i][0].transcript + " ";
                        } else {
                            interimText += event.results[i][0].transcript;
                        }
                    }
                    document.getElementById("transcript-box").textContent =
                        fullTranscript + (interimText ? "[..." + interimText + "]" : "");
                };
                recognition.onerror = function(e) {
                    if (e.error !== "no-speech") {
                        document.getElementById("rec-status-text").textContent = "Mic error: " + e.error + ". Check browser permissions.";
                    }
                };
                recognition.onend = function() {
                    if (isRecording) recognition.start();
                };
                recognition.start();
            } else {
                document.getElementById("transcript-box").textContent =
                    "Live transcription not supported in this browser. Recording audio only.\n" +
                    "(Chrome recommended for live transcription)";
            }

            // Also record audio for backup
            navigator.mediaDevices.getUserMedia({ audio: true }).then(function(stream) {
                mediaRecorder = new MediaRecorder(stream);
                var chunks = [];
                mediaRecorder.ondataavailable = function(e) { if (e.data.size > 0) chunks.push(e.data); };
                mediaRecorder.onstop = function() {
                    // Audio recorded — transcript is the primary output
                    stream.getTracks().forEach(function(t){ t.stop(); });
                };
                mediaRecorder.start();
            }).catch(function(err) {
                console.warn("Audio capture not available:", err);
            });
        }

        function stopRecording() {
            if (!isRecording) return;
            isRecording = false;
            clearInterval(timerInterval);
            document.getElementById("rec-dot").style.background = "#27ae60";
            document.getElementById("rec-dot").style.animation = "none";
            document.getElementById("rec-status-text").textContent =
                "Recording stopped. Transcript saved below (" + formatTime(secondsElapsed) + ").";
            document.getElementById("btn-start").disabled = false;
            document.getElementById("btn-start").style.background = "linear-gradient(135deg,#27ae60,#1e8449)";
            document.getElementById("btn-start").style.cursor = "pointer";
            document.getElementById("btn-stop").disabled = true;
            document.getElementById("btn-stop").style.background = "#555";
            document.getElementById("btn-stop").style.cursor = "not-allowed";
            if (recognition) { try { recognition.stop(); } catch(e){} recognition = null; }
            if (mediaRecorder && mediaRecorder.state !== "inactive") { mediaRecorder.stop(); }
            if (window.speechSynthesis) {
                window.speechSynthesis.cancel();
                var msg = new SpeechSynthesisUtterance(
                    "Recording complete. Please review your transcript and fill in the details below, then click Submit.");
                msg.rate = 0.93; msg.pitch = 1.0;
                window.speechSynthesis.speak(msg);
            }
        }

        function copyTranscript() {
            var text = document.getElementById("transcript-box").textContent;
            navigator.clipboard.writeText(text).then(function(){
                var s = document.getElementById("copy-status");
                s.style.display = "inline";
                setTimeout(function(){ s.style.display = "none"; }, 2500);
            });
        }

        var style = document.createElement("style");
        style.textContent = "@keyframes blink { 0%,100%{opacity:1;} 50%{opacity:0.2;} }";
        document.head.appendChild(style);
        </script>
        """, height=320)

        st.markdown("""
        <div class='member-intro-box'>
          <strong>Members — use the voice recorder above, then complete the form below to log your contributions.</strong>
          Your TYFCB, referrals, and testimonials are automatically saved to the chapter's Google Sheet
          and included in the Thursday 8:30 AM meeting report sent to chapter leadership.
        </div>
        """, unsafe_allow_html=True)

        with st.expander("&#129300; What do these mean? (click to expand)", expanded=False):
            st.markdown("""
**&#127881; Thank You for Closed Business (TYFCB)**
> Someone referred business TO you and it CLOSED! You are publicly thanking the member whose referral turned into revenue. Include the value if you can — it motivates the whole chapter!

**&#128279; Referral Passed**
> You are passing a referral TO another member — connecting them with someone who could use their services. Include who you referred and to whom.

**&#11088; Testimonial**
> A positive testimonial ABOUT another member's work, character, or results. This builds trust and credibility for that member in front of the chapter.
            """)

        with st.form("member_form", clear_on_submit=True):
            st.markdown("## Your Information")
            col_m1, col_m2 = st.columns(2)
            with col_m1:
                member_name = st.text_input("Your Full Name *", placeholder="e.g. John Smith")
            with col_m2:
                member_profession = st.text_input("Your Profession / Category", placeholder="e.g. Insurance Agent")

            st.markdown("## Meeting Date & Location")
            col_m3, col_m4 = st.columns(2)
            with col_m3:
                meeting_date = st.date_input("Meeting Date", value=datetime.today())
            with col_m4:
                chapter_name = st.text_input("Chapter Name (optional)", placeholder="e.g. BNI Champions")

            st.markdown("## &#127881; Thank You for Closed Business (TYFCB)")
            has_tyfcb = st.checkbox("I have a Thank You for Closed Business to share")
            tyfcb_member = ""; tyfcb_amount = ""; tyfcb_details = ""
            if has_tyfcb:
                col_t1, col_t2 = st.columns(2)
                with col_t1:
                    tyfcb_member = st.text_input("Which member referred the business? *",
                        placeholder="Member name", key="tyfcb_member")
                with col_t2:
                    tyfcb_amount = st.text_input("Approximate value of closed business",
                        placeholder="e.g. $2,500", key="tyfcb_amount")
                tyfcb_details = st.text_area("Brief description (what was the business?)",
                    placeholder="e.g. John referred me to ABC Corp for a 3-month insurance review...",
                    height=80, key="tyfcb_details")

            st.markdown("## &#128279; Referral(s) Passed")
            has_referral = st.checkbox("I am passing one or more referrals today")
            referral_details_list = ""
            if has_referral:
                st.selectbox("How many referrals are you passing?", ["1","2","3","4","5+"], key="num_ref")
                referral_details_list = st.text_area(
                    "Referral details *",
                    placeholder="List each referral: e.g. To Jane Smith (Insurance) referred Mike Brown at ABC Corp",
                    height=120, key="ref_details"
                )

            st.markdown("## &#11088; Testimonial")
            has_testimonial = st.checkbox("I have a testimonial to give for a chapter member")
            testimonial_for = ""; testimonial_text = ""
            if has_testimonial:
                testimonial_for = st.text_input("Testimonial for which member? *",
                    placeholder="Member name", key="test_for")
                testimonial_text = st.text_area(
                    "Your testimonial *",
                    placeholder="e.g. I just want to recognize Sarah Jones — she helped me redesign my website and leads doubled in 30 days!",
                    height=100, key="test_text"
                )

            st.markdown("## Voice Transcript (paste from recorder above — optional)")
            voice_transcript = st.text_area(
                "Paste your voice recording transcript here for the report record",
                placeholder="Paste the transcript from the voice recorder above (optional but recommended for accuracy)",
                height=90, key="voice_trans"
            )

            st.markdown("## Additional Notes")
            member_notes = st.text_area(
                "Anything else to share with the chapter? (optional)",
                placeholder="e.g. Announcements, 1-2-1 requests, upcoming events...",
                height=70, key="mnotes"
            )

            m_submitted = st.form_submit_button("&#127942; Submit My Activity")

        if m_submitted:
            m_errors = []
            if not member_name.strip(): m_errors.append("Your Full Name")
            if has_tyfcb and not tyfcb_member.strip():  m_errors.append("Member who referred the business (TYFCB)")
            if has_tyfcb and not tyfcb_details.strip():  m_errors.append("TYFCB description")
            if has_referral and not referral_details_list.strip(): m_errors.append("Referral details")
            if has_testimonial and not testimonial_for.strip():    m_errors.append("Testimonial recipient name")
            if has_testimonial and not testimonial_text.strip():   m_errors.append("Testimonial text")
            if not has_tyfcb and not has_referral and not has_testimonial:
                m_errors.append("At least one activity (TYFCB, Referral, or Testimonial) must be selected")
            if m_errors:
                st.error("Please complete: " + ", ".join(m_errors))
            else:
                m_timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                m_date_str = meeting_date.strftime("%Y-%m-%d")
                activity_types = []
                if has_tyfcb:       activity_types.append("TYFCB")
                if has_referral:    activity_types.append("Referral")
                if has_testimonial: activity_types.append("Testimonial")
                m_row = [
                    m_timestamp, m_date_str, member_name.strip(), member_profession.strip(),
                    chapter_name.strip(), ", ".join(activity_types),
                    "Yes" if has_tyfcb else "No",
                    tyfcb_member.strip() if has_tyfcb else "",
                    tyfcb_amount.strip() if has_tyfcb else "",
                    tyfcb_details.strip() if has_tyfcb else "",
                    "Yes" if has_referral else "No",
                    referral_details_list.strip() if has_referral else "",
                    "Yes" if has_testimonial else "No",
                    testimonial_for.strip() if has_testimonial else "",
                    testimonial_text.strip() if has_testimonial else "",
                    voice_transcript.strip(),
                    member_notes.strip()
                ]
                try:
                    creds_dict = json.loads(st.secrets["GOOGLE_CREDS"])
                    creds = Credentials.from_service_account_info(creds_dict, scopes=[
                        "https://spreadsheets.google.com/feeds",
                        "https://www.googleapis.com/auth/drive"
                    ])
                    client = gspread.authorize(creds)
                    spreadsheet = client.open(st.secrets["SHEET_NAME"])
                    try:
                        m_sheet = spreadsheet.worksheet("Member Activity")
                    except Exception:
                        m_sheet = spreadsheet.add_worksheet(title="Member Activity", rows="1000", cols="20")
                        m_sheet.append_row([
                            "Timestamp","Meeting Date","Member Name","Profession","Chapter",
                            "Activity Types","Has TYFCB","TYFCB From Member","TYFCB Value","TYFCB Description",
                            "Has Referral","Referral Details","Has Testimonial","Testimonial For","Testimonial Text",
                            "Voice Transcript","Notes"
                        ])
                    m_sheet.append_row(m_row)
                except Exception as e:
                    st.warning(f"Note: Could not save to sheet — {e}")

                # Send report immediately after member submits
                try:
                    gmail_user_m  = st.secrets["GMAIL_USER"]
                    gmail_pass_m  = st.secrets["GMAIL_APP_PASSWORD"]
                    report_to     = ["ausjones84@gmail.com"]
                    extra = st.secrets.get("REPORT_EMAIL", "")
                    if extra and extra not in report_to:
                        report_to.append(extra)
                    # Build simple row dict for report
                    member_row_dict = {
                        "Member Name": member_name.strip(),
                        "Activity Types": ", ".join(activity_types),
                        "TYFCB Value": tyfcb_amount.strip() if has_tyfcb else "",
                        "TYFCB Description": tyfcb_details.strip() if has_tyfcb else ""
                    }
                    send_meeting_report(m_date_str, [member_row_dict], [], gmail_user_m, gmail_pass_m, report_to)
                except KeyError:
                    pass
                except Exception:
                    pass

                badges_html = ""
                if has_tyfcb:       badges_html += "<span class='badge-tyfcb'>&#127881; TYFCB</span>"
                if has_referral:    badges_html += "<span class='badge-referral'>&#128279; Referral Passed</span>"
                if has_testimonial: badges_html += "<span class='badge-testimonial'>&#11088; Testimonial</span>"

                st.components.v1.html(f"""
                <script>
                if(window.speechSynthesis){{
                    window.speechSynthesis.cancel();
                    var msg = new SpeechSynthesisUtterance(
                        "Great job, {member_name.strip()}! Your activity has been logged. " +
                        "You recorded: {', '.join(activity_types)}. " +
                        "Givers Gain! Thank you for contributing to our chapter!"
                    );
                    msg.rate=0.93; msg.pitch=1.05;
                    window.speechSynthesis.speak(msg);
                }}
                </script>
                """, height=0)
                st.balloons()
                st.markdown(f"""
                <div class='member-success-card'>
                  <h3 style='color:#2980b9; margin-top:0;'>&#127942; Logged, {member_name.strip()}! Great meeting contribution.</h3>
                  <div style='margin:10px 0;'>{badges_html}</div>
                  <table style='width:100%; font-size:0.95em; border-collapse:collapse; margin-top:12px;'>
                    <tr><td style='padding:5px 8px; color:#555; width:130px;'><strong>Member</strong></td><td style='padding:5px 8px;'>{member_name.strip()}</td></tr>
                    <tr style='background:#f0f8ff;'><td style='padding:5px 8px; color:#555;'><strong>Profession</strong></td><td style='padding:5px 8px;'>{member_profession.strip() or "&#8212;"}</td></tr>
                    <tr><td style='padding:5px 8px; color:#555;'><strong>Meeting Date</strong></td><td style='padding:5px 8px;'>{m_date_str}</td></tr>
                    <tr style='background:#f0f8ff;'><td style='padding:5px 8px; color:#555;'><strong>Activities</strong></td><td style='padding:5px 8px;'>{", ".join(activity_types)}</td></tr>
                    {"<tr><td style='padding:5px 8px; color:#555;'><strong>TYFCB From</strong></td><td style='padding:5px 8px;'>" + tyfcb_member.strip() + (" &mdash; " + tyfcb_amount.strip() if tyfcb_amount.strip() else "") + "</td></tr>" if has_tyfcb else ""}
                    {"<tr style='background:#f0f8ff;'><td style='padding:5px 8px; color:#555;'><strong>Testimonial For</strong></td><td style='padding:5px 8px;'>" + testimonial_for.strip() + "</td></tr>" if has_testimonial else ""}
                  </table>
                  <p style='margin-top:14px; color:#555; font-size:0.92em;'>
                    Saved to <strong>Member Activity</strong> tab in the Google Sheet.
                    A meeting report has been sent to chapter leadership. Keep giving, keep growing! &#127881;
                  </p>
                </div>
                """, unsafe_allow_html=True)
