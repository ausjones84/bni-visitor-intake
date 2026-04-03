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
    page_title="BNI Visitor Registration",
    page_icon="\U0001f91d",
    layout="centered"
)

# ── Voice Welcome (Web Speech API) ──────────────────────────────────────────
st.components.v1.html("""
<div id="voice-banner" style="
    background: linear-gradient(135deg,#C8102E 0%,#a00d24 100%);
    color: white;
    border-radius: 12px;
    padding: 14px 20px;
    margin-bottom: 10px;
    display: flex;
    align-items: center;
    gap: 14px;
    box-shadow: 0 4px 16px rgba(200,16,46,0.25);
    cursor: pointer;
    transition: transform 0.15s;
" onclick="speakWelcome()" title="Click to hear welcome message">
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
    "B N I stands for Business Network International — where referrals are our business. " +
    "Please take just two minutes to fill out this quick form and one of our members " +
    "will personally reach out to help grow your business. " +
    "We cannot wait to connect with you!"
  );
  msg.rate = 0.92;
  msg.pitch = 1.05;
  msg.volume = 1.0;
  var voices = window.speechSynthesis.getVoices();
  var preferred = voices.find(function(v){ return v.name.indexOf("Google US English") > -1 || v.name.indexOf("Samantha") > -1 || v.name.indexOf("Karen") > -1 || v.lang === "en-US"; });
  if (preferred) msg.voice = preferred;
  window.speechSynthesis.speak(msg);
  document.getElementById("voice-banner").style.transform = "scale(0.97)";
  setTimeout(function(){ document.getElementById("voice-banner").style.transform = "scale(1)"; }, 200);
}
window.addEventListener("load", function() {
  setTimeout(speakWelcome, 800);
});
</script>
""", height=80)

# ── CSS Styling ──────────────────────────────────────────────────────────────
st.markdown("""
<style>
  @keyframes fadeInDown {
    from { opacity: 0; transform: translateY(-18px); }
    to   { opacity: 1; transform: translateY(0); }
  }
  @keyframes pulse {
    0%,100% { box-shadow: 0 0 0 0 rgba(200,16,46,0.30); }
    50%      { box-shadow: 0 0 0 8px rgba(200,16,46,0); }
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
  .stButton > button:hover {
    transform: translateY(-2px) !important;
    opacity: 0.93 !important;
  }
  .intro-box {
    background: #fff5f5;
    border-left: 5px solid #C8102E;
    padding: 1em 1.5em;
    border-radius: 0 8px 8px 0;
    margin-bottom: 1em;
    font-size: 1.02em;
    animation: fadeInDown 0.9s ease both;
  }
  h2 {
    color: #C8102E !important;
    border-bottom: 2px solid #f0f0f0;
    padding-bottom: 6px;
  }
  .success-card {
    background: linear-gradient(135deg, #f0fff4 0%, #e8f8ee 100%);
    border: 1.5px solid #27ae60;
    border-radius: 12px;
    padding: 1.5em;
    margin-top: 1em;
    animation: fadeInDown 0.6s ease both;
  }
  .tip-box {
    background: linear-gradient(135deg, #fffbf0 0%, #fff8e1 100%);
    border-left: 4px solid #f39c12;
    border-radius: 0 8px 8px 0;
    padding: 0.9em 1.2em;
    margin: 0.5em 0 1.2em 0;
    font-size: 0.97em;
  }
</style>
""", unsafe_allow_html=True)

# ── BNI Referral Tip of the Day ───────────────────────────────────────────────
BNI_TIPS = [
    "💡 **BNI Tip:** The most successful BNI members give referrals before expecting to receive them.",
    "💡 **BNI Tip:** Your 60-second pitch should be crystal-clear — the easier you make it to refer you, the more referrals you'll receive!",
    "💡 **BNI Tip:** BNI members generate an average of $50,000+ in new business per year through referrals.",
    "💡 **BNI Tip:** Givers Gain® — members who give the most referrals consistently receive the most in return.",
    "💡 **BNI Tip:** Each member holds one seat per profession — securing your seat locks out competitors!",
    "💡 **BNI Tip:** 1-2-1 meetings with fellow members are the #1 driver of strong referral relationships.",
    "💡 **BNI Tip:** The average BNI chapter passes over $1 million in referrals each year.",
]
random_tip = random.choice(BNI_TIPS)

# ── Hero Header ──────────────────────────────────────────────────────────────
st.markdown("""
<div class='hero-wrap' style='text-align:center; padding: 10px 0 4px 0;'>
  <div style='display:inline-block; background:linear-gradient(135deg,#C8102E 0%,#8b0000 100%);
       color:white; font-size:2.4em; font-weight:900; padding:6px 24px;
       border-radius:10px; letter-spacing:4px; font-family:Arial,sans-serif;
       box-shadow:0 4px 16px rgba(200,16,46,0.35);'>BNI</div>
  <h1 style='color:#C8102E; margin:12px 0 2px 0; font-size:1.9em;'>Welcome to Our BNI Chapter!</h1>
  <p style='color:#888; margin:0; font-size:1em;'>Business Network International — Where Referrals Are Our Business</p>
</div>
""", unsafe_allow_html=True)

st.markdown(f"""
<div class='intro-box'>
  <strong>Thanks for visiting today!</strong> Take 2 minutes to fill out this quick form
  and our members will follow up to help grow your business. We cannot wait to connect!
</div>
<div class='tip-box'>{random_tip}</div>
""", unsafe_allow_html=True)

# ── Email helpers ─────────────────────────────────────────────────────────────
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


def send_hot_lead_alert(first_name, last_name, visitor_email, phone,
                        business_name, industry, elevator_pitch,
                        interest_level, gmail_user, gmail_pass, report_email):
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


# ── Visitor Form ─────────────────────────────────────────────────────────────
with st.form("visitor_form", clear_on_submit=True):

    st.markdown("## Contact Information")
    col1, col2 = st.columns(2)
    with col1:
        first_name = st.text_input("First Name *", placeholder="Jane")
        email      = st.text_input("Email Address *", placeholder="jane@example.com")
        phone      = st.text_input("Phone Number", placeholder="(555) 555-5555")
    with col2:
        last_name = st.text_input("Last Name *", placeholder="Smith")
        city      = st.text_input("City / Area", placeholder="Atlanta, GA")
        website   = st.text_input("Website", placeholder="www.yoursite.com")

    st.markdown("## Social Media")
    col3, col4 = st.columns(2)
    with col3:
        linkedin  = st.text_input("LinkedIn",    placeholder="linkedin.com/in/yourname")
        instagram = st.text_input("Instagram",   placeholder="@yourhandle")
    with col4:
        facebook  = st.text_input("Facebook",    placeholder="facebook.com/yourpage")
        twitter_x = st.text_input("X / Twitter", placeholder="@yourhandle")

    st.markdown("## Your Business")
    business_name = st.text_input("Business Name *", placeholder="Smith Consulting LLC")
    industry = st.selectbox("Industry / Profession *", [
        "Select one...",
        "Accounting / Finance", "Attorney / Legal", "Banking / Lending",
        "Chiropractor / Health", "Construction / Contracting",
        "Consulting / Coaching", "Digital Marketing", "Financial Planning",
        "Health & Wellness", "Home Services / Remodeling", "HR / Staffing",
        "Insurance", "IT / Technology / Cybersecurity",
        "Mortgage / Real Estate", "Photography / Videography",
        "Printing / Signage / Design", "Restaurant / Catering / Food",
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
        "Social media", "Google search", "Friend / colleague",
        "Attended before", "Other"
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
        options=["Just exploring","Somewhat interested","Very interested","Ready to apply!"]
    )
    notes = st.text_area("Anything else you would like us to know? (optional)", height=70)

    submitted = st.form_submit_button("\U0001f91d  Submit — We Will Be In Touch!")

# ── Submission Logic ──────────────────────────────────────────────────────────
if submitted:
    errors = []
    if not first_name.strip():      errors.append("First Name")
    if not last_name.strip():       errors.append("Last Name")
    if not email.strip():           errors.append("Email Address")
    if not business_name.strip():   errors.append("Business Name")
    if industry == "Select one...": errors.append("Industry / Profession")
    if industry == "Other" and not other_industry.strip(): errors.append("Profession (Other)")
    if not elevator_pitch.strip():  errors.append("One-sentence business description")

    if errors:
        st.error("Please complete these required fields: " + ", ".join(errors))
    else:
        final_industry = other_industry.strip() if industry == "Other" else industry
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        row = [
            timestamp, first_name.strip(), last_name.strip(), email.strip(),
            phone.strip(), city.strip(), website.strip(),
            linkedin.strip(), instagram.strip(), facebook.strip(), twitter_x.strip(),
            business_name.strip(), final_industry, elevator_pitch.strip(),
            years_in_biz, ideal_referral.strip(), top_clients.strip(),
            how_heard, invited_by.strip(), ", ".join(looking_for),
            has_bni_before, biggest_challenge.strip(), ready_to_join, notes.strip()
        ]

        # Save to Google Sheet
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
            sheet  = client.open(st.secrets["SHEET_NAME"]).sheet1
            sheet.append_row(row)
        except Exception as e:
            st.warning(f"Note: Could not save to sheet — {e}")

        # Send emails
        try:
            gmail_user   = st.secrets["GMAIL_USER"]
            gmail_pass   = st.secrets["GMAIL_APP_PASSWORD"]
            report_email = st.secrets["REPORT_EMAIL"]
            send_visitor_welcome(
                first_name.strip(), email.strip(),
                business_name.strip(), ready_to_join,
                gmail_user, gmail_pass
            )
            if ready_to_join in ["Ready to apply!", "Very interested"]:
                send_hot_lead_alert(
                    first_name.strip(), last_name.strip(), email.strip(),
                    phone.strip(), business_name.strip(), final_industry,
                    elevator_pitch.strip(), ready_to_join,
                    gmail_user, gmail_pass, report_email
                )
        except KeyError:
            pass  # Email secrets not configured
        except Exception:
            pass

        # ── Confetti + Voice Celebration ──────────────────────────────────────
        st.components.v1.html("""
<canvas id="confetti-canvas" style="position:fixed;top:0;left:0;width:100vw;height:100vh;pointer-events:none;z-index:9999;"></canvas>
<script>
(function(){
  var canvas = document.getElementById("confetti-canvas");
  var ctx = canvas.getContext("2d");
  canvas.width = window.innerWidth;
  canvas.height = window.innerHeight;
  var colors = ["#C8102E","#FFD700","#27ae60","#3498db","#f39c12","#9b59b6","#ffffff","#e74c3c"];
  var pieces = [];
  for(var i=0;i<180;i++){
    pieces.push({
      x: Math.random()*canvas.width, y: Math.random()*canvas.height-canvas.height,
      w: Math.random()*10+6, h: Math.random()*5+4,
      color: colors[Math.floor(Math.random()*colors.length)],
      rot: Math.random()*360, vx: Math.random()*2-1,
      vy: Math.random()*4+2, vr: Math.random()*6-3
    });
  }
  var frame=0;
  function draw(){
    ctx.clearRect(0,0,canvas.width,canvas.height);
    pieces.forEach(function(p){
      ctx.save(); ctx.translate(p.x,p.y); ctx.rotate(p.rot*Math.PI/180);
      ctx.fillStyle=p.color; ctx.globalAlpha=0.87;
      ctx.fillRect(-p.w/2,-p.h/2,p.w,p.h); ctx.restore();
      p.x+=p.vx; p.y+=p.vy; p.rot+=p.vr;
      if(p.y>canvas.height){ p.y=-10; p.x=Math.random()*canvas.width; }
    });
    frame++;
    if(frame<220) requestAnimationFrame(draw);
    else ctx.clearRect(0,0,canvas.width,canvas.height);
  }
  draw();
  if(window.speechSynthesis){
    window.speechSynthesis.cancel();
    var msg=new SpeechSynthesisUtterance("Thank you for registering! A B N I member will reach out to you very soon. We are so excited to connect with you!");
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
  <p style='margin-top:14px; color:#555;'>A chapter member will reach out soon. Check your email for your welcome message!</p>
  <div style='background:#fff; border:1px solid #c3e6cb; border-radius:8px; padding:10px 14px; margin-top:12px; font-size:0.9em; color:#27ae60;'>
    <strong>What happens next?</strong><br>
    &#10003; A BNI member contacts you within 24 hours.<br>
    &#10003; You will be invited to a 1-2-1 coffee meeting.<br>
    &#10003; You can apply for membership and lock in your profession!
  </div>
</div>
""", unsafe_allow_html=True)
