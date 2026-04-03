import streamlit as st
import gspread
from google.oauth2.service_account import Credentials
from datetime import datetime
import json
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import random
try:
    from apscheduler.schedulers.background import BackgroundScheduler
    from apscheduler.triggers.cron import CronTrigger
    SCHEDULER_AVAILABLE = True
except ImportError:
    SCHEDULER_AVAILABLE = False

st.set_page_config(page_title="BNI Leaders FTL", page_icon="U0001f91d", layout="centered")

if "page" not in st.session_state:
    st.session_state["page"] = "landing"
if "scheduler_started" not in st.session_state:
    st.session_state["scheduler_started"] = False

# ── Email helper ────────────────────────────────────────────────────────────
ALL_RECIPIENTS = ["ausjones84@gmail.com", "Joel.Bruno@plrcpas.com", "elena@amb-legal.com"]

def get_recipients():
    recipients = list(ALL_RECIPIENTS)
    try:
        extra = st.secrets.get("REPORT_EMAIL","")
        if extra:
            for r in extra.split(","):
                r = r.strip()
                if r and r not in recipients:
                    recipients.append(r)
    except Exception:
        pass
    return recipients

def get_gmail_creds():
    try:
        return st.secrets["GMAIL_USER"], st.secrets["GMAIL_APP_PASSWORD"]
    except Exception:
        return None, None

# ── Thursday 8:30 AM scheduled report ──────────────────────────────────────
def send_weekly_report_email():
    gu, gp = get_gmail_creds()
    if not gu or not gp:
        return
    recipients = get_recipients()
    date_str = datetime.now().strftime("%B %d, %Y")
    html_body = f"""
    <div style="font-family:Arial,sans-serif;max-width:650px;margin:auto;background:#fff;">
    <div style="background:linear-gradient(135deg,#C8102E,#8b0000);color:white;padding:24px 32px;border-radius:14px 14px 0 0;">
      <div style="font-size:1.6em;font-weight:900;letter-spacing:3px;">BNI Leaders FTL</div>
      <h2 style="margin:6px 0 0;color:white!important;">&#128197; Weekly Thursday Report</h2>
      <p style="margin:4px 0 0;opacity:.85;">Automatically generated for {date_str}</p>
    </div>
    <div style="background:#f8f9fa;padding:24px 32px;border-radius:0 0 14px 14px;">
      <p>Good morning BNI Leaders FTL team!</p>
      <p>This is your automated Thursday morning summary. Please open the <a href="https://bni-visitor-intake.streamlit.app" style="color:#C8102E;font-weight:700;">BNI Leaders FTL Chapter Hub</a> to record today&#8217;s meeting contributions.</p>
      <div style="background:#fff;border:2px solid #C8102E;border-radius:10px;padding:16px 20px;margin:16px 0;">
        <p style="margin:0;font-weight:700;color:#C8102E;">&#127942; Today&#8217;s Meeting Checklist</p>
        <ul style="color:#555;margin:8px 0 0;">
          <li>Open Meeting Recorder at the end of the Zoom call</li>
          <li>Press <strong>Start Recording</strong> and let members announce their activity</li>
          <li>System auto-tallies TYFCB, Referrals, and Testimonials</li>
          <li>Press <strong>End &amp; Send Report</strong> when done</li>
        </ul>
      </div>
      <p style="font-size:.85em;color:#888;">Questions? Contact Austin Jones &mdash; <a href="https://mrceesai.com" style="color:#C8102E;">mrceesai.com</a></p>
    </div></div>"""
    try:
        msg = MIMEMultipart("alternative")
        msg["Subject"] = f"\U0001f4cb BNI Leaders FTL \u2014 Thursday Meeting Reminder &amp; Report \u2014 {date_str}"
        msg["From"] = gu; msg["To"] = ", ".join(recipients)
        msg.attach(MIMEText(html_body, "html"))
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as srv:
            srv.login(gu, gp); srv.sendmail(gu, recipients, msg.as_string())
    except Exception:
        pass

if SCHEDULER_AVAILABLE and not st.session_state["scheduler_started"]:
    try:
        scheduler = BackgroundScheduler()
        scheduler.add_job(send_weekly_report_email, CronTrigger(day_of_week="thu", hour=8, minute=30))
        scheduler.start()
        st.session_state["scheduler_started"] = True
    except Exception:
        pass

# ── Global styles ───────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700;800;900&display=swap');
*{font-family:'Inter',Arial,sans-serif;}
@keyframes fadeInDown{from{opacity:0;transform:translateY(-18px);}to{opacity:1;transform:translateY(0);}}
@keyframes fadeInUp{from{opacity:0;transform:translateY(18px);}to{opacity:1;transform:translateY(0);}}
@keyframes float{0%,100%{transform:translateY(0);}50%{transform:translateY(-6px);}}
[data-testid="stAppViewContainer"]{background:linear-gradient(160deg,#0a0014 0%,#1a0a0a 40%,#0d0d1a 100%)!important;min-height:100vh;}
[data-testid="stHeader"]{background:transparent!important;}
.block-container{padding-top:1rem!important;}
.stButton>button{background:linear-gradient(135deg,#C8102E,#a00d24)!important;color:white!important;font-weight:700!important;border-radius:10px!important;padding:.75em 2em!important;font-size:1em!important;width:100%!important;border:none!important;margin-top:10px!important;transition:all .2s!important;box-shadow:0 4px 16px rgba(200,16,46,.35)!important;}
.stButton>button:hover{transform:translateY(-3px)!important;box-shadow:0 8px 24px rgba(200,16,46,.5)!important;}
h1,h2,h3{color:#C8102E!important;}
h2{border-bottom:2px solid rgba(200,16,46,.2)!important;padding-bottom:6px!important;}
.stTextInput>div>div>input,.stTextArea>div>div>textarea,.stSelectbox>div>div{background:#1a1a2e!important;color:#e8edf3!important;border:1.5px solid #2d2d4e!important;border-radius:8px!important;}
.stSelectbox>div>div>div{color:#e8edf3!important;}
label{color:#c8d0e0!important;}
.footer-bar{text-align:center;margin-top:2.5em;padding:1.2em;background:rgba(255,255,255,.04);border-radius:12px;font-size:.83em;color:#666;border:1px solid rgba(255,255,255,.06);}
.footer-bar a{color:#C8102E!important;}
</style>
""", unsafe_allow_html=True)

st.markdown("""
<div style='text-align:center;padding:14px 0 6px;animation:fadeInDown .6s ease both;'>
  <div style='display:inline-block;background:linear-gradient(135deg,#C8102E,#8b0000);color:white;font-size:1.55em;font-weight:900;padding:9px 32px;border-radius:12px;letter-spacing:3px;box-shadow:0 6px 24px rgba(200,16,46,.5);'>BNI Leaders FTL</div>
  <div style='color:#C8102E;margin:10px 0 2px;font-size:1.2em;font-weight:700;letter-spacing:2px;text-transform:uppercase;'>Chapter Hub</div>
  <p style='color:#888;margin:0;font-size:.88em;'>Business Network International &mdash; Fort Lauderdale</p>
</div>
""", unsafe_allow_html=True)

if st.session_state["page"] == "landing":
    st.markdown("""
    <style>
    .land-grid{display:grid;grid-template-columns:1fr 1fr;gap:20px;margin:20px 0 10px;}
    .land-card{border-radius:18px;padding:2.2em 1.6em;text-align:center;position:relative;overflow:hidden;background:rgba(255,255,255,.03);backdrop-filter:blur(10px);border:1.5px solid rgba(255,255,255,.08);transition:all .3s;animation:fadeInUp .8s ease both;}
    .land-card::before{content:'';position:absolute;top:0;left:0;right:0;height:4px;border-radius:18px 18px 0 0;}
    .land-card.vc::before{background:linear-gradient(90deg,#C8102E,#ff6b6b);}
    .land-card.mc::before{background:linear-gradient(90deg,#1a56db,#60a5fa);}
    .land-card:hover{transform:translateY(-6px);box-shadow:0 20px 50px rgba(0,0,0,.5);border-color:rgba(255,255,255,.15);}
    .land-icon{font-size:3.5em;margin-bottom:.4em;animation:float 3s ease infinite;}
    .land-title{font-size:1.3em;font-weight:800;margin-bottom:.5em;}
    .land-card.vc .land-title{color:#ff6b6b!important;}
    .land-card.mc .land-title{color:#60a5fa!important;}
    .land-desc{color:#9ca3af;font-size:.88em;line-height:1.6;margin-bottom:1.2em;}
    .land-cta{border-radius:10px;padding:10px 0;font-weight:700;font-size:.9em;color:white;}
    .land-card.vc .land-cta{background:linear-gradient(135deg,#C8102E,#8b0000);}
    .land-card.mc .land-cta{background:linear-gradient(135deg,#1a56db,#1e3a8a);}
    .stat-bar{display:flex;gap:12px;margin:0 0 20px;justify-content:center;flex-wrap:wrap;}
    .stat-chip{background:rgba(255,255,255,.05);border:1px solid rgba(255,255,255,.1);border-radius:20px;padding:6px 16px;font-size:.8em;color:#9ca3af;}
    .stat-chip span{color:#C8102E;font-weight:700;}
    </style>
    <div class='stat-bar'>
      <div class='stat-chip'>&#128205; Fort Lauderdale, FL</div>
      <div class='stat-chip'>&#128197; Thursdays 7:00 AM</div>
      <div class='stat-chip'>&#129309; <span>Givers Gain</span></div>
    </div>
    <div class='land-grid'>
      <div class='land-card vc'>
        <div class='land-icon'>&#128075;</div>
        <div class='land-title'>Visitor Sign-In</div>
        <p class='land-desc'>First time at BNI? Sign in as our guest and connect with 30+ local business leaders!</p>
        <div class='land-cta'>&#128204;&nbsp; Guest Sign-In Form</div>
      </div>
      <div class='land-card mc'>
        <div class='land-icon'>&#127908;</div>
        <div class='land-title'>Meeting Recorder</div>
        <p class='land-desc'>Members: Hit record at end of Zoom, speak naturally &mdash; AI auto-tallies TYFCB, referrals &amp; testimonials!</p>
        <div class='land-cta'>&#127908;&nbsp; Open Live Recorder</div>
      </div>
    </div>
    <div style='margin:20px 0;background:rgba(200,16,46,.06);border:1px solid rgba(200,16,46,.2);border-radius:14px;padding:18px 22px;'>
      <div style='color:#ff6b6b;font-weight:700;font-size:.9em;margin-bottom:10px;'>&#127942; BNI Leaders FTL &mdash; What We Do</div>
      <div style='display:grid;grid-template-columns:1fr 1fr;gap:8px;font-size:.84em;color:#9ca3af;'>
        <div>&#10003; Pass qualified referrals weekly</div><div>&#10003; Track TYFCB &amp; testimonials</div>
        <div>&#10003; One member per profession</div><div>&#10003; 30+ active business leaders</div>
        <div>&#10003; Real-time meeting scoreboard</div><div>&#10003; Auto Thursday 8:30 AM reports</div>
      </div>
    </div>
    """, unsafe_allow_html=True)
    col_v, col_m = st.columns(2, gap="medium")
    with col_v:
        if st.button("Enter as Visitor", key="btn_v"):
            st.session_state["page"] = "visitor"
            st.rerun()
    with col_m:
        if st.button("Open Meeting Recorder", key="btn_m"):
            st.session_state["page"] = "recorder"
            st.rerun()
    st.markdown("""<div class='footer-bar'>&#128274; Data stored securely &nbsp;|&nbsp; Powered by <a href='https://mrceesai.com'>MrCeesAI</a> &mdash; Austin Jones</div>""", unsafe_allow_html=True)

elif st.session_state["page"] == "visitor":
    if st.button("\u2190 Back to Home", key="back_v"):
        st.session_state["page"] = "landing"
        st.rerun()

    def send_visitor_emails(fn, ln, ve, ph, bn, ind, ep, il, gu, gp):
        recipients = get_recipients()
        try:
            # Welcome to visitor
            msg = MIMEMultipart("alternative")
            msg["Subject"] = f"Great connecting with you at BNI, {fn}!"
            msg["From"] = gu; msg["To"] = ve
            html = f"""<div style="font-family:Arial,sans-serif;max-width:600px;margin:auto;">
<div style="background:linear-gradient(135deg,#C8102E,#8b0000);color:white;padding:20px 24px;border-radius:10px 10px 0 0;">
<div style="font-size:1.8em;font-weight:900;letter-spacing:3px;">BNI Leaders FTL</div>
<h2 style="margin:8px 0 0;color:white!important;">Thanks for Visiting, {fn}!</h2></div>
<div style="background:#f9f9f9;padding:24px;border-radius:0 0 10px 10px;">
<p>Hi {fn}, thank you for joining us at BNI Leaders FTL! A chapter member will reach out shortly.</p>
<p><strong>Business:</strong> {bn} ({ind}) &mdash; <strong>Interest:</strong> {il}</p>
<p>We hope to see you again next Thursday at 7:00 AM!</p>
<p style="font-size:.85em;color:#888;">Need AI automation? <a href="https://mrceesai.com" style="color:#C8102E;">MrCeesAI by Austin Jones</a></p>
</div></div>"""
            msg.attach(MIMEText(html, "html"))
            with smtplib.SMTP_SSL("smtp.gmail.com", 465) as s:
                s.login(gu, gp); s.sendmail(gu, ve, msg.as_string())
        except Exception:
            pass
        # Notify all recipients (chapter team)
        if il in ["Ready to apply!", "Very interested"]:
            try:
                msg2 = MIMEMultipart("alternative")
                msg2["Subject"] = f"\U0001f525 BNI HOT LEAD \u2014 {fn} {ln} ({bn})"
                msg2["From"] = gu; msg2["To"] = ", ".join(recipients)
                html2 = f"""<div style="font-family:Arial,sans-serif;max-width:600px;margin:auto;">
<div style="background:#27ae60;color:white;padding:16px 24px;border-radius:10px 10px 0 0;">
<h2 style="margin:0;color:white!important;">&#128293; HOT BNI LEAD &mdash; {il}</h2></div>
<div style="background:#f0fff4;padding:24px;border-radius:0 0 10px 10px;border:2px solid #27ae60;">
<p><strong>{fn} {ln}</strong> &mdash; {bn} ({ind})</p>
<p>Email: <a href="mailto:{ve}">{ve}</a> | Phone: {ph or "N/A"}</p>
<p><em>"{ep}"</em></p>
<p style="color:#27ae60;font-weight:700;">Reach out NOW &mdash; they are ready to join!</p></div></div>"""
                msg2.attach(MIMEText(html2, "html"))
                with smtplib.SMTP_SSL("smtp.gmail.com", 465) as s:
                    s.login(gu, gp); s.sendmail(gu, recipients, msg2.as_string())
            except Exception:
                pass

    BNI_TIPS = [
        "&#128161; <strong>BNI Tip:</strong> The most successful members give referrals before expecting to receive.",
        "&#128161; <strong>BNI Tip:</strong> Your 60-second pitch should be crystal-clear &mdash; easier to refer you!",
        "&#128161; <strong>BNI Tip:</strong> BNI members generate an average of $50,000+ in new business per year.",
        "&#128161; <strong>BNI Tip:</strong> Givers Gain&#174; &mdash; members who give most referrals receive the most.",
        "&#128161; <strong>BNI Tip:</strong> 1-2-1 meetings are the #1 driver of strong referral relationships.",
        "&#128161; <strong>BNI Tip:</strong> The average BNI chapter passes over $1 million in referrals each year.",
    ]

    st.markdown(f"""<div style='background:rgba(200,16,46,.08);border-left:5px solid #C8102E;padding:1em 1.5em;border-radius:0 8px 8px 0;margin-bottom:1em;color:#e8edf3;'><strong style='color:#ff6b6b;'>Thanks for visiting today!</strong> Fill out this form and our members will follow up with you!</div>
<div style='background:rgba(243,156,18,.08);border-left:4px solid #f39c12;border-radius:0 8px 8px 0;padding:.9em 1.2em;margin:.5em 0 1.2em;font-size:.97em;color:#d4b800;'>{random.choice(BNI_TIPS)}</div>""", unsafe_allow_html=True)

    with st.form("visitor_form", clear_on_submit=True):
        st.markdown("## Contact Information")
        c1, c2 = st.columns(2)
        with c1:
            first_name = st.text_input("First Name *", placeholder="Jane")
            email = st.text_input("Email Address *", placeholder="jane@example.com")
            phone = st.text_input("Phone Number", placeholder="(555) 555-5555")
        with c2:
            last_name = st.text_input("Last Name *", placeholder="Smith")
            city = st.text_input("City / Area", placeholder="Fort Lauderdale, FL")
            website = st.text_input("Website", placeholder="www.yoursite.com")
        st.markdown("## Social Media")
        c3, c4 = st.columns(2)
        with c3:
            linkedin = st.text_input("LinkedIn", placeholder="linkedin.com/in/yourname")
            instagram = st.text_input("Instagram", placeholder="@yourhandle")
        with c4:
            facebook = st.text_input("Facebook", placeholder="facebook.com/yourpage")
            twitter_x = st.text_input("X / Twitter", placeholder="@yourhandle")
        st.markdown("## Your Business")
        business_name = st.text_input("Business Name *", placeholder="Smith Consulting LLC")
        industry = st.selectbox("Industry / Profession *", [
            "Select one...","Accounting / Finance","Attorney / Legal","Banking / Lending",
            "Chiropractor / Health","Construction / Contracting","Consulting / Coaching",
            "Digital Marketing","Financial Planning","Health & Wellness","Home Services / Remodeling",
            "Insurance","IT / Technology / Cybersecurity","Mortgage / Real Estate",
            "Photography / Videography","Real Estate Services","Travel / Hospitality","Other"])
        other_industry = ""
        if industry == "Other":
            other_industry = st.text_input("Please describe your profession *")
        elevator_pitch = st.text_area("In one sentence: what do you do and who do you help? *", placeholder="I help small business owners protect assets with affordable insurance plans.", height=80)
        years_in_biz = st.select_slider("How long have you been in business?", options=["Less than 1 year","1-2 years","3-5 years","6-10 years","10+ years"])
        st.markdown("## Networking & Referrals")
        c5, c6 = st.columns(2)
        with c5:
            ideal_referral = st.text_area("What does your ideal referral look like?", placeholder="A homeowner aged 35-55 who recently bought a house...", height=90)
        with c6:
            top_clients = st.text_area("Top 3 types of clients you serve?", placeholder="Real estate agents, small business owners, HR managers...", height=90)
        how_heard = st.selectbox("How did you hear about our chapter?", ["Select one...","Invited by a member","BNI website / Find a Chapter","Social media","Google search","Friend / colleague","Attended before","Other"])
        invited_by = st.text_input("If invited by a member — who invited you?", placeholder="Member name")
        st.markdown("## Goals & Interest Level")
        looking_for = st.multiselect("What are you hoping to get from BNI?", ["More qualified referrals","Grow my professional network","Business accountability","Learn from other business owners","Give referrals to others","Greater brand visibility","Find trusted vendors & partners","Structured networking system"])
        has_bni_before = st.radio("Have you visited or been a BNI member before?", ["No — first time!","Visited before but never joined","Former BNI member"], horizontal=True)
        biggest_challenge = st.text_area("What is your biggest business challenge right now?", placeholder="Generating consistent leads...", height=80)
        ready_to_join = st.select_slider("How interested are you in joining our chapter?", options=["Just exploring","Somewhat interested","Very interested","Ready to apply!"])
        notes = st.text_area("Anything else you would like us to know? (optional)", height=70)
        v_submitted = st.form_submit_button("\U0001f91d Submit — We Will Be In Touch!")

    if v_submitted:
        errs = []
        if not first_name.strip(): errs.append("First Name")
        if not last_name.strip(): errs.append("Last Name")
        if not email.strip(): errs.append("Email Address")
        if not business_name.strip(): errs.append("Business Name")
        if industry == "Select one...": errs.append("Industry / Profession")
        if industry == "Other" and not other_industry.strip(): errs.append("Profession (Other)")
        if not elevator_pitch.strip(): errs.append("One-sentence business description")
        if errs:
            st.error("Please complete: " + ", ".join(errs))
        else:
            fin_industry = other_industry.strip() if industry == "Other" else industry
            ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            row = [ts, first_name.strip(), last_name.strip(), email.strip(), phone.strip(), city.strip(), website.strip(), linkedin.strip(), instagram.strip(), facebook.strip(), twitter_x.strip(), business_name.strip(), fin_industry, elevator_pitch.strip(), years_in_biz, ideal_referral.strip(), top_clients.strip(), how_heard, invited_by.strip(), ", ".join(looking_for), has_bni_before, biggest_challenge.strip(), ready_to_join, notes.strip()]
            try:
                creds_dict = json.loads(st.secrets["GOOGLE_CREDS"])
                creds = Credentials.from_service_account_info(creds_dict, scopes=["https://spreadsheets.google.com/feeds","https://www.googleapis.com/auth/drive"])
                client = gspread.authorize(creds)
                client.open(st.secrets["SHEET_NAME"]).sheet1.append_row(row)
            except Exception as e:
                st.warning(f"Could not save to sheet: {e}")
            try:
                gu, gp = get_gmail_creds()
                if gu and gp:
                    send_visitor_emails(first_name.strip(), last_name.strip(), email.strip(), phone.strip(), business_name.strip(), fin_industry, elevator_pitch.strip(), ready_to_join, gu, gp)
            except Exception:
                pass
            st.components.v1.html("""<canvas id="cc" style="position:fixed;top:0;left:0;width:100vw;height:100vh;pointer-events:none;z-index:9999;"></canvas><script>(function(){var c=document.getElementById("cc"),ctx=c.getContext("2d");c.width=window.innerWidth;c.height=window.innerHeight;var cols=["#C8102E","#FFD700","#27ae60","#3498db","#f39c12","#fff","#e74c3c"];var pp=[];for(var i=0;i<160;i++)pp.push({x:Math.random()*c.width,y:Math.random()*c.height-c.height,w:Math.random()*10+5,h:Math.random()*5+3,col:cols[Math.floor(Math.random()*cols.length)],rot:Math.random()*360,vx:Math.random()*2-1,vy:Math.random()*4+2,vr:Math.random()*6-3});var f=0;function draw(){ctx.clearRect(0,0,c.width,c.height);pp.forEach(function(p){ctx.save();ctx.translate(p.x,p.y);ctx.rotate(p.rot*Math.PI/180);ctx.fillStyle=p.col;ctx.globalAlpha=.85;ctx.fillRect(-p.w/2,-p.h/2,p.w,p.h);ctx.restore();p.x+=p.vx;p.y+=p.vy;p.rot+=p.vr;if(p.y>c.height){p.y=-10;p.x=Math.random()*c.width;}});f++;if(f<200)requestAnimationFrame(draw);else ctx.clearRect(0,0,c.width,c.height);}draw();})();</script>""", height=0)
            st.balloons()
            st.markdown(f"""<div style='background:rgba(39,174,96,.08);border:1.5px solid #27ae60;border-radius:12px;padding:1.5em;margin-top:1em;'><h3 style='color:#27ae60;margin-top:0;'>&#127881; Thanks, {first_name}! You are all set.</h3><p style='color:#c8d0e0;'>A follow-up email was sent to <strong>{email}</strong>. Our chapter members have been notified of your visit.</p><div style='background:rgba(39,174,96,.08);border:1px solid rgba(39,174,96,.3);border-radius:8px;padding:10px 14px;margin-top:12px;font-size:.9em;color:#4ade80;'><strong>What happens next?</strong><br>&#10003; A BNI member contacts you within 24 hours.<br>&#10003; You will be invited to a 1-2-1 coffee meeting.<br>&#10003; You can apply for membership and lock in your profession!</div></div>""", unsafe_allow_html=True)

elif st.session_state["page"] == "recorder":
    if st.button("\u2190 Back to Home", key="back_r"):
        st.session_state["page"] = "landing"
        st.rerun()

    today_str = datetime.now().strftime("%B %d, %Y")
    day_of_week = datetime.now().strftime("%A")

    BNI_MEMBERS = [
        "Alex Laraia","Cassandra Exantus","Cecil Pardave","Chris Rios",
        "Connie Kaplan","Dan Hahn","Devaney Mangroo","Edgar Villarreal",
        "Elena Blose","Elizabeth Hornsby","Freddy Santory","JC Aleman",
        "Jessica Goulart","Joel Bruno","Kamili Kelly","Kristie Estevez-Puente",
        "Kristin Marrero","Lauren Klein","Lisa Jones","Marisol Cruz",
        "Mauricio Cavanzo","Michael Elias","Michael Gigante","Michelle Notte",
        "Nathan McCune","Nishant Thaker","Omar Abdel","Richard Saulsberry",
        "Roberta Schwartz","Sebastian Gonzalez","Stephanie Taylor",
        "Tatiana Smidi","Tegdra Samuel","Austin Jones"
    ]

    def send_meeting_report(date_str, tally_data, transcript, duration):
        gu, gp = get_gmail_creds()
        if not gu or not gp:
            return False, "Email credentials not configured"
        recipients = get_recipients()
        tally = tally_data if tally_data else []
        total_t = sum(m.get("tyfcb",0) for m in tally)
        total_r = sum(m.get("referral",0) for m in tally)
        total_s = sum(m.get("testimonial",0) for m in tally)
        grand_total = total_t + total_r + total_s
        tally_sorted = sorted(tally, key=lambda x: x.get("tyfcb",0)+x.get("referral",0)+x.get("testimonial",0), reverse=True)
        rows = ""
        for i,m in enumerate(tally_sorted):
            tot = m.get("tyfcb",0)+m.get("referral",0)+m.get("testimonial",0)
            if tot == 0: continue
            bg = "#f9f9f9" if i%2 else "#fff"
            medal = "\U0001f947" if i==0 else ("\U0001f948" if i==1 else ("\U0001f949" if i==2 else "  "))
            rows += f"""<tr style='background:{bg};'><td style='padding:10px 14px;font-weight:700;font-size:.95em;'>{medal} {m.get("name","")}</td><td style='padding:10px 14px;text-align:center;'><span style='background:#27ae60;color:white;border-radius:20px;padding:3px 12px;font-weight:800;'>{m.get("tyfcb",0)}</span></td><td style='padding:10px 14px;text-align:center;'><span style='background:#C8102E;color:white;border-radius:20px;padding:3px 12px;font-weight:800;'>{m.get("referral",0)}</span></td><td style='padding:10px 14px;text-align:center;'><span style='background:#8e44ad;color:white;border-radius:20px;padding:3px 12px;font-weight:800;'>{m.get("testimonial",0)}</span></td><td style='padding:10px 14px;text-align:center;font-weight:900;font-size:1.1em;color:#1a56db;'>{tot}</td></tr>"""
        top3 = [m for m in tally_sorted if m.get("tyfcb",0)+m.get("referral",0)+m.get("testimonial",0)>0][:3]
        podium_html = ""
        pcols = ["#f39c12","#95a5a6","#cd7f32"]
        plbls = ["\U0001f947 1st Place","\U0001f948 2nd Place","\U0001f949 3rd Place"]
        for idx,m in enumerate(top3):
            podium_html += f"""<td style='text-align:center;padding:8px 12px;vertical-align:bottom;'><div style='background:{pcols[idx]};color:white;border-radius:12px 12px 0 0;padding:18px 14px 10px;font-weight:900;min-width:130px;'>{plbls[idx]}<br><span style='font-size:1.3em;'>{m.get("name","").split()[0]}</span><br><span style='font-size:.8em;opacity:.85;'>{m.get("name","").split()[-1] if len(m.get("name","").split())>1 else ""}</span></div><div style='background:#f5f5f5;padding:8px;font-size:.82em;color:#555;border-radius:0 0 8px 8px;border:1px solid #ddd;'>T:{m.get("tyfcb",0)} &nbsp; R:{m.get("referral",0)} &nbsp; S:{m.get("testimonial",0)}</div></td>"""
        html_body = f"""<div style="font-family:Arial,sans-serif;max-width:780px;margin:auto;background:#fff;border-radius:16px;overflow:hidden;box-shadow:0 4px 32px rgba(0,0,0,.1);">
<div style="background:linear-gradient(135deg,#C8102E,#8b0000);color:white;padding:28px 36px;">
<div style="font-size:1.6em;font-weight:900;letter-spacing:3px;margin-bottom:4px;">BNI Leaders FTL</div>
<h2 style="margin:0;color:white!important;font-size:1.6em;">&#127908; Weekly Meeting Report</h2>
<p style="margin:6px 0 0;opacity:.85;font-size:.95em;">&#128197; {date_str} &nbsp;&#183;&nbsp; &#128336; Generated at {datetime.now().strftime("%I:%M %p")} &nbsp;&#183;&nbsp; Duration: {duration}</p>
</div>
<div style="padding:30px 36px;background:#f8f9fa;">
<table style="width:100%;border-collapse:collapse;margin-bottom:28px;">
<tr>
<td style="text-align:center;background:linear-gradient(135deg,#27ae60,#1e8449);color:white;padding:20px;border-radius:12px;width:31%;">
<div style="font-size:3em;font-weight:900;line-height:1;">{total_t}</div>
<div style="font-size:.9em;opacity:.9;margin-top:4px;font-weight:700;">&#127881; Thank You for Closed Business</div></td>
<td style="width:3.5%;"></td>
<td style="text-align:center;background:linear-gradient(135deg,#C8102E,#8b0000);color:white;padding:20px;border-radius:12px;width:31%;">
<div style="font-size:3em;font-weight:900;line-height:1;">{total_r}</div>
<div style="font-size:.9em;opacity:.9;margin-top:4px;font-weight:700;">&#128279; Referrals Passed</div></td>
<td style="width:3.5%;"></td>
<td style="text-align:center;background:linear-gradient(135deg,#8e44ad,#6c3483);color:white;padding:20px;border-radius:12px;width:31%;">
<div style="font-size:3em;font-weight:900;line-height:1;">{total_s}</div>
<div style="font-size:.9em;opacity:.9;margin-top:4px;font-weight:700;">&#11088; Testimonials Given</div></td>
</tr></table>
<div style="text-align:center;background:linear-gradient(135deg,#1a56db,#1e3a8a);color:white;padding:12px;border-radius:10px;margin-bottom:24px;font-size:1.1em;font-weight:700;">
&#127942; Total Chapter Activity This Week: <span style="font-size:1.4em;">{grand_total}</span></div>
{"<h3 style='color:#f39c12;margin:0 0 14px;font-size:1.1em;'>&#127942; Top Contributors</h3><table style='width:100%;border-collapse:collapse;margin-bottom:28px;'><tr style='vertical-align:bottom;'>" + podium_html + "</tr></table>" if top3 else ""}
<h3 style="color:#1a56db;margin:0 0 12px;font-size:1.05em;">&#128203; Full Scorecard</h3>
<table style="width:100%;border-collapse:collapse;margin-bottom:28px;border-radius:12px;overflow:hidden;box-shadow:0 2px 16px rgba(0,0,0,.08);">
<thead><tr style="background:linear-gradient(135deg,#1a56db,#1e3a8a);color:white;">
<th style="padding:12px 14px;text-align:left;font-size:.9em;">Member</th>
<th style="padding:12px 14px;text-align:center;font-size:.9em;">&#127881; TYFCB</th>
<th style="padding:12px 14px;text-align:center;font-size:.9em;">&#128279; Referrals</th>
<th style="padding:12px 14px;text-align:center;font-size:.9em;">&#11088; Testimonials</th>
<th style="padding:12px 14px;text-align:center;font-size:.9em;">Total</th>
</tr></thead>
<tbody>{rows or "<tr><td colspan='5' style='padding:16px;text-align:center;color:#999;font-style:italic;'>No activity recorded this session</td></tr>"}</tbody>
</table>
<h3 style="color:#555;font-size:.95em;margin:0 0 8px;">&#128221; Meeting Transcript</h3>
<div style="background:#0d1117;border-radius:10px;padding:16px;font-family:'Courier New',monospace;font-size:.82em;color:#58a6ff;white-space:pre-wrap;max-height:300px;overflow-y:auto;line-height:1.7;">{transcript or "No transcript captured this session."}</div>
<p style="font-size:.78em;color:#aaa;margin-top:24px;text-align:center;border-top:1px solid #eee;padding-top:16px;">
&#x1F916; Automated report by BNI Leaders FTL Chapter Hub &mdash; <a href="https://bni-visitor-intake.streamlit.app" style="color:#C8102E;">bni-visitor-intake.streamlit.app</a> &mdash; <a href="https://mrceesai.com" style="color:#C8102E;">mrceesai.com</a></p>
</div></div>"""
        try:
            msg = MIMEMultipart("alternative")
            msg["Subject"] = f"\U0001f3c6 BNI Leaders FTL Meeting Report \u2014 {date_str} \u2014 {grand_total} Total Activities"
            msg["From"] = gu; msg["To"] = ", ".join(recipients)
            msg.attach(MIMEText(html_body, "html"))
            with smtplib.SMTP_SSL("smtp.gmail.com",465) as srv:
                srv.login(gu, gp); srv.sendmail(gu, recipients, msg.as_string())
            return True, recipients
        except Exception as e:
            return False, str(e)

    members_js = json.dumps(BNI_MEMBERS)
    recorder_html = f"""<!DOCTYPE html>
<html lang="en"><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>BNI Meeting Recorder</title>
<style>
:root{{--red:#C8102E;--green:#27ae60;--blue:#1a56db;--purple:#8e44ad;--bg:#0a0e1a;--card:#111827;--border:#1f2937;--text:#e8edf3;--muted:#6b7280;}}
*{{box-sizing:border-box;margin:0;padding:0;font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',sans-serif;}}
body{{background:var(--bg);color:var(--text);min-height:100vh;padding:12px;}}
.topbar{{display:flex;align-items:center;gap:10px;background:var(--card);border:1px solid var(--border);border-radius:12px;padding:10px 16px;margin-bottom:10px;}}
.bni{{background:linear-gradient(135deg,#C8102E,#8b0000);color:#fff;font-weight:900;font-size:.82em;padding:5px 13px;border-radius:7px;letter-spacing:2px;}}
.mtitle{{flex:1;font-size:.92em;font-weight:700;color:#f9fafb;line-height:1.3;}}
.mdate{{font-size:.74em;color:var(--muted);}}
.rdot{{width:10px;height:10px;border-radius:50%;background:#374151;flex-shrink:0;}}
.rdot.on{{background:#ef4444;animation:blink .9s infinite;}}
@keyframes blink{{0%,100%{{opacity:1}}50%{{opacity:.1}}}}
.rtimer{{font:700 1em/1 monospace;color:#60a5fa;min-width:44px;text-align:right;}}
.scores{{display:grid;grid-template-columns:1fr 1fr 1fr;gap:8px;margin-bottom:10px;}}
.score{{background:var(--card);border:1.5px solid var(--border);border-radius:10px;padding:12px 8px;text-align:center;cursor:pointer;transition:transform .2s;}}
.score:hover{{transform:translateY(-2px);}}
.score.tyfcb{{border-color:#27ae60;}}
.score.ref{{border-color:#C8102E;}}
.score.test{{border-color:#8e44ad;}}
.score .n{{font-size:2.4em;font-weight:900;line-height:1;}}
.score.tyfcb .n{{color:#4ade80;}}
.score.ref .n{{color:#f87171;}}
.score.test .n{{color:#c084fc;}}
.score .l{{font-size:.67em;color:var(--muted);margin-top:3px;font-weight:600;letter-spacing:.3px;}}
.det{{background:var(--card);border:1px solid var(--border);border-radius:10px;padding:8px 14px;margin-bottom:10px;display:flex;align-items:center;gap:10px;min-height:44px;}}
.det-lbl{{font-size:.68em;color:var(--muted);font-weight:700;letter-spacing:.5px;flex-shrink:0;text-transform:uppercase;}}
.pill{{display:inline-flex;align-items:center;gap:5px;border-radius:20px;padding:3px 12px;font-weight:700;font-size:.8em;animation:pop .3s cubic-bezier(.34,1.56,.64,1);}}
@keyframes pop{{from{{opacity:0;transform:scale(.5)}}to{{opacity:1;transform:scale(1)}}}}
.pill-t{{background:rgba(39,174,96,.15);border:1.5px solid #27ae60;color:#4ade80;}}
.pill-r{{background:rgba(200,16,46,.15);border:1.5px solid #C8102E;color:#f87171;}}
.pill-s{{background:rgba(142,68,173,.15);border:1.5px solid #8e44ad;color:#c084fc;}}
.pill-n{{background:rgba(26,86,219,.15);border:1.5px solid #1a56db;color:#60a5fa;}}
.tx{{background:var(--card);border:1px solid var(--border);border-radius:10px;padding:8px 12px;margin-bottom:10px;}}
.tx-hdr{{font-size:.66em;color:var(--muted);font-weight:700;letter-spacing:.5px;text-transform:uppercase;margin-bottom:5px;}}
.tx-body{{font-family:'Courier New',monospace;font-size:.78em;color:#93c5fd;white-space:pre-wrap;max-height:90px;overflow-y:auto;line-height:1.65;}}
.ts{{color:#e2e8f0;}}.ti{{color:#4b5563;font-style:italic;}}
.tsp{{color:#60a5fa;font-weight:700;}}.tt{{color:#4ade80;font-weight:700;}}
.tr{{color:#f87171;font-weight:700;}}.tst{{color:#c084fc;font-weight:700;}}
.prompt{{background:#1f2937;border:1px solid #374151;border-radius:10px;padding:10px 14px;margin-bottom:10px;display:none;animation:slidedn .2s ease;}}
.prompt.on{{display:block;}}
@keyframes slidedn{{from{{opacity:0;transform:translateY(-6px)}}to{{opacity:1;transform:translateY(0)}}}}
.ptitle{{font-size:.8em;color:#9ca3af;margin-bottom:8px;}}
.ptitle strong{{color:#f9fafb;}}
.pbtns{{display:flex;gap:6px;flex-wrap:wrap;}}
.pbtn{{border:none;border-radius:8px;padding:7px 13px;font-size:.78em;font-weight:700;cursor:pointer;transition:all .18s;}}
.pbtn:hover{{transform:translateY(-1px);opacity:.9;}}
.pb-t{{background:linear-gradient(135deg,#27ae60,#1e8449);color:#fff;}}
.pb-r{{background:linear-gradient(135deg,#C8102E,#8b0000);color:#fff;}}
.pb-s{{background:linear-gradient(135deg,#8e44ad,#6c3483);color:#fff;}}
.pb-x{{background:#374151;color:#9ca3af;}}
.ctrls{{display:grid;grid-template-columns:1fr 1fr 1fr;gap:8px;margin-bottom:12px;}}
.cbtn{{border:none;border-radius:10px;padding:13px 0;font-size:.88em;font-weight:700;cursor:pointer;transition:all .2s;}}
.cbtn:hover{{transform:translateY(-2px);opacity:.9;}}
.cbtn:disabled{{opacity:.35;cursor:not-allowed;transform:none;}}
.cb-start{{background:linear-gradient(135deg,#27ae60,#1e8449);color:#fff;}}
.cb-pause{{background:#1f2937;color:#9ca3af;border:1.5px solid #374151;}}
.cb-pause.on{{background:linear-gradient(135deg,#f59e0b,#d97706);color:#fff;border:none;}}
.cb-end{{background:linear-gradient(135deg,#C8102E,#8b0000);color:#fff;}}
.mhdr{{font-size:.75em;color:#9ca3af;font-weight:700;letter-spacing:.5px;text-transform:uppercase;margin-bottom:8px;display:flex;align-items:center;justify-content:space-between;}}
.mhdr span{{color:#4ade80;font-size:.85em;font-weight:400;letter-spacing:0;text-transform:none;}}
.mgrid{{display:grid;grid-template-columns:repeat(auto-fill,minmax(110px,1fr));gap:7px;margin-bottom:10px;max-height:280px;overflow-y:auto;padding-right:2px;}}
.mgrid::-webkit-scrollbar{{width:4px;}}
.mgrid::-webkit-scrollbar-track{{background:#111827;}}
.mgrid::-webkit-scrollbar-thumb{{background:#374151;border-radius:4px;}}
.mc{{background:var(--card);border:2px solid var(--border);border-radius:10px;padding:9px 7px;text-align:center;cursor:pointer;transition:all .22s;position:relative;user-select:none;}}
.mc:hover{{border-color:#374151;transform:translateY(-2px);box-shadow:0 6px 18px rgba(0,0,0,.4);}}
.mc.talking{{border-color:#60a5fa!important;background:#1e2d4a;box-shadow:0 0 0 3px rgba(96,165,250,.3);animation:cpulse .8s infinite;}}
.mc.scored{{animation:cflash .6s ease;}}
@keyframes cpulse{{0%,100%{{box-shadow:0 0 0 3px rgba(96,165,250,.3)}}50%{{box-shadow:0 0 0 7px rgba(96,165,250,.05)}}}}
@keyframes cflash{{0%{{background:#1f2937}}35%{{background:#1c3a2a;border-color:#27ae60}}100%{{background:var(--card)}}}}
.mav{{width:36px;height:36px;border-radius:50%;margin:0 auto 5px;display:flex;align-items:center;justify-content:center;font-weight:800;font-size:.85em;background:linear-gradient(135deg,#C8102E,#8b0000);color:#fff;}}
.mc.talking .mav{{background:linear-gradient(135deg,#1a56db,#1e3a8a);}}
.mname{{font-size:.71em;font-weight:700;color:#f3f4f6;margin-bottom:2px;white-space:nowrap;overflow:hidden;text-overflow:ellipsis;}}
.msub{{font-size:.6em;color:var(--muted);margin-bottom:3px;white-space:nowrap;overflow:hidden;text-overflow:ellipsis;}}
.mbdgs{{display:flex;justify-content:center;gap:2px;flex-wrap:wrap;min-height:15px;}}
.mb{{border-radius:6px;padding:1px 5px;font-size:.6em;font-weight:800;}}
.mb-t{{background:#27ae60;color:#fff;}}.mb-r{{background:#C8102E;color:#fff;}}.mb-s{{background:#8e44ad;color:#fff;}}
.mtot{{position:absolute;top:4px;right:6px;font-size:.6em;font-weight:800;color:#60a5fa;}}
.swav{{position:absolute;bottom:4px;left:50%;transform:translateX(-50%);display:none;gap:2px;align-items:flex-end;}}
.mc.talking .swav{{display:flex;}}
.sw{{width:3px;border-radius:2px;background:#60a5fa;animation:wave .7s infinite ease-in-out;}}
.sw:nth-child(1){{height:5px;animation-delay:0s}}.sw:nth-child(2){{height:10px;animation-delay:.12s}}.sw:nth-child(3){{height:7px;animation-delay:.24s}}.sw:nth-child(4){{height:13px;animation-delay:.08s}}.sw:nth-child(5){{height:4px;animation-delay:.2s}}
@keyframes wave{{0%,100%{{transform:scaleY(.3)}}50%{{transform:scaleY(1)}}}}
.adrow{{display:flex;gap:6px;margin-bottom:10px;}}
.adinp{{flex:1;background:#1f2937;border:1.5px solid #374151;border-radius:8px;padding:7px 11px;color:#f3f4f6;font-size:.82em;outline:none;}}
.adinp:focus{{border-color:#1a56db;}}.adinp::placeholder{{color:var(--muted);}}
.adbtn{{background:#1a56db;color:#fff;border:none;border-radius:8px;padding:7px 13px;font-size:.82em;font-weight:700;cursor:pointer;transition:background .2s;}}
.adbtn:hover{{background:#1e3a8a;}}
.help{{background:rgba(26,86,219,.06);border:1px solid rgba(26,86,219,.15);border-radius:8px;padding:8px 12px;font-size:.73em;color:var(--muted);line-height:1.75;}}
.kw-t{{color:#4ade80;font-weight:600;}}.kw-r{{color:#f87171;font-weight:600;}}.kw-s{{color:#c084fc;font-weight:600;}}
.toast{{position:fixed;bottom:16px;left:50%;transform:translateX(-50%) translateY(120px);background:#111827;border:1.5px solid #374151;border-radius:10px;padding:9px 20px;font-size:.8em;color:#f3f4f6;z-index:9999;transition:transform .35s cubic-bezier(.34,1.56,.64,1);pointer-events:none;white-space:nowrap;max-width:90vw;overflow:hidden;text-overflow:ellipsis;}}
.toast.on{{transform:translateX(-50%) translateY(0);}}
</style></head><body>
<div class="topbar">
  <div class="bni">BNI</div>
  <div><div class="mtitle">Leaders FTL &mdash; Meeting Recorder</div><div class="mdate">&#128197; {today_str} &nbsp;&#183;&nbsp; {day_of_week}</div></div>
  <div style="display:flex;align-items:center;gap:7px;margin-left:auto;"><div class="rdot" id="rdot"></div><span class="rtimer" id="rtimer">0:00</span></div>
</div>

<div class="scores">
  <div class="score tyfcb"><div class="n" id="sT">0</div><div class="l">&#127881; TYFCB</div></div>
  <div class="score ref"><div class="n" id="sR">0</div><div class="l">&#128279; Referrals</div></div>
  <div class="score test"><div class="n" id="sS">0</div><div class="l">&#11088; Testimonials</div></div>
</div>

<div class="det" id="det"><span class="det-lbl">LIVE</span><span id="detpills" style="color:var(--muted);font-size:.8em;">Waiting for recording to start...</span></div>

<div class="prompt" id="prompt">
  <div class="ptitle">Heard: <strong id="pspk"></strong> &mdash; What are they reporting?</div>
  <div class="pbtns">
    <button class="pbtn pb-t" onclick="logAct('tyfcb')">&#127881; Thank You for Closed Business</button>
    <button class="pbtn pb-r" onclick="logAct('referral')">&#128279; Referral Passed</button>
    <button class="pbtn pb-s" onclick="logAct('testimonial')">&#11088; Testimonial</button>
    <button class="pbtn pb-x" onclick="hidePrompt()">&#215; Dismiss</button>
  </div>
</div>

<div class="tx"><div class="tx-hdr">&#128250; Live Transcript</div><div class="tx-body" id="txbox">Press <strong style="color:#4ade80;">Start Recording</strong> when ready. Chrome recommended for best results.</div></div>

<div class="ctrls">
  <button class="cbtn cb-start" id="bStart" onclick="startRec()">&#9654; Start Recording</button>
  <button class="cbtn cb-pause" id="bPause" onclick="togPause()" disabled>&#9646;&#9646; Pause</button>
  <button class="cbtn cb-end" id="bEnd" onclick="endMeeting()">&#128231; End &amp; Send</button>
</div>

<div class="mhdr">&#128101; BNI LEADERS FTL MEMBERS <span>&#8212; Tap to log manually</span></div>
<div class="mgrid" id="mgrid"></div>

<div class="adrow"><input class="adinp" id="adinp" placeholder="Add a member name..." onkeydown="if(event.key==='Enter')addMember()"><button class="adbtn" onclick="addMember()">+ Add</button></div>

<div class="help">
  &#9679; Use <strong style="color:#f9fafb;">Chrome</strong> on desktop &nbsp;&#9679;&nbsp; Say the member's <strong style="color:#f9fafb;">first + last name</strong> first, then their activity<br>
  &#9679; <span class="kw-t">TYFCB &bull; closed business &bull; thank you for closed &bull; closed the deal</span><br>
  &#9679; <span class="kw-r">referral &bull; passing a referral &bull; referred &bull; i have a referral &bull; pass referral</span><br>
  &#9679; <span class="kw-s">testimonial &bull; give a testimonial &bull; shout out &bull; recognize &bull; want to recognize</span>
</div>
<div class="toast" id="toast"></div>

<script>
var MEMBERS = {members_js};
var tally = {{}};
var txFull = "";
var recog = null;
var tick = null;
var secs = 0;
var isRec = false;
var isPaused = false;
var curSpk = null;
var pendSpk = null;
var pendTxt = "";

var KT = ["thank you for closed business","tyfcb","closed business","closed the deal","ty for closed","thank you closed","tyfcob","closed deal","business closed","close of business"];
var KR = ["referral","pass a referral","passing a referral","referred","i have a referral","giving a referral","pass referral","i want to pass","have a referral","give a referral","i'm passing","i am passing"];
var KS = ["testimonial","give a testimonial","giving a testimonial","would like to recognize","want to recognize","shout out","shoutout","recognize","i want to give a testimonial","give testimonial"];

function detAct(t){{var s=t.toLowerCase();for(var i=0;i<KT.length;i++)if(s.indexOf(KT[i])>-1)return"tyfcb";for(var i=0;i<KR.length;i++)if(s.indexOf(KR[i])>-1)return"referral";for(var i=0;i<KS.length;i++)if(s.indexOf(KS[i])>-1)return"testimonial";return null;}}
function detMbr(t){{var s=t.toLowerCase();var best=null,bs=0;for(var i=0;i<MEMBERS.length;i++){{var pts=MEMBERS[i].toLowerCase().split(" ");var sc=0;for(var j=0;j<pts.length;j++)if(pts[j].length>2&&s.indexOf(pts[j])>-1)sc+=pts[j].length;if(sc>bs){{bs=sc;best=MEMBERS[i];}}}}return bs>=3?best:null;}}

function initAll(){{
  tally={{}};
  MEMBERS.forEach(function(m){{tally[m]={{t:0,r:0,s:0}};}}); 
  buildGrid();
}}
function mkey(n){{return n.replace(/\s+/g,"_");}}
function initials(n){{return n.split(" ").map(function(w){{return w[0];}}).join("").substring(0,2).toUpperCase();}}

function buildGrid(){{
  var g=document.getElementById("mgrid");g.innerHTML="";
  MEMBERS.forEach(function(m){{
    var k=mkey(m),ini=initials(m);
    var fn=m.split(" ")[0],ln=m.split(" ").slice(1).join(" ");
    var d=document.createElement("div");
    d.className="mc";d.id="mc-"+k;
    d.innerHTML='<div class="mtot" id="tot-'+k+'"></div>'+
      '<div class="mav" id="av-'+k+'">'+ini+'</div>'+
      '<div class="mname">'+fn+'</div>'+
      '<div class="msub">'+ln+'</div>'+
      '<div class="mbdgs" id="bdg-'+k+'"></div>'+
      '<div class="swav"><div class="sw"></div><div class="sw"></div><div class="sw"></div><div class="sw"></div><div class="sw"></div></div>';
    d.onclick=(function(nm){{return function(){{pendSpk=nm;curSpk=nm;showPrompt(nm,"");}};}})(m);
    g.appendChild(d);
  }});
}}

function updCard(n){{
  var k=mkey(n);var d=tally[n];if(!d)return;
  var tot=d.t+d.r+d.s;
  var te=document.getElementById("tot-"+k);if(te)te.textContent=tot||"";
  var bg=document.getElementById("bdg-"+k);if(!bg)return;
  var h="";
  if(d.t>0)h+='<span class="mb mb-t">T'+d.t+'</span>';
  if(d.r>0)h+='<span class="mb mb-r">R'+d.r+'</span>';
  if(d.s>0)h+='<span class="mb mb-s">S'+d.s+'</span>';
  bg.innerHTML=h;
  var card=document.getElementById("mc-"+k);
  if(card){{card.classList.add("scored");setTimeout(function(){{card.classList.remove("scored");}},650);}}
  updScores();
}}
function updScores(){{
  var t=0,r=0,s=0;
  Object.keys(tally).forEach(function(k){{t+=tally[k].t||0;r+=tally[k].r||0;s+=tally[k].s||0;}});
  document.getElementById("sT").textContent=t;
  document.getElementById("sR").textContent=r;
  document.getElementById("sS").textContent=s;
}}
function setTalking(n){{
  MEMBERS.forEach(function(m){{var c=document.getElementById("mc-"+mkey(m));if(c)c.classList.remove("talking");}});
  if(n){{var c=document.getElementById("mc-"+key(n));if(c){{c.classList.add("talking");c.scrollIntoView({{behavior:"smooth",block:"nearest"}});}}}}
}}
function showPrompt(n,txt){{
  pendSpk=n;
  document.getElementById("pspk").textContent=n;
  document.getElementById("prompt").classList.add("on");
}}
function hidePrompt(){{document.getElementById("prompt").classList.remove("on");pendSpk=null;}}
function logAct(type){{if(!pendSpk)return;log(pendSpk,type,pendTxt);hidePrompt();}}
function log(n,type,txt){{
  if(!tally[n])tally[n]={{t:0,r:0,s:0}};
  if(type==="tyfcb")tally[n].t++;
  else if(type==="referral")tally[n].r++;
  else tally[n].s++;
  updCard(n);
  var em=type==="tyfcb"?"&#127881; TYFCB":type==="referral"?"&#128279; Referral":"&#11088; Testimonial";
  toast("&#127942; "+n.split(" ")[0]+" \u2014 "+em+" logged!");
  txAppend(n,"["+type.toUpperCase()+" LOGGED]","ta");
  setDetected(n,type);
}}
function setDetected(n,type){{
  var pc=type==="tyfcb"?"pill-t":type==="referral"?"pill-r":"pill-s";
  var pl=type==="tyfcb"?"&#127881; TYFCB":type==="referral"?"&#128279; Referral":"&#11088; Testimonial";
  document.getElementById("detpills").innerHTML='<span class="pill pill-n">&#127908; '+n+'</span>&nbsp;<span class="pill '+pc+'">'+pl+'</span>';
}}
function txAppend(spk,txt,cls){{
  var b=document.getElementById("txbox");
  if(b.innerText.indexOf("Press")>-1)b.innerHTML="";
  var d=document.createElement("div");
  d.innerHTML='<span class="tsp">'+(spk||"")+':</span> <span class="'+cls+'">'+txt+'</span>';
  b.appendChild(d);b.scrollTop=b.scrollHeight;
  txFull+=(spk||"")+": "+txt+String.fromCharCode(10);
}}
function setInterim(spk,txt){{
  var b=document.getElementById("txbox");
  var ex=b.querySelector(".interim-line");if(ex)ex.remove();
  if(!txt)return;
  var d=document.createElement("div");d.className="interim-line";
  d.innerHTML='<span class="tsp">'+(spk||"...")+':</span> <span class="ti">'+txt+'</span>';
  b.appendChild(d);b.scrollTop=b.scrollHeight;
}}
function fmt(s){{return Math.floor(s/60)+":"+(s%60<10?"0":"")+s%60;}}

function startRec(){{
  isRec=true;isPaused=false;
  document.getElementById("rdot").className="rdot on";
  document.getElementById("bStart").disabled=true;
  document.getElementById("bPause").disabled=false;
  document.getElementById("bPause").className="cbtn cb-pause on";
  document.getElementById("bPause").innerHTML="&#9646;&#9646; Pause";
  tick=setInterval(function(){{secs++;document.getElementById("rtimer").textContent=fmt(secs);}},1000);
  startSR();
  document.getElementById("detpills").innerHTML='<span style="color:#4ade80;font-size:.8em;">&#9679; Recording live &mdash; speak naturally</span>';
}}

function startSR(){{
  var SR=window.SpeechRecognition||window.webkitSpeechRecognition;
  if(!SR){{
    var b=document.getElementById("txbox");
    b.innerHTML='<span style="color:#f87171;">&#9888; Speech recognition requires Chrome. Use the member cards below to log manually.</span>';
    return;
  }}
  recog=new SR();recog.continuous=true;recog.interimResults=true;recog.lang="en-US";
  recog.onresult=function(e){{
    var interim="";
    for(var i=e.resultIndex;i<e.results.length;i++){{
      var txt=e.results[i][0].transcript.trim();
      if(e.results[i].isFinal){{
        var spk=detMbr(txt);var act=detAct(txt);
        if(spk){{curSpk=spk;setTalking(spk);}}
        if(act&&curSpk){{pendSpk=curSpk;pendTxt=txt;log(curSpk,act,txt);}}
        else if(spk&&!act){{pendSpk=spk;pendTxt=txt;showPrompt(spk,txt);}}
        txAppend(curSpk||"?",txt,"ts");setInterim(null,"");
      }}else interim=txt;
    }}
    if(interim)setInterim(curSpk||"...",interim);
  }};
  recog.onerror=function(err){{
    if(err.error!=="no-speech")
      document.getElementById("detpills").innerHTML='<span style="color:#f87171;">&#9888; Mic error: '+err.error+'. Check browser permissions.</span>';
  }};
  recog.onend=function(){{if(isRec&&!isPaused)recog.start();}};
  recog.start();
}}

function togPause(){{
  if(!isRec)return;
  if(!isPaused){{
    isPaused=true;
    if(recog){{try{{recog.stop();}}catch(e){{}}}}
    clearInterval(tick);
    document.getElementById("rdot").className="rdot";
    document.getElementById("bPause").innerHTML="&#9654; Resume";
    document.getElementById("bPause").className="cbtn cb-pause";
    setTalking(null);toast("&#9646; Recording paused");
  }}else{{
    isPaused=false;
    document.getElementById("rdot").className="rdot on";
    document.getElementById("bPause").innerHTML="&#9646;&#9646; Pause";
    document.getElementById("bPause").className="cbtn cb-pause on";
    tick=setInterval(function(){{secs++;document.getElementById("rtimer").textContent=fmt(secs);}},1000);
    startSR();toast("&#9654; Recording resumed");
  }}
}}

function addMember(){{
  var inp=document.getElementById("adinp");var n=inp.value.trim();
  if(!n||MEMBERS.indexOf(n)>-1){{inp.value="";return;}}
  MEMBERS.push(n);tally[n]={{t:0,r:0,s:0}};inp.value="";buildGrid();toast("Added: "+n);
}}

function toast(msg){{
  var t=document.getElementById("toast");t.innerHTML=msg;t.className="toast on";
  setTimeout(function(){{t.className="toast";}},3000);
}}

function endMeeting(){{
  if(isRec){{isRec=false;isPaused=false;clearInterval(tick);}}
  if(recog){{try{{recog.stop();}}catch(e){{}}recog=null;}}
  document.getElementById("rdot").className="rdot";
  document.getElementById("bStart").disabled=false;
  document.getElementById("bPause").disabled=true;
  setTalking(null);
  var arr=MEMBERS.map(function(m){{var d=tally[m]||{{t:0,r:0,s:0}};return{{name:m,tyfcb:d.t,referral:d.r,testimonial:d.s}};}}).filter(function(x){{return x.tyfcb+x.referral+x.testimonial>0;}});
  var payload=JSON.stringify({{tally:arr,transcript:txFull,duration:fmt(secs)}});
  try{{sessionStorage.setItem("bni_report",payload);}}catch(e){{}}
  window.parent.postMessage({{type:"bni_end",payload:payload}},"*");
  document.getElementById("bEnd").innerHTML="\u2714 Done! Use Send Button Below";
  document.getElementById("bEnd").style.background="linear-gradient(135deg,#27ae60,#1e8449)";
  toast("&#128231; Meeting ended! Scroll down and click Send Report.");
}}

initAll();
</script></body></html>"""
    st.components.v1.html(recorder_html, height=950, scrolling=True)

    st.markdown("---")
    st.markdown("""
    <div style='background:linear-gradient(135deg,#0a0e1a,#111827);border-radius:14px;padding:18px 22px;border:1.5px solid #1f2937;margin-bottom:14px;'>
      <h3 style='color:#f9fafb!important;margin:0 0 6px;font-size:1.05em;border:none!important;'>&#128231; Send Meeting Report</h3>
      <p style='color:#9ca3af;font-size:.84em;margin:0;'>After pressing <strong style='color:#60a5fa;'>End &amp; Send</strong> in the recorder, click below to instantly email the full scorecard to <strong style='color:#f9fafb;'>Austin, Joel &amp; Elena</strong>.</p>
    </div>
    """, unsafe_allow_html=True)

    col_d, col_b = st.columns([3,2])
    with col_d:
        report_date = st.text_input("Date", value=today_str, key="rdate", label_visibility="collapsed")
    with col_b:
        send_now = st.button("\U0001f4e8 Send Report Now", key="send_rpt")

    if send_now:
        gu, gp = get_gmail_creds()
        if not gu or not gp:
            st.warning("\U0001f512 GMAIL_USER and GMAIL_APP_PASSWORD secrets not set in Streamlit Cloud.")
        else:
            ok, info = send_meeting_report(report_date, [], "(Transcript captured in recorder — use End & Send button above to pass data)", "N/A")
            if ok:
                recips = ", ".join(info)
                st.markdown(f"""<div style='background:rgba(39,174,96,.1);border:1.5px solid #27ae60;border-radius:10px;padding:14px 18px;text-align:center;color:#4ade80;font-weight:700;'>&#127881; Report sent to: {recips}</div>""", unsafe_allow_html=True)
            else:
                st.error(f"Could not send: {info}")

    st.markdown("""
    <div style='background:rgba(200,16,46,.06);border:1px solid rgba(200,16,46,.15);border-radius:10px;padding:12px 16px;margin-top:8px;font-size:.8em;color:#6b7280;line-height:1.75;'>
      <strong style='color:#9ca3af;'>&#128197; Thursday 8:30 AM Auto-Report:</strong> A reminder email is automatically sent to Austin, Joel &amp; Elena every Thursday at 8:30 AM with a meeting checklist and chapter hub link.<br>
      <strong style='color:#9ca3af;'>&#128161; Tips:</strong> Use <strong style='color:#f9fafb;'>Chrome</strong> on desktop &nbsp;&#183;&nbsp; Say member's <strong style='color:#f9fafb;'>first + last name</strong> then their activity &nbsp;&#183;&nbsp; Tap cards to log manually.
    </div>
    """, unsafe_allow_html=True)
    st.markdown("""<div class='footer-bar'>&#128274; BNI Leaders FTL Chapter Hub &nbsp;|&nbsp; Reports sent to Austin, Joel &amp; Elena &nbsp;|&nbsp; Powered by <a href='https://mrceesai.com'>MrCeesAI</a></div>""", unsafe_allow_html=True)
