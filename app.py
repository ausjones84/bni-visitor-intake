import streamlit as st
import gspread
from google.oauth2.service_account import Credentials
from datetime import datetime
import json
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import random

st.set_page_config(page_title="BNI Leaders FTL", page_icon="U0001f91d", layout="centered")

if "page" not in st.session_state:
    st.session_state["page"] = "landing"

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700;800;900&display=swap');
*{font-family:'Inter',Arial,sans-serif;}
@keyframes fadeInDown{from{opacity:0;transform:translateY(-18px);}to{opacity:1;transform:translateY(0);}}
@keyframes fadeInUp{from{opacity:0;transform:translateY(18px);}to{opacity:1;transform:translateY(0);}}
@keyframes float{0%,100%{transform:translateY(0);}50%{transform:translateY(-6px);}}
[data-testid="stAppViewContainer"]{background:linear-gradient(160deg,#0a0014 0%,#1a0a0a 40%,#0d0d1a 100%) !important;min-height:100vh;}
[data-testid="stHeader"]{background:transparent !important;}
.block-container{padding-top:1rem !important;}
.stButton>button{background:linear-gradient(135deg,#C8102E 0%,#a00d24 100%) !important;color:white !important;font-weight:700 !important;border-radius:10px !important;padding:.75em 2em !important;font-size:1em !important;width:100% !important;border:none !important;margin-top:10px !important;transition:all .2s !important;box-shadow:0 4px 16px rgba(200,16,46,.35) !important;}
.stButton>button:hover{transform:translateY(-3px) !important;box-shadow:0 8px 24px rgba(200,16,46,.5) !important;}
h1,h2,h3{color:#C8102E !important;}
h2{border-bottom:2px solid rgba(200,16,46,.2) !important;padding-bottom:6px !important;}
.stTextInput>div>div>input,.stTextArea>div>div>textarea,.stSelectbox>div>div{background:#1a1a2e !important;color:#e8edf3 !important;border:1.5px solid #2d2d4e !important;border-radius:8px !important;}
.stSelectbox>div>div>div{color:#e8edf3 !important;}
label{color:#c8d0e0 !important;}
.footer-bar{text-align:center;margin-top:2.5em;padding:1.2em;background:rgba(255,255,255,.04);border-radius:12px;font-size:.83em;color:#666;border:1px solid rgba(255,255,255,.06);}
.footer-bar a{color:#C8102E !important;}
</style>
""", unsafe_allow_html=True)

st.markdown("""
<div style='text-align:center;padding:14px 0 6px;animation:fadeInDown .6s ease both;'>
  <div style='display:inline-block;background:linear-gradient(135deg,#C8102E 0%,#8b0000 100%);color:white;font-size:1.55em;font-weight:900;padding:9px 32px;border-radius:12px;letter-spacing:3px;box-shadow:0 6px 24px rgba(200,16,46,.5);'>BNI Leaders FTL</div>
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
    .land-card.vc .land-title{color:#ff6b6b !important;}
    .land-card.mc .land-title{color:#60a5fa !important;}
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
        <p class='land-desc'>Members: Hit record, speak naturally, and let AI tally your TYFCB, referrals &amp; testimonials!</p>
        <div class='land-cta'>&#127908;&nbsp; Open Live Recorder</div>
      </div>
    </div>
    <div style='margin:20px 0;background:rgba(200,16,46,.06);border:1px solid rgba(200,16,46,.2);border-radius:14px;padding:18px 22px;'>
      <div style='color:#ff6b6b;font-weight:700;font-size:.9em;margin-bottom:10px;'>&#127942; BNI Leaders FTL &mdash; What We Do</div>
      <div style='display:grid;grid-template-columns:1fr 1fr;gap:8px;font-size:.84em;color:#9ca3af;'>
        <div>&#10003; Pass qualified referrals weekly</div><div>&#10003; Track TYFCB &amp; testimonials</div>
        <div>&#10003; One member per profession</div><div>&#10003; 30+ active business leaders</div>
        <div>&#10003; Real-time meeting scoreboard</div><div>&#10003; Automated weekly reports</div>
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
    if st.button("← Back to Home", key="back_v"):
        st.session_state["page"] = "landing"
        st.rerun()

    def send_visitor_welcome(fn, ve, bn, il, gu, gp):
        try:
            msg = MIMEMultipart("alternative")
            msg["Subject"] = f"Great connecting with you at BNI, {fn}!"
            msg["From"] = gu; msg["To"] = ve
            html = f"""<div style="font-family:Arial,sans-serif;max-width:600px;margin:auto;"><div style="background:linear-gradient(135deg,#C8102E,#8b0000);color:white;padding:20px 24px;border-radius:10px 10px 0 0;"><div style="font-size:1.8em;font-weight:900;letter-spacing:3px;">BNI Leaders FTL</div><h2 style="margin:8px 0 0;color:white !important;">Thanks for Visiting, {fn}!</h2></div><div style="background:#f9f9f9;padding:24px;border-radius:0 0 10px 10px;"><p>Hi {fn}, thank you for joining us at BNI Leaders FTL! A member will reach out shortly.</p><p><strong>Business:</strong> {bn} &mdash; <strong>Interest:</strong> {il}</p><p>See you next Thursday!</p><p style="font-size:.85em;color:#888;">Need AI automation? <a href="https://mrceesai.com" style="color:#C8102E;">MrCeesAI by Austin Jones</a></p></div></div>"""
            msg.attach(MIMEText(html, "html"))
            with smtplib.SMTP_SSL("smtp.gmail.com", 465) as s:
                s.login(gu, gp); s.sendmail(gu, ve, msg.as_string())
            return True
        except Exception:
            return False

    def send_hot_lead(fn, ln, ve, ph, bn, ind, ep, il, gu, gp, re_):
        try:
            msg = MIMEMultipart("alternative")
            msg["Subject"] = f"BNI HOT LEAD — {fn} {ln} ({bn})"
            msg["From"] = gu; msg["To"] = re_
            html = f"""<div style="font-family:Arial,sans-serif;max-width:600px;margin:auto;"><div style="background:#27ae60;color:white;padding:16px 24px;border-radius:10px 10px 0 0;"><h2 style="margin:0;color:white !important;">U0001f525 HOT BNI LEAD &mdash; {il}</h2></div><div style="background:#f0fff4;padding:24px;border-radius:0 0 10px 10px;border:2px solid #27ae60;"><p><strong>{fn} {ln}</strong> &mdash; {bn} ({ind})</p><p>Email: <a href="mailto:{ve}">{ve}</a> | Phone: {ph or "N/A"}</p><p><em>"{ep}"</em></p><p style="color:#27ae60;font-weight:700;">Reach out NOW!</p></div></div>"""
            msg.attach(MIMEText(html, "html"))
            with smtplib.SMTP_SSL("smtp.gmail.com", 465) as s:
                s.login(gu, gp); s.sendmail(gu, re_, msg.as_string())
            return True
        except Exception:
            return False

    BNI_TIPS = [
        "&#128161; <strong>BNI Tip:</strong> The most successful members give referrals before expecting to receive.",
        "&#128161; <strong>BNI Tip:</strong> Your 60-second pitch should be crystal-clear &mdash; easier to refer you!",
        "&#128161; <strong>BNI Tip:</strong> BNI members generate an average of $50,000+ in new business per year.",
        "&#128161; <strong>BNI Tip:</strong> Givers Gain&#174; &mdash; members who give the most referrals receive the most.",
        "&#128161; <strong>BNI Tip:</strong> 1-2-1 meetings are the #1 driver of strong referral relationships.",
        "&#128161; <strong>BNI Tip:</strong> The average BNI chapter passes over $1 million in referrals each year.",
    ]

    st.markdown(f"""<div style='background:rgba(200,16,46,.08);border-left:5px solid #C8102E;padding:1em 1.5em;border-radius:0 8px 8px 0;margin-bottom:1em;color:#e8edf3;'><strong style='color:#ff6b6b;'>Thanks for visiting!</strong> Fill out this quick form and our members will follow up.</div>
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
        v_submitted = st.form_submit_button("U0001f91d Submit — We Will Be In Touch!")

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
                gu = st.secrets["GMAIL_USER"]; gp = st.secrets["GMAIL_APP_PASSWORD"]
                re_ = st.secrets["REPORT_EMAIL"]
                send_visitor_welcome(first_name.strip(), email.strip(), business_name.strip(), ready_to_join, gu, gp)
                if ready_to_join in ["Ready to apply!", "Very interested"]:
                    send_hot_lead(first_name.strip(), last_name.strip(), email.strip(), phone.strip(), business_name.strip(), fin_industry, elevator_pitch.strip(), ready_to_join, gu, gp, re_)
            except KeyError:
                pass
            except Exception:
                pass
            st.components.v1.html("""<canvas id="cc" style="position:fixed;top:0;left:0;width:100vw;height:100vh;pointer-events:none;z-index:9999;"></canvas><script>(function(){var c=document.getElementById("cc"),ctx=c.getContext("2d");c.width=window.innerWidth;c.height=window.innerHeight;var cols=["#C8102E","#FFD700","#27ae60","#3498db","#f39c12","#fff","#e74c3c"];var pp=[];for(var i=0;i<160;i++)pp.push({x:Math.random()*c.width,y:Math.random()*c.height-c.height,w:Math.random()*10+5,h:Math.random()*5+3,col:cols[Math.floor(Math.random()*cols.length)],rot:Math.random()*360,vx:Math.random()*2-1,vy:Math.random()*4+2,vr:Math.random()*6-3});var f=0;function draw(){ctx.clearRect(0,0,c.width,c.height);pp.forEach(function(p){ctx.save();ctx.translate(p.x,p.y);ctx.rotate(p.rot*Math.PI/180);ctx.fillStyle=p.col;ctx.globalAlpha=.85;ctx.fillRect(-p.w/2,-p.h/2,p.w,p.h);ctx.restore();p.x+=p.vx;p.y+=p.vy;p.rot+=p.vr;if(p.y>c.height){p.y=-10;p.x=Math.random()*c.width;}});f++;if(f<200)requestAnimationFrame(draw);else ctx.clearRect(0,0,c.width,c.height);}draw();})();</script>""", height=0)
            st.balloons()
            st.markdown(f"""<div style='background:rgba(39,174,96,.08);border:1.5px solid #27ae60;border-radius:12px;padding:1.5em;margin-top:1em;'><h3 style='color:#27ae60;margin-top:0;'>&#127881; Thanks, {first_name}! You are all set.</h3><table style='width:100%;font-size:.95em;border-collapse:collapse;color:#e8edf3;'><tr><td style='padding:5px 8px;color:#9ca3af;width:110px;'><strong>Name</strong></td><td>{first_name} {last_name}</td></tr><tr style='background:rgba(39,174,96,.05);'><td style='padding:5px 8px;color:#9ca3af;'><strong>Business</strong></td><td>{business_name}</td></tr><tr><td style='padding:5px 8px;color:#9ca3af;'><strong>Interest</strong></td><td><strong style='color:#C8102E;'>{ready_to_join}</strong></td></tr></table><div style='background:rgba(39,174,96,.08);border:1px solid rgba(39,174,96,.3);border-radius:8px;padding:10px 14px;margin-top:12px;font-size:.9em;color:#4ade80;'><strong>What happens next?</strong><br>&#10003; A BNI member contacts you within 24 hours.<br>&#10003; You will be invited to a 1-2-1 coffee meeting.<br>&#10003; You can apply for membership and lock in your profession!</div></div>""", unsafe_allow_html=True)

elif st.session_state["page"] == "recorder":
    if st.button("← Back to Home", key="back_r"):
        st.session_state["page"] = "landing"
        st.rerun()

    today_str = datetime.now().strftime("%B %d, %Y")
    day_of_week = datetime.now().strftime("%A")

    BNI_MEMBERS = [
        "Alex Laraia", "Cassandra Exantus", "Cecil Pardave", "Chris Rios",
        "Connie Kaplan", "Dan Hahn", "Devaney Mangroo", "Edgar Villarreal",
        "Elena Blose", "Elizabeth Hornsby", "Freddy Santory", "JC Aleman",
        "Jessica Goulart", "Joel Bruno", "Kamili Kelly", "Kristie Estevez-Puente",
        "Kristin Marrero", "Lauren Klein", "Lisa Jones", "Marisol Cruz",
        "Mauricio Cavanzo", "Michael Elias", "Michael Gigante", "Michelle Notte",
        "Nathan McCune", "Nishant Thaker", "Omar Abdel", "Richard Saulsberry",
        "Roberta Schwartz", "Sebastian Felipe Gonzalez", "Stephanie Taylor",
        "Tatiana Smidi", "Tegdra Samuel", "Austin Jones"
    ]

    def send_meeting_report(date_str, tally_data, transcript, gmail_user, gmail_pass):
        recipients = ["ausjones84@gmail.com"]
        try:
            extra = st.secrets.get("REPORT_EMAIL","")
            if extra:
                for r in extra.split(","):
                    r = r.strip()
                    if r and r not in recipients:
                        recipients.append(r)
        except Exception:
            pass
        tally = tally_data if tally_data else []
        total_t = sum(m.get("tyfcb",0) for m in tally)
        total_r = sum(m.get("referral",0) for m in tally)
        total_s = sum(m.get("testimonial",0) for m in tally)
        tally_sorted = sorted(tally, key=lambda x: x.get("tyfcb",0)+x.get("referral",0)+x.get("testimonial",0), reverse=True)
        rows = ""
        for i,m in enumerate(tally_sorted):
            tot = m.get("tyfcb",0)+m.get("referral",0)+m.get("testimonial",0)
            if tot == 0: continue
            bg = "#f9f9f9" if i%2 else "#fff"
            medal = "U0001f947" if i==0 else ("U0001f948" if i==1 else ("U0001f949" if i==2 else ""))
            rows += f"""<tr style='background:{bg};'><td style='padding:10px 12px;font-weight:700;'>{medal} {m.get("name","")}</td><td style='padding:10px 12px;text-align:center;'><span style='background:#27ae60;color:white;border-radius:20px;padding:3px 10px;font-weight:700;'>{m.get("tyfcb",0)}</span></td><td style='padding:10px 12px;text-align:center;'><span style='background:#C8102E;color:white;border-radius:20px;padding:3px 10px;font-weight:700;'>{m.get("referral",0)}</span></td><td style='padding:10px 12px;text-align:center;'><span style='background:#8e44ad;color:white;border-radius:20px;padding:3px 10px;font-weight:700;'>{m.get("testimonial",0)}</span></td><td style='padding:10px 12px;text-align:center;font-weight:800;color:#1a56db;'>{tot}</td></tr>"""
        top3 = [m for m in tally_sorted if m.get("tyfcb",0)+m.get("referral",0)+m.get("testimonial",0)>0][:3]
        podium_html = ""
        pcols = ["#f39c12","#95a5a6","#cd7f32"]
        plbls = ["U0001f947 1st","U0001f948 2nd","U0001f949 3rd"]
        for idx,m in enumerate(top3):
            podium_html += f"""<td style='text-align:center;padding:8px;vertical-align:bottom;'><div style='background:{pcols[idx]};color:white;border-radius:10px 10px 0 0;padding:14px 10px 8px;font-weight:800;min-width:110px;'>{plbls[idx]}<br><span style='font-size:1.2em;'>{m.get("name","").split()[0]}</span></div><div style='background:#f0f0f0;padding:6px;font-size:.8em;color:#555;border-radius:0 0 8px 8px;'>T:{m.get("tyfcb",0)} R:{m.get("referral",0)} S:{m.get("testimonial",0)}</div></td>"""
        html_body = f"""<div style="font-family:Arial,sans-serif;max-width:750px;margin:auto;background:#fff;"><div style="background:linear-gradient(135deg,#C8102E 0%,#8b0000 100%);color:white;padding:26px 32px;border-radius:14px 14px 0 0;"><div style="font-size:1.5em;font-weight:900;letter-spacing:3px;margin-bottom:4px;">BNI Leaders FTL</div><h2 style="margin:0;color:white !important;font-size:1.5em;">&#127908; Weekly Meeting Report</h2><p style="margin:6px 0 0;opacity:.85;">&#128197; {date_str} &mdash; Generated at {datetime.now().strftime("%I:%M %p")}</p></div><div style="padding:28px 32px;background:#f8f9fa;"><table style="width:100%;border-collapse:collapse;margin-bottom:28px;"><tr><td style="text-align:center;background:#27ae60;color:white;padding:18px;border-radius:12px;width:30%;"><div style="font-size:2.8em;font-weight:900;line-height:1;">{total_t}</div><div style="font-size:.9em;opacity:.9;margin-top:4px;">&#127881; TYFCBs</div></td><td style="width:4%;"></td><td style="text-align:center;background:#C8102E;color:white;padding:18px;border-radius:12px;width:30%;"><div style="font-size:2.8em;font-weight:900;line-height:1;">{total_r}</div><div style="font-size:.9em;opacity:.9;margin-top:4px;">&#128279; Referrals</div></td><td style="width:4%;"></td><td style="text-align:center;background:#8e44ad;color:white;padding:18px;border-radius:12px;width:30%;"><div style="font-size:2.8em;font-weight:900;line-height:1;">{total_s}</div><div style="font-size:.9em;opacity:.9;margin-top:4px;">&#11088; Testimonials</div></td></tr></table>{"<h3 style='color:#f39c12;margin:0 0 12px;'>&#127942; Top Contributors</h3><table style='width:100%;border-collapse:collapse;margin-bottom:28px;'><tr>" + podium_html + "</tr></table>" if top3 else ""}<h3 style="color:#1a56db;margin:0 0 12px;">&#128203; Full Scorecard</h3><table style="width:100%;border-collapse:collapse;font-size:.93em;margin-bottom:28px;border-radius:10px;overflow:hidden;box-shadow:0 2px 12px rgba(0,0,0,.08);"><thead><tr style="background:#1a56db;color:white;"><th style="padding:10px 12px;text-align:left;">Member</th><th style="padding:10px 12px;text-align:center;">&#127881; TYFCB</th><th style="padding:10px 12px;text-align:center;">&#128279; Referrals</th><th style="padding:10px 12px;text-align:center;">&#11088; Testimonials</th><th style="padding:10px 12px;text-align:center;">Total</th></tr></thead><tbody>{rows or "<tr><td colspan='5' style='padding:14px;text-align:center;color:#999;'>No activity recorded</td></tr>"}</tbody></table><h3 style="color:#555;font-size:.95em;">&#128221; Meeting Transcript</h3><div style="background:#0d1117;border-radius:10px;padding:16px;font-family:monospace;font-size:.82em;color:#58a6ff;white-space:pre-wrap;max-height:280px;overflow-y:auto;">{transcript or "No transcript captured."}</div><p style="font-size:.78em;color:#aaa;margin-top:24px;text-align:center;border-top:1px solid #eee;padding-top:16px;">&#x1F916; Automated by BNI Leaders FTL Chapter Hub &mdash; <a href="https://mrceesai.com" style="color:#C8102E;">mrceesai.com</a></p></div></div>"""
        try:
            msg = MIMEMultipart("alternative")
            msg["Subject"] = f"U0001f3c6 BNI Leaders FTL Meeting Report — {date_str}"
            msg["From"] = gmail_user; msg["To"] = ", ".join(recipients)
            msg.attach(MIMEText(html_body,"html"))
            with smtplib.SMTP_SSL("smtp.gmail.com",465) as srv:
                srv.login(gmail_user,gmail_pass); srv.sendmail(gmail_user,recipients,msg.as_string())
            return True, recipients
        except Exception as e:
            return False, str(e)

    members_js = json.dumps(BNI_MEMBERS)
    st.components.v1.html(f"""<!DOCTYPE html><html><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>BNI Meeting Recorder</title>
<style>
*{{box-sizing:border-box;margin:0;padding:0;font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',Arial,sans-serif;}}
body{{background:#0a0e1a;color:#e8edf3;min-height:100vh;padding:10px;}}
.top-bar{{display:flex;align-items:center;gap:10px;background:#111827;border-radius:12px;padding:10px 16px;margin-bottom:10px;border:1px solid #1f2937;}}
.bni-badge{{background:linear-gradient(135deg,#C8102E,#8b0000);color:white;font-weight:900;font-size:.85em;padding:5px 12px;border-radius:8px;letter-spacing:2px;flex-shrink:0;}}
.meeting-title{{flex:1;font-size:.95em;font-weight:700;color:#f9fafb;}}
.meeting-date{{font-size:.78em;color:#6b7280;}}
.rec-dot{{width:11px;height:11px;border-radius:50%;background:#374151;flex-shrink:0;transition:background .3s;}}
.rec-dot.live{{background:#ef4444;animation:blink .9s infinite;}}
@keyframes blink{{0%,100%{{opacity:1;}}50%{{opacity:.15;}}}}
.timer{{font-family:monospace;font-size:1em;font-weight:700;color:#60a5fa;min-width:44px;}}
.score-totals{{display:flex;gap:8px;margin-bottom:10px;}}
.total-pill{{flex:1;text-align:center;border-radius:10px;padding:10px 6px;}}
.total-pill .num{{font-size:2em;font-weight:900;line-height:1;}}
.total-pill .lbl{{font-size:.68em;opacity:.85;margin-top:2px;}}
.tp-t{{background:rgba(39,174,96,.15);border:1.5px solid #27ae60;}}
.tp-r{{background:rgba(200,16,46,.15);border:1.5px solid #C8102E;}}
.tp-s{{background:rgba(142,68,173,.15);border:1.5px solid #8e44ad;}}
.detected-wrap{{background:#111827;border-radius:10px;padding:8px 14px;margin-bottom:10px;border:1px solid #1f2937;display:flex;align-items:center;gap:10px;min-height:46px;}}
.detected-label{{font-size:.7em;color:#6b7280;font-weight:600;letter-spacing:.5px;flex-shrink:0;}}
.detected-pill{{display:inline-flex;align-items:center;gap:5px;border-radius:20px;padding:3px 12px;font-weight:700;font-size:.82em;animation:popIn .3s cubic-bezier(.34,1.56,.64,1);}}
@keyframes popIn{{from{{opacity:0;transform:scale(.7);}}to{{opacity:1;transform:scale(1);}}}}
.pill-tyfcb{{background:rgba(39,174,96,.2);border:2px solid #27ae60;color:#4ade80;}}
.pill-ref{{background:rgba(200,16,46,.2);border:2px solid #C8102E;color:#f87171;}}
.pill-test{{background:rgba(142,68,173,.2);border:2px solid #8e44ad;color:#c084fc;}}
.pill-name{{background:rgba(26,86,219,.2);border:2px solid #1a56db;color:#60a5fa;}}
.transcript-wrap{{background:#111827;border-radius:10px;padding:8px 12px;margin-bottom:10px;border:1px solid #1f2937;}}
.transcript-hdr{{font-size:.68em;color:#6b7280;font-weight:700;letter-spacing:.5px;margin-bottom:4px;}}
.transcript-body{{font-family:monospace;font-size:.8em;color:#93c5fd;white-space:pre-wrap;max-height:100px;overflow-y:auto;line-height:1.6;}}
.t-final{{color:#e2e8f0;}}.t-interim{{color:#6b7280;font-style:italic;}}
.t-speaker{{color:#60a5fa;font-weight:700;}}.t-tyfcb{{color:#4ade80;font-weight:700;}}
.t-ref{{color:#f87171;font-weight:700;}}.t-test{{color:#c084fc;font-weight:700;}}
.action-prompt{{background:#1f2937;border-radius:10px;padding:10px 14px;margin-bottom:10px;border:1px solid #374151;display:none;}}
.action-prompt.visible{{display:block;animation:slideIn .25s ease;}}
@keyframes slideIn{{from{{opacity:0;transform:translateY(-6px);}}to{{opacity:1;transform:translateY(0);}}}}
.action-prompt-title{{font-size:.8em;color:#9ca3af;margin-bottom:8px;}}
.action-prompt strong{{color:#f9fafb;font-size:.92em;}}
.action-btns{{display:flex;gap:6px;flex-wrap:wrap;}}
.act-btn{{border:none;border-radius:8px;padding:7px 12px;font-size:.8em;font-weight:700;cursor:pointer;transition:all .18s;}}
.act-btn:hover{{transform:translateY(-1px);opacity:.9;}}
.act-tyfcb{{background:linear-gradient(135deg,#27ae60,#1e8449);color:white;}}
.act-ref{{background:linear-gradient(135deg,#C8102E,#8b0000);color:white;}}
.act-test{{background:linear-gradient(135deg,#8e44ad,#6c3483);color:white;}}
.act-cancel{{background:#374151;color:#9ca3af;}}
.members-section{{margin-bottom:10px;}}
.members-hdr{{font-size:.78em;color:#9ca3af;font-weight:700;letter-spacing:.5px;margin-bottom:8px;}}
.members-grid{{display:grid;grid-template-columns:repeat(auto-fill,minmax(120px,1fr));gap:7px;}}
.member-card{{background:#111827;border:2px solid #1f2937;border-radius:10px;padding:9px 7px;text-align:center;cursor:pointer;transition:all .22s;position:relative;}}
.member-card:hover{{transform:translateY(-2px);box-shadow:0 6px 18px rgba(0,0,0,.4);border-color:#374151;}}
.member-card.speaking{{border-color:#60a5fa;background:#1e2d4a;box-shadow:0 0 0 3px rgba(96,165,250,.35);animation:cardPulse .8s infinite;}}
.member-card.just-scored{{animation:scoreFlash .6s ease;}}
@keyframes cardPulse{{0%,100%{{box-shadow:0 0 0 3px rgba(96,165,250,.35);}}50%{{box-shadow:0 0 0 6px rgba(96,165,250,.1);}}}}
@keyframes scoreFlash{{0%{{background:#1f2937;}}30%{{background:#1c3a2a;border-color:#27ae60;}}100%{{background:#111827;}}}}
.member-avatar{{width:36px;height:36px;border-radius:50%;margin:0 auto 5px;display:flex;align-items:center;justify-content:center;font-weight:800;font-size:.85em;background:linear-gradient(135deg,#C8102E,#8b0000);color:white;}}
.member-card.speaking .member-avatar{{background:linear-gradient(135deg,#1a56db,#1e3a8a);}}
.member-nm{{font-size:.73em;font-weight:700;color:#f3f4f6;margin-bottom:3px;white-space:nowrap;overflow:hidden;text-overflow:ellipsis;}}
.member-sub{{font-size:.62em;color:#6b7280;margin-bottom:3px;white-space:nowrap;overflow:hidden;text-overflow:ellipsis;}}
.member-badges{{display:flex;justify-content:center;gap:3px;flex-wrap:wrap;min-height:16px;}}
.mbadge{{border-radius:8px;padding:1px 5px;font-size:.62em;font-weight:800;}}
.mb-t{{background:#27ae60;color:white;}}.mb-r{{background:#C8102E;color:white;}}.mb-s{{background:#8e44ad;color:white;}}
.member-total{{position:absolute;top:4px;right:6px;font-size:.62em;font-weight:800;color:#60a5fa;opacity:.8;}}
.speaking-wave{{position:absolute;bottom:4px;left:50%;transform:translateX(-50%);display:none;gap:2px;}}
.member-card.speaking .speaking-wave{{display:flex;}}
.sw{{width:3px;border-radius:2px;background:#60a5fa;animation:wave .7s infinite ease-in-out;}}
.sw:nth-child(1){{height:5px;animation-delay:0s;}}.sw:nth-child(2){{height:10px;animation-delay:.15s;}}.sw:nth-child(3){{height:7px;animation-delay:.3s;}}.sw:nth-child(4){{height:12px;animation-delay:.1s;}}.sw:nth-child(5){{height:4px;animation-delay:.25s;}}
@keyframes wave{{0%,100%{{transform:scaleY(.4);}}50%{{transform:scaleY(1);}}}}
.add-member-row{{display:flex;gap:6px;margin-bottom:10px;}}
.add-member-inp{{flex:1;background:#1f2937;border:1.5px solid #374151;border-radius:8px;padding:7px 10px;color:#f3f4f6;font-size:.82em;outline:none;}}
.add-member-inp:focus{{border-color:#1a56db;}}.add-member-inp::placeholder{{color:#6b7280;}}
.add-member-btn{{background:#1a56db;color:white;border:none;border-radius:8px;padding:7px 12px;font-size:.82em;font-weight:700;cursor:pointer;}}
.controls{{display:flex;gap:8px;margin-bottom:10px;}}
.ctrl-btn{{flex:1;border:none;border-radius:10px;padding:12px 0;font-size:.88em;font-weight:700;cursor:pointer;transition:all .2s;}}
.ctrl-btn:hover{{transform:translateY(-2px);opacity:.9;}}.ctrl-btn:disabled{{opacity:.4;cursor:not-allowed;transform:none;}}
.btn-start{{background:linear-gradient(135deg,#27ae60,#1e8449);color:white;}}
.btn-pause{{background:linear-gradient(135deg,#374151,#1f2937);color:#9ca3af;border:1.5px solid #374151;}}
.btn-pause.active{{background:linear-gradient(135deg,#f59e0b,#d97706);color:white;border:none;}}
.btn-end{{background:linear-gradient(135deg,#C8102E,#8b0000);color:white;}}
.toast{{position:fixed;bottom:16px;left:50%;transform:translateX(-50%) translateY(100px);background:#111827;border:1.5px solid #374151;border-radius:10px;padding:8px 18px;font-size:.82em;color:#f3f4f6;z-index:9999;transition:transform .35s cubic-bezier(.34,1.56,.64,1);pointer-events:none;white-space:nowrap;}}
.toast.show{{transform:translateX(-50%) translateY(0);}}
.help-bar{{background:rgba(26,86,219,.06);border:1px solid rgba(26,86,219,.15);border-radius:8px;padding:8px 12px;font-size:.75em;color:#6b7280;line-height:1.7;margin-top:6px;}}
.help-bar .kw-t{{color:#4ade80;}}.help-bar .kw-r{{color:#f87171;}}.help-bar .kw-s{{color:#c084fc;}}
</style></head><body>
<div class="top-bar">
  <div class="bni-badge">BNI</div>
  <div><div class="meeting-title">Leaders FTL &mdash; Meeting Recorder</div><div class="meeting-date">&#128197; {today_str} &nbsp;&#183;&nbsp; {day_of_week}</div></div>
  <div style="display:flex;align-items:center;gap:8px;margin-left:auto;"><div class="rec-dot" id="recDot"></div><span class="timer" id="timer">0:00</span></div>
</div>
<div class="score-totals">
  <div class="total-pill tp-t"><div class="num" id="totalT">0</div><div class="lbl">&#127881; TYFCB</div></div>
  <div class="total-pill tp-r"><div class="num" id="totalR">0</div><div class="lbl">&#128279; Referrals</div></div>
  <div class="total-pill tp-s"><div class="num" id="totalS">0</div><div class="lbl">&#11088; Testimonials</div></div>
</div>
<div class="detected-wrap" id="detectedWrap">
  <span class="detected-label">DETECTED</span>
  <span id="detectedPills" style="color:#6b7280;font-size:.82em;">Waiting for speech...</span>
</div>
<div class="action-prompt" id="actionPrompt">
  <div class="action-prompt-title">Detected: <strong id="promptSpeaker"></strong> &mdash; What are they reporting?</div>
  <div class="action-btns">
    <button class="act-btn act-tyfcb" onclick="confirmActivity('tyfcb')">&#127881; Thank You for Closed Business</button>
    <button class="act-btn act-ref" onclick="confirmActivity('referral')">&#128279; Referral Passed</button>
    <button class="act-btn act-test" onclick="confirmActivity('testimonial')">&#11088; Testimonial</button>
    <button class="act-btn act-cancel" onclick="dismissPrompt()">&#215; Dismiss</button>
  </div>
</div>
<div class="transcript-wrap">
  <div class="transcript-hdr">&#128250; LIVE TRANSCRIPT</div>
  <div class="transcript-body" id="transcriptBox">Press Start Recording. Chrome recommended for best speech recognition.</div>
</div>
<div class="controls">
  <button class="ctrl-btn btn-start" id="btnStart" onclick="startRec()">&#9654; Start Recording</button>
  <button class="ctrl-btn btn-pause" id="btnPause" onclick="togglePause()" disabled>&#9646;&#9646; Pause</button>
  <button class="ctrl-btn btn-end" id="btnEnd" onclick="endMeeting()">&#128231; End &amp; Send Report</button>
</div>
<div class="members-section">
  <div class="members-hdr">&#128101; BNI LEADERS FTL MEMBERS &mdash; <span style="color:#4ade80;font-size:.85em;font-weight:400;">Tap card to manually log activity</span></div>
  <div class="members-grid" id="membersGrid"></div>
</div>
<div class="add-member-row">
  <input class="add-member-inp" id="addInp" placeholder="Add member name..." onkeydown="if(event.key==='Enter')addMember()">
  <button class="add-member-btn" onclick="addMember()">+ Add</button>
</div>
<div class="help-bar">
  &#9679; Use <strong style="color:#f9fafb;">Chrome</strong> for best speech recognition &nbsp;&#9679;&nbsp; Say member's <strong style="color:#f9fafb;">first + last name</strong> then their activity<br>
  &#9679; Auto-keywords: <span class="kw-t">TYFCB / closed business / thank you for closed</span> &middot; <span class="kw-r">referral / passing / referred</span> &middot; <span class="kw-s">testimonial / recognize / shout out</span><br>
  &#9679; Tap any member card to log manually &mdash; no speech required
</div>
<div class="toast" id="toast"></div>
<script>
var MEMBERS={members_js};
var tally={{}};var fullTranscript="";var recognition=null;var timerInterval=null;var elapsed=0;
var isRecording=false;var isPaused=false;var currentSpeaker=null;var pendingSpeaker=null;var pendingText="";
var KW_TYFCB=["thank you for closed business","tyfcb","closed business","closed the deal","thank you for the closed","closed deal","business closed","tyfcob","ty for closed","thank you closed"];
var KW_REF=["referral","pass a referral","passing a referral","referred","i have a referral","i'm passing","i am passing","giving a referral","pass referral","passing referral","i want to pass","i'd like to pass","have a referral","give a referral"];
var KW_TEST=["testimonial","give a testimonial","giving a testimonial","would like to recognize","want to recognize","shout out","shoutout","recognize","i want to give","i'd like to give a testimonial","give testimonial"];
function detectActivity(t){{var s=t.toLowerCase();for(var i=0;i<KW_TYFCB.length;i++)if(s.indexOf(KW_TYFCB[i])>-1)return"tyfcb";for(var i=0;i<KW_REF.length;i++)if(s.indexOf(KW_REF[i])>-1)return"referral";for(var i=0;i<KW_TEST.length;i++)if(s.indexOf(KW_TEST[i])>-1)return"testimonial";return null;}}
function detectMember(t){{var s=t.toLowerCase();var best=null,bestScore=0;for(var i=0;i<MEMBERS.length;i++){{var parts=MEMBERS[i].toLowerCase().split(" ");var score=0;for(var j=0;j<parts.length;j++)if(parts[j].length>2&&s.indexOf(parts[j])>-1)score+=parts[j].length;if(score>bestScore){{bestScore=score;best=MEMBERS[i];}}}}return bestScore>=3?best:null;}}
function initTally(){{tally={{}};MEMBERS.forEach(function(m){{tally[m]={{tyfcb:0,referral:0,testimonial:0,notes:""}};}}); }}
function initGrid(){{
  var grid=document.getElementById("membersGrid");grid.innerHTML="";
  MEMBERS.forEach(function(m){{
    var initials=m.split(" ").map(function(w){{return w[0];}}).join("").substring(0,2).toUpperCase();
    var firstName=m.split(" ")[0];var lastName=m.split(" ").slice(1).join(" ");
    var card=document.createElement("div");card.className="member-card";card.id="card-"+m.replace(/\s+/g,"_");
    card.innerHTML='<div class="member-total" id="total-'+m.replace(/\s+/g,"_")+'"></div>'+
      '<div class="member-avatar" id="av-'+m.replace(/\s+/g,"_")+'">'+initials+'</div>'+
      '<div class="member-nm">'+firstName+'</div><div class="member-sub">'+lastName+'</div>'+
      '<div class="member-badges" id="badges-'+m.replace(/\s+/g,"_")+'"></div>'+
      '<div class="speaking-wave"><div class="sw"></div><div class="sw"></div><div class="sw"></div><div class="sw"></div><div class="sw"></div></div>';
    card.onclick=(function(name){{return function(){{pendingSpeaker=name;currentSpeaker=name;showPrompt(name,"");}};}})(m);
    grid.appendChild(card);
  }});
}}
function updateCard(name){{
  var key=name.replace(/\s+/g,"_");var d=tally[name];if(!d)return;
  var total=d.tyfcb+d.referral+d.testimonial;
  var te=document.getElementById("total-"+key);if(te)te.textContent=total||"";
  var bg=document.getElementById("badges-"+key);if(!bg)return;
  var html="";
  if(d.tyfcb>0)html+='<span class="mbadge mb-t">T'+d.tyfcb+'</span>';
  if(d.referral>0)html+='<span class="mbadge mb-r">R'+d.referral+'</span>';
  if(d.testimonial>0)html+='<span class="mbadge mb-s">S'+d.testimonial+'</span>';
  bg.innerHTML=html;
  var card=document.getElementById("card-"+key);
  if(card){{card.classList.add("just-scored");setTimeout(function(){{card.classList.remove("just-scored");}},650);}}
  updateTotals();
}}
function updateTotals(){{var t=0,r=0,s=0;Object.keys(tally).forEach(function(k){{t+=tally[k].tyfcb||0;r+=tally[k].referral||0;s+=tally[k].testimonial||0;}});document.getElementById("totalT").textContent=t;document.getElementById("totalR").textContent=r;document.getElementById("totalS").textContent=s;}}
function setSpeaking(name){{MEMBERS.forEach(function(m){{var c=document.getElementById("card-"+m.replace(/\s+/g,"_"));if(c)c.classList.remove("speaking");}});if(name){{var c=document.getElementById("card-"+name.replace(/\s+/g,"_"));if(c)c.classList.add("speaking");}}}}
function showPrompt(name,text){{pendingSpeaker=name;document.getElementById("promptSpeaker").textContent=name;document.getElementById("actionPrompt").classList.add("visible");}}
function dismissPrompt(){{document.getElementById("actionPrompt").classList.remove("visible");pendingSpeaker=null;}}
function confirmActivity(type){{if(!pendingSpeaker)return;addScore(pendingSpeaker,type,pendingText);dismissPrompt();}}
function addScore(name,type,text){{
  if(!tally[name])tally[name]={{tyfcb:0,referral:0,testimonial:0,notes:""}};
  tally[name][type]++;if(text)tally[name].notes+=text.substring(0,50)+"... ";
  updateCard(name);
  var emoji=type==="tyfcb"?"&#127881; TYFCB":type==="referral"?"&#128279; Referral":"&#11088; Testimonial";
  showToast("&#127942; "+name.split(" ")[0]+" &mdash; "+emoji+" logged!");
  appendTranscript(name,"["+type.toUpperCase()+" LOGGED]","action");
  updateDetected(name,type);
}}
function updateDetected(name,type){{var pills=document.getElementById("detectedPills");var cls=type==="tyfcb"?"pill-tyfcb":type==="referral"?"pill-ref":"pill-test";var lbl=type==="tyfcb"?"&#127881; TYFCB":type==="referral"?"&#128279; Referral":"&#11088; Testimonial";pills.innerHTML='<span class="detected-pill pill-name">&#127908; '+name+'</span>&nbsp;<span class="detected-pill '+cls+'">'+lbl+'</span>';}}
function appendTranscript(speaker,text,type){{var box=document.getElementById("transcriptBox");if(box.textContent.indexOf("Press Start")>-1||box.textContent.indexOf("Waiting")>-1)box.innerHTML="";var line=document.createElement("div");var cls=type==="action"?"t-action":"t-final";if(type==="tyfcb")cls="t-tyfcb";if(type==="referral")cls="t-ref";if(type==="testimonial")cls="t-test";line.innerHTML='<span class="t-speaker">'+(speaker||"?")+':</span> <span class="'+cls+'">'+text+'</span>';box.appendChild(line);box.scrollTop=box.scrollHeight;fullTranscript+=(speaker||"?")+": "+text+"\n";}}
function setInterim(speaker,text){{var box=document.getElementById("transcriptBox");var ex=box.querySelector(".t-interim-line");if(ex)ex.remove();if(!text)return;var line=document.createElement("div");line.className="t-interim-line";line.innerHTML='<span class="t-speaker">'+(speaker||"...")+':</span> <span class="t-interim">'+text+'</span>';box.appendChild(line);box.scrollTop=box.scrollHeight;}}
function fmt(s){{return Math.floor(s/60)+":"+(s%60<10?"0":"")+s%60;}}
function startRec(){{isRecording=true;isPaused=false;document.getElementById("recDot").classList.add("live");document.getElementById("btnStart").disabled=true;document.getElementById("btnPause").disabled=false;document.getElementById("btnPause").classList.add("active");document.getElementById("btnPause").textContent="\u23F8 Pause";timerInterval=setInterval(function(){{elapsed++;document.getElementById("timer").textContent=fmt(elapsed);}},1000);startSR();document.getElementById("detectedPills").innerHTML='<span style="color:#4ade80;font-size:.82em;">&#9679; Recording live &mdash; speak naturally</span>';}}
function startSR(){{var SR=window.SpeechRecognition||window.webkitSpeechRecognition;if(!SR){{document.getElementById("transcriptBox").textContent="Speech recognition needs Chrome. Use member cards below to log manually.";return;}}recognition=new SR();recognition.continuous=true;recognition.interimResults=true;recognition.lang="en-US";recognition.onresult=function(e){{var interim="";for(var i=e.resultIndex;i<e.results.length;i++){{var txt=e.results[i][0].transcript.trim();if(e.results[i].isFinal){{var spk=detectMember(txt);var act=detectActivity(txt);if(spk){{currentSpeaker=spk;setSpeaking(spk);}}if(act&&currentSpeaker){{pendingSpeaker=currentSpeaker;pendingText=txt;addScore(currentSpeaker,act,txt);}}else if(spk&&!act){{pendingSpeaker=spk;pendingText=txt;showPrompt(spk,txt);}}appendTranscript(currentSpeaker||"Unknown",txt,"final");setInterim(null,"");}}else{{interim=txt;}}}}if(interim)setInterim(currentSpeaker||"...",interim);}};recognition.onerror=function(err){{if(err.error!=="no-speech")document.getElementById("detectedPills").innerHTML='<span style="color:#f87171;">Mic error: '+err.error+'. Check permissions.</span>';}};recognition.onend=function(){{if(isRecording&&!isPaused)recognition.start();}};recognition.start();}}
function togglePause(){{if(!isRecording)return;if(!isPaused){{isPaused=true;if(recognition){{try{{recognition.stop();}}catch(e){{}}}}clearInterval(timerInterval);document.getElementById("recDot").classList.remove("live");document.getElementById("btnPause").textContent="\u25B6 Resume";document.getElementById("btnPause").classList.remove("active");setSpeaking(null);showToast("Recording paused");}}else{{isPaused=false;document.getElementById("recDot").classList.add("live");document.getElementById("btnPause").textContent="\u23F8 Pause";document.getElementById("btnPause").classList.add("active");timerInterval=setInterval(function(){{elapsed++;document.getElementById("timer").textContent=fmt(elapsed);}},1000);startSR();showToast("Recording resumed");}}}}
function addMember(){{var inp=document.getElementById("addInp");var name=inp.value.trim();if(!name||MEMBERS.indexOf(name)>-1){{inp.value="";return;}}MEMBERS.push(name);tally[name]={{tyfcb:0,referral:0,testimonial:0,notes:""}};inp.value="";initGrid();showToast("Added: "+name);}}
function showToast(msg){{var t=document.getElementById("toast");t.innerHTML=msg;t.classList.add("show");setTimeout(function(){{t.classList.remove("show");}},2800);}}
function endMeeting(){{if(isRecording){{isRecording=false;isPaused=false;clearInterval(timerInterval);}}if(recognition){{try{{recognition.stop();}}catch(e){{}}recognition=null;}}document.getElementById("recDot").classList.remove("live");document.getElementById("btnStart").disabled=false;document.getElementById("btnPause").disabled=true;setSpeaking(null);var tallyArr=MEMBERS.map(function(m){{var d=tally[m]||{{tyfcb:0,referral:0,testimonial:0,notes:""}};return{{name:m,tyfcb:d.tyfcb,referral:d.referral,testimonial:d.testimonial,notes:d.notes}};}}).filter(function(r){{return r.tyfcb+r.referral+r.testimonial>0;}});var payload=JSON.stringify({{tally:tallyArr,transcript:fullTranscript,duration:fmt(elapsed)}});try{{sessionStorage.setItem("bni_report",payload);}}catch(e){{}}window.parent.postMessage({{type:"bni_end",payload:payload}},"*");document.getElementById("btnEnd").textContent="\u2714 Meeting Ended &mdash; Click Send Below";document.getElementById("btnEnd").style.background="linear-gradient(135deg,#27ae60,#1e8449)";showToast("&#128231; Done! Click Send Report below.");}}
initTally();initGrid();
</script></body></html>
""", height=920, scrolling=True)

    st.markdown("---")
    st.markdown("""
    <div style='background:linear-gradient(135deg,#0a0e1a,#111827);border-radius:14px;padding:18px 22px;border:1.5px solid #1f2937;margin-bottom:12px;'>
      <h3 style='color:#f9fafb !important;margin:0 0 6px;font-size:1.05em;border:none !important;'>&#128231; Send Meeting Report</h3>
      <p style='color:#9ca3af;font-size:.84em;margin:0;'>After pressing <strong style='color:#60a5fa;'>End &amp; Send Report</strong> above, click below to email the full scorecard instantly.</p>
    </div>
    """, unsafe_allow_html=True)
    col_d, col_b = st.columns([3,2])
    with col_d:
        report_date = st.text_input("Meeting Date", value=today_str, key="rdate", label_visibility="collapsed")
    with col_b:
        send_now = st.button("U0001f4e8 Send Report Now", key="send_rpt")
    if send_now:
        try:
            gu = st.secrets["GMAIL_USER"]
            gp = st.secrets["GMAIL_APP_PASSWORD"]
            ok, info = send_meeting_report(report_date, [], "(Transcript captured live in recorder above)", gu, gp)
            if ok:
                st.markdown(f"""<div style='background:rgba(39,174,96,.1);border:1.5px solid #27ae60;border-radius:10px;padding:14px 18px;text-align:center;color:#4ade80;font-weight:700;'>&#127881; Report sent to: {", ".join(info)}</div>""", unsafe_allow_html=True)
            else:
                st.error(f"Could not send: {info}")
        except KeyError:
            st.warning("U0001f512 Add GMAIL_USER, GMAIL_APP_PASSWORD, and REPORT_EMAIL in Streamlit Cloud Secrets.")
        except Exception as e:
            st.error(f"Error: {e}")
    st.markdown("""
    <div style='background:rgba(26,86,219,.05);border:1px solid rgba(26,86,219,.15);border-radius:10px;padding:10px 14px;margin-top:8px;font-size:.78em;color:#6b7280;line-height:1.7;'>
      <strong style='color:#9ca3af;'>&#128161; Tips:</strong><br>
      &#9679; Use <strong style='color:#f9fafb;'>Chrome</strong> on desktop for the best speech recognition.<br>
      &#9679; Say member's <strong style='color:#f9fafb;'>first and last name</strong> before their activity.<br>
      &#9679; Or tap any member card to log manually.
    </div>
    """, unsafe_allow_html=True)
    st.markdown("""<div class='footer-bar'>&#128274; BNI Leaders FTL Chapter Hub &nbsp;|&nbsp; Powered by <a href='https://mrceesai.com'>MrCeesAI</a> &mdash; Austin Jones</div>""", unsafe_allow_html=True)
