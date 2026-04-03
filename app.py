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
    page_title="BNI Leaders FTL",
    page_icon="\U0001f91d",
    layout="centered"
)

if "page" not in st.session_state:
    st.session_state["page"] = "landing"

st.markdown("""
<style>
@keyframes fadeInDown { from{opacity:0;transform:translateY(-16px);}to{opacity:1;transform:translateY(0);} }
@keyframes fadeInUp   { from{opacity:0;transform:translateY(16px);}to{opacity:1;transform:translateY(0);} }
@keyframes pulse { 0%,100%{box-shadow:0 0 0 0 rgba(200,16,46,.28);}50%{box-shadow:0 0 0 8px rgba(200,16,46,0);} }
[data-testid="stAppViewContainer"]{background:#fff;}
.hero-wrap{animation:fadeInDown .7s ease both;}
.stButton>button{
  background:linear-gradient(135deg,#C8102E 0%,#a00d24 100%) !important;
  color:white !important;font-weight:700 !important;border-radius:8px !important;
  padding:.7em 2em !important;font-size:1.05em !important;width:100% !important;
  border:none !important;margin-top:8px !important;
  animation:pulse 2.4s infinite !important;transition:transform .12s,opacity .12s !important;
}
.stButton>button:hover{transform:translateY(-2px) !important;opacity:.93 !important;}
.land-card{border-radius:16px;padding:2em 1.4em;text-align:center;background:#fff;
  box-shadow:0 6px 28px rgba(0,0,0,.09);border:2.5px solid transparent;
  animation:fadeInUp .8s ease both;transition:transform .22s,box-shadow .22s;}
.land-card:hover{transform:translateY(-5px);box-shadow:0 14px 40px rgba(0,0,0,.13);}
.land-visitor{border-color:#C8102E !important;}
.land-member{border-color:#1a56db !important;}
.intro-box{background:#fff5f5;border-left:5px solid #C8102E;padding:1em 1.5em;
  border-radius:0 8px 8px 0;margin-bottom:1em;animation:fadeInDown .9s ease both;}
.tip-box{background:linear-gradient(135deg,#fffbf0,#fff8e1);border-left:4px solid #f39c12;
  border-radius:0 8px 8px 0;padding:.9em 1.2em;margin:.5em 0 1.2em;font-size:.97em;}
.success-card{background:linear-gradient(135deg,#f0fff4,#e8f8ee);border:1.5px solid #27ae60;
  border-radius:12px;padding:1.5em;margin-top:1em;animation:fadeInDown .6s ease both;}
h2{color:#C8102E !important;border-bottom:2px solid #f0f0f0;padding-bottom:6px;}
div[data-testid="stTabs"] button[data-baseweb="tab"]{font-size:1.05em !important;font-weight:600 !important;padding:10px 24px !important;}
.footer-bar{text-align:center;margin-top:2em;padding:1em;background:#f8f9fa;border-radius:10px;font-size:.85em;color:#888;}
</style>
""", unsafe_allow_html=True)

st.markdown("""
<div class='hero-wrap' style='text-align:center;padding:10px 0 4px;'>
  <div style='display:inline-block;background:linear-gradient(135deg,#C8102E 0%,#8b0000 100%);
       color:white;font-size:1.6em;font-weight:900;padding:8px 28px;border-radius:10px;
       letter-spacing:3px;font-family:Arial,sans-serif;box-shadow:0 4px 16px rgba(200,16,46,.35);'>BNI Leaders FTL</div>
  <h2 style='color:#C8102E;margin:8px 0 2px;font-size:1.3em;font-weight:600;letter-spacing:1px;border:none !important;'>Chapter Hub</h2>
  <p style='color:#888;margin:0;font-size:.95em;'>Business Network International &mdash; Where Referrals Are Our Business</p>
</div>
""", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════
# LANDING PAGE
# ══════════════════════════════════════════════════════
if st.session_state["page"] == "landing":
    st.markdown("<div style='text-align:center;margin:1.2em 0 1.8em;'><p style='font-size:1.1em;color:#555;max-width:520px;margin:0 auto;'>Welcome! Choose your role to get started.</p></div>", unsafe_allow_html=True)
    col_a, col_b = st.columns(2, gap="large")
    with col_a:
        st.markdown("""
        <div class='land-card land-visitor'>
          <div style='font-size:3.2em;margin-bottom:.3em;'>&#128075;</div>
          <h2 style='color:#C8102E !important;border:none !important;margin:0 0 .5em;font-size:1.35em;'>Visitor Sign-In</h2>
          <p style='color:#666;font-size:.93em;margin-bottom:1.2em;'>Attending BNI today as a guest? Sign in here and connect with our members!</p>
          <div style='background:#C8102E;color:white;border-radius:8px;padding:9px 0;font-weight:700;font-size:.95em;'>&#128204;&nbsp; Guest Sign-In Form</div>
        </div>""", unsafe_allow_html=True)
        if st.button("Enter as Visitor", key="btn_v"):
            st.session_state["page"] = "visitor"
            st.rerun()
    with col_b:
        st.markdown("""
        <div class='land-card land-member'>
          <div style='font-size:3.2em;margin-bottom:.3em;'>&#127908;</div>
          <h2 style='color:#1a56db !important;border:none !important;margin:0 0 .5em;font-size:1.35em;'>Meeting Recorder</h2>
          <p style='color:#666;font-size:.93em;margin-bottom:1.2em;'>BNI member? Launch the live scoreboard recorder — tracks TYFCB, referrals &amp; testimonials in real time.</p>
          <div style='background:#1a56db;color:white;border-radius:8px;padding:9px 0;font-weight:700;font-size:.95em;'>&#127908;&nbsp; Open Meeting Recorder</div>
        </div>""", unsafe_allow_html=True)
        if st.button("Open Meeting Recorder", key="btn_m"):
            st.session_state["page"] = "recorder"
            st.rerun()
    st.markdown("<div class='footer-bar'>&#128274; Info stored securely in your chapter's Google Sheet.&nbsp;|&nbsp; Powered by <a href='https://mrceesai.com' style='color:#C8102E;'>MrCeesAI</a> &mdash; Austin Jones</div>", unsafe_allow_html=True)


# ══════════════════════════════════════════════════════
# VISITOR PAGE
# ══════════════════════════════════════════════════════
elif st.session_state["page"] == "visitor":
    if st.button("\u2190 Back to Home", key="back_v"):
        st.session_state["page"] = "landing"
        st.rerun()

    def send_visitor_welcome(fn, ve, bn, il, gu, gp):
        try:
            msg = MIMEMultipart("alternative")
            msg["Subject"] = f"Great connecting with you at BNI, {fn}!"
            msg["From"] = gu
            msg["To"] = ve
            html = f"""<div style="font-family:Arial,sans-serif;max-width:600px;margin:auto;">
              <div style="background:linear-gradient(135deg,#C8102E,#8b0000);color:white;padding:20px 24px;border-radius:10px 10px 0 0;">
                <div style="font-size:1.8em;font-weight:900;letter-spacing:3px;">BNI Leaders FTL</div>
                <h2 style="margin:8px 0 0;color:white !important;">Thanks for Visiting, {fn}!</h2>
              </div>
              <div style="background:#f9f9f9;padding:24px;border-radius:0 0 10px 10px;">
                <p>Hi {fn}, thank you for joining us at BNI! A chapter member will reach out shortly.</p>
                <p><strong>Business:</strong> {bn} &mdash; <strong>Interest:</strong> {il}</p>
                <p>We hope to see you again next week!</p>
                <p style="font-size:.85em;color:#888;">Need AI automation? <a href="https://mrceesai.com" style="color:#C8102E;">MrCeesAI by Austin Jones</a></p>
              </div></div>"""
            msg.attach(MIMEText(html, "html"))
            with smtplib.SMTP_SSL("smtp.gmail.com", 465) as s:
                s.login(gu, gp); s.sendmail(gu, ve, msg.as_string())
            return True
        except Exception: return False

    def send_hot_lead(fn, ln, ve, ph, bn, ind, ep, il, gu, gp, re_):
        try:
            msg = MIMEMultipart("alternative")
            msg["Subject"] = f"BNI HOT LEAD \u2014 {fn} {ln} ({bn})"
            msg["From"] = gu; msg["To"] = re_
            html = f"""<div style="font-family:Arial,sans-serif;max-width:600px;margin:auto;">
              <div style="background:#27ae60;color:white;padding:16px 24px;border-radius:10px 10px 0 0;">
                <h2 style="margin:0;color:white !important;">&#128293; HOT BNI LEAD &mdash; {il}</h2></div>
              <div style="background:#f0fff4;padding:24px;border-radius:0 0 10px 10px;border:2px solid #27ae60;">
                <p><strong>{fn} {ln}</strong> &mdash; {bn} ({ind})</p>
                <p>Email: <a href="mailto:{ve}">{ve}</a> | Phone: {ph or "N/A"}</p>
                <p><em>"{ep}"</em></p>
                <p style="color:#27ae60;font-weight:700;">Reach out NOW!</p></div></div>"""
            msg.attach(MIMEText(html, "html"))
            with smtplib.SMTP_SSL("smtp.gmail.com", 465) as s:
                s.login(gu, gp); s.sendmail(gu, re_, msg.as_string())
            return True
        except Exception: return False

    BNI_TIPS = [
        "&#128161; <strong>BNI Tip:</strong> The most successful members give referrals before expecting to receive them.",
        "&#128161; <strong>BNI Tip:</strong> Your 60-second pitch should be crystal-clear &mdash; the easier to refer you, the more referrals you get!",
        "&#128161; <strong>BNI Tip:</strong> BNI members generate an average of $50,000+ in new business per year.",
        "&#128161; <strong>BNI Tip:</strong> Givers Gain&#174; &mdash; members who give the most referrals receive the most in return.",
        "&#128161; <strong>BNI Tip:</strong> Each member holds one seat &mdash; securing yours locks out competitors!",
        "&#128161; <strong>BNI Tip:</strong> 1-2-1 meetings are the #1 driver of strong referral relationships.",
        "&#128161; <strong>BNI Tip:</strong> The average BNI chapter passes over $1 million in referrals each year.",
    ]
    st.markdown(f"""<div class='intro-box'><strong>Thanks for visiting today!</strong> Take 2 minutes to fill out this quick form and our members will follow up to help grow your business.</div>
    <div class='tip-box'>{random.choice(BNI_TIPS)}</div>""", unsafe_allow_html=True)

    with st.form("visitor_form", clear_on_submit=True):
        st.markdown("## Contact Information")
        c1, c2 = st.columns(2)
        with c1:
            first_name = st.text_input("First Name *", placeholder="Jane")
            email      = st.text_input("Email Address *", placeholder="jane@example.com")
            phone      = st.text_input("Phone Number", placeholder="(555) 555-5555")
        with c2:
            last_name  = st.text_input("Last Name *", placeholder="Smith")
            city       = st.text_input("City / Area", placeholder="Fort Lauderdale, FL")
            website    = st.text_input("Website", placeholder="www.yoursite.com")
        st.markdown("## Social Media")
        c3, c4 = st.columns(2)
        with c3:
            linkedin  = st.text_input("LinkedIn", placeholder="linkedin.com/in/yourname")
            instagram = st.text_input("Instagram", placeholder="@yourhandle")
        with c4:
            facebook  = st.text_input("Facebook", placeholder="facebook.com/yourpage")
            twitter_x = st.text_input("X / Twitter", placeholder="@yourhandle")
        st.markdown("## Your Business")
        business_name = st.text_input("Business Name *", placeholder="Smith Consulting LLC")
        industry = st.selectbox("Industry / Profession *", [
            "Select one...","Accounting / Finance","Attorney / Legal","Banking / Lending",
            "Chiropractor / Health","Construction / Contracting","Consulting / Coaching",
            "Digital Marketing","Financial Planning","Health & Wellness","Home Services / Remodeling",
            "HR / Staffing","Insurance","IT / Technology / Cybersecurity","Mortgage / Real Estate",
            "Photography / Videography","Printing / Signage / Design","Restaurant / Catering / Food",
            "Retail / E-Commerce","Travel / Hospitality","Other"])
        other_industry = ""
        if industry == "Other":
            other_industry = st.text_input("Please describe your profession *")
        elevator_pitch = st.text_area("In one sentence: what do you do and who do you help? *",
            placeholder="e.g. I help small business owners protect assets with affordable insurance plans.", height=80)
        years_in_biz = st.select_slider("How long have you been in business?",
            options=["Less than 1 year","1-2 years","3-5 years","6-10 years","10+ years"])
        st.markdown("## Networking & Referrals")
        c5, c6 = st.columns(2)
        with c5:
            ideal_referral = st.text_area("What does your ideal referral look like?",
                placeholder="e.g. A homeowner aged 35-55 who recently bought a house...", height=90)
        with c6:
            top_clients = st.text_area("Top 3 types of clients / industries you serve?",
                placeholder="e.g. Real estate agents, small business owners, HR managers...", height=90)
        how_heard  = st.selectbox("How did you hear about our chapter?", [
            "Select one...","Invited by a member","BNI website / Find a Chapter",
            "Social media","Google search","Friend / colleague","Attended before","Other"])
        invited_by = st.text_input("If invited by a member — who invited you?", placeholder="Member name")
        st.markdown("## Goals & Interest Level")
        looking_for = st.multiselect("What are you hoping to get from BNI?", [
            "More qualified referrals","Grow my professional network","Business accountability",
            "Learn from other business owners","Give referrals to others","Greater brand visibility",
            "Find trusted vendors & partners","Structured networking system"])
        has_bni_before = st.radio("Have you visited or been a BNI member before?",
            ["No — first time!","Visited before but never joined","Former BNI member"], horizontal=True)
        biggest_challenge = st.text_area("What is your biggest business challenge right now?",
            placeholder="e.g. Generating consistent leads...", height=80)
        ready_to_join = st.select_slider("How interested are you in joining our chapter?",
            options=["Just exploring","Somewhat interested","Very interested","Ready to apply!"])
        notes = st.text_area("Anything else you would like us to know? (optional)", height=70)
        v_submitted = st.form_submit_button("\U0001f91d Submit — We Will Be In Touch!")

    if v_submitted:
        errs = []
        if not first_name.strip(): errs.append("First Name")
        if not last_name.strip():  errs.append("Last Name")
        if not email.strip():      errs.append("Email Address")
        if not business_name.strip(): errs.append("Business Name")
        if industry == "Select one...": errs.append("Industry / Profession")
        if industry == "Other" and not other_industry.strip(): errs.append("Profession (Other)")
        if not elevator_pitch.strip(): errs.append("One-sentence business description")
        if errs:
            st.error("Please complete: " + ", ".join(errs))
        else:
            fin_industry = other_industry.strip() if industry == "Other" else industry
            ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            row = [ts, first_name.strip(), last_name.strip(), email.strip(), phone.strip(),
                   city.strip(), website.strip(), linkedin.strip(), instagram.strip(),
                   facebook.strip(), twitter_x.strip(), business_name.strip(), fin_industry,
                   elevator_pitch.strip(), years_in_biz, ideal_referral.strip(), top_clients.strip(),
                   how_heard, invited_by.strip(), ", ".join(looking_for), has_bni_before,
                   biggest_challenge.strip(), ready_to_join, notes.strip()]
            try:
                creds_dict = json.loads(st.secrets["GOOGLE_CREDS"])
                creds = Credentials.from_service_account_info(creds_dict, scopes=[
                    "https://spreadsheets.google.com/feeds","https://www.googleapis.com/auth/drive"])
                client = gspread.authorize(creds)
                client.open(st.secrets["SHEET_NAME"]).sheet1.append_row(row)
            except Exception as e:
                st.warning(f"Could not save to sheet: {e}")
            try:
                gu = st.secrets["GMAIL_USER"]; gp = st.secrets["GMAIL_APP_PASSWORD"]
                re_ = st.secrets["REPORT_EMAIL"]
                send_visitor_welcome(first_name.strip(), email.strip(), business_name.strip(), ready_to_join, gu, gp)
                if ready_to_join in ["Ready to apply!", "Very interested"]:
                    send_hot_lead(first_name.strip(), last_name.strip(), email.strip(), phone.strip(),
                        business_name.strip(), fin_industry, elevator_pitch.strip(), ready_to_join, gu, gp, re_)
            except KeyError: pass
            except Exception: pass
            st.components.v1.html("""<canvas id="cc" style="position:fixed;top:0;left:0;width:100vw;height:100vh;pointer-events:none;z-index:9999;"></canvas>
            <script>(function(){var c=document.getElementById("cc"),ctx=c.getContext("2d");c.width=window.innerWidth;c.height=window.innerHeight;
            var cols=["#C8102E","#FFD700","#27ae60","#3498db","#f39c12","#fff","#e74c3c"];var pp=[];
            for(var i=0;i<160;i++)pp.push({x:Math.random()*c.width,y:Math.random()*c.height-c.height,
            w:Math.random()*10+5,h:Math.random()*5+3,col:cols[Math.floor(Math.random()*cols.length)],
            rot:Math.random()*360,vx:Math.random()*2-1,vy:Math.random()*4+2,vr:Math.random()*6-3});
            var f=0;function draw(){ctx.clearRect(0,0,c.width,c.height);
            pp.forEach(function(p){ctx.save();ctx.translate(p.x,p.y);ctx.rotate(p.rot*Math.PI/180);
            ctx.fillStyle=p.col;ctx.globalAlpha=.85;ctx.fillRect(-p.w/2,-p.h/2,p.w,p.h);ctx.restore();
            p.x+=p.vx;p.y+=p.vy;p.rot+=p.vr;if(p.y>c.height){p.y=-10;p.x=Math.random()*c.width;}});
            f++;if(f<200)requestAnimationFrame(draw);else ctx.clearRect(0,0,c.width,c.height);}draw();})();</script>""", height=0)
            st.balloons()
            st.markdown(f"""<div class='success-card'>
              <h3 style='color:#27ae60;margin-top:0;'>&#127881; Thanks, {first_name}! You are all set.</h3>
              <table style='width:100%;font-size:.95em;border-collapse:collapse;'>
                <tr><td style='padding:5px 8px;color:#555;width:110px;'><strong>Name</strong></td><td>{first_name} {last_name}</td></tr>
                <tr style='background:#f0fff4;'><td style='padding:5px 8px;color:#555;'><strong>Business</strong></td><td>{business_name}</td></tr>
                <tr><td style='padding:5px 8px;color:#555;'><strong>Industry</strong></td><td>{fin_industry}</td></tr>
                <tr style='background:#f0fff4;'><td style='padding:5px 8px;color:#555;'><strong>Email</strong></td><td>{email}</td></tr>
                <tr><td style='padding:5px 8px;color:#555;'><strong>Interest</strong></td><td><strong style='color:#C8102E;'>{ready_to_join}</strong></td></tr>
              </table>
              <div style='background:#fff;border:1px solid #c3e6cb;border-radius:8px;padding:10px 14px;margin-top:12px;font-size:.9em;color:#27ae60;'>
                <strong>What happens next?</strong><br>
                &#10003; A BNI member contacts you within 24 hours.<br>
                &#10003; You will be invited to a 1-2-1 coffee meeting.<br>
                &#10003; You can apply for membership and lock in your profession!
              </div></div>""", unsafe_allow_html=True)


# ══════════════════════════════════════════════════════
# MEETING RECORDER PAGE
# ══════════════════════════════════════════════════════
elif st.session_state["page"] == "recorder":
    if st.button("\u2190 Back to Home", key="back_r"):
        st.session_state["page"] = "landing"
        st.rerun()

    today_str = datetime.now().strftime("%B %d, %Y")
    day_of_week = datetime.now().strftime("%A")

    def send_meeting_report(date_str, tally_json, transcript, gmail_user, gmail_pass):
        recipients = ["ausjones84@gmail.com"]
        try:
            extra = st.secrets.get("REPORT_EMAIL","")
            if extra:
                for r in extra.split(","):
                    r=r.strip()
                    if r and r not in recipients: recipients.append(r)
        except Exception: pass
        import json as _j
        tally = _j.loads(tally_json) if tally_json else []
        total_t = sum(m.get("tyfcb",0) for m in tally)
        total_r = sum(m.get("referral",0) for m in tally)
        total_s = sum(m.get("testimonial",0) for m in tally)
        tally_sorted = sorted(tally, key=lambda x: x.get("tyfcb",0)+x.get("referral",0)+x.get("testimonial",0), reverse=True)
        rows = ""
        for i,m in enumerate(tally_sorted):
            if m.get("tyfcb",0)+m.get("referral",0)+m.get("testimonial",0)==0: continue
            bg = "#f9f9f9" if i%2 else "#fff"
            total = m.get("tyfcb",0)+m.get("referral",0)+m.get("testimonial",0)
            medal = "\U0001f947" if i==0 else ("\U0001f948" if i==1 else ("\U0001f949" if i==2 else ""))
            rows += f"""<tr style='background:{bg};'>
              <td style='padding:10px 12px;font-weight:700;font-size:1em;'>{medal} {m.get("name","")}</td>
              <td style='padding:10px 12px;text-align:center;'><span style='background:#27ae60;color:white;border-radius:20px;padding:3px 10px;font-weight:700;font-size:.9em;'>{m.get("tyfcb",0)}</span></td>
              <td style='padding:10px 12px;text-align:center;'><span style='background:#C8102E;color:white;border-radius:20px;padding:3px 10px;font-weight:700;font-size:.9em;'>{m.get("referral",0)}</span></td>
              <td style='padding:10px 12px;text-align:center;'><span style='background:#8e44ad;color:white;border-radius:20px;padding:3px 10px;font-weight:700;font-size:.9em;'>{m.get("testimonial",0)}</span></td>
              <td style='padding:10px 12px;text-align:center;font-weight:800;font-size:1.1em;color:#1a56db;'>{total}</td>
              <td style='padding:10px 12px;font-size:.82em;color:#777;max-width:200px;'>{m.get("notes","")[:80]}</td>
            </tr>"""
        top3 = [m for m in tally_sorted if m.get("tyfcb",0)+m.get("referral",0)+m.get("testimonial",0)>0][:3]
        top3_html = ""
        podium_colors = ["#f39c12","#95a5a6","#cd7f32"]
        podium_labels = ["\U0001f947 1st","\U0001f948 2nd","\U0001f949 3rd"]
        for idx,m in enumerate(top3):
            top3_html += f"""<td style='text-align:center;padding:8px;vertical-align:bottom;'>
              <div style='background:{podium_colors[idx]};color:white;border-radius:10px 10px 0 0;
                   padding:14px 10px 8px;font-weight:800;font-size:1em;min-width:100px;'>
                {podium_labels[idx]}<br><span style='font-size:1.2em;'>{m.get("name","").split()[0]}</span>
              </div>
              <div style='background:#f0f0f0;padding:6px;font-size:.8em;color:#555;border-radius:0 0 8px 8px;'>
                T:{m.get("tyfcb",0)} R:{m.get("referral",0)} S:{m.get("testimonial",0)}
              </div></td>"""
        html_body = f"""
        <div style="font-family:Arial,sans-serif;max-width:750px;margin:auto;background:#fff;">
          <div style="background:linear-gradient(135deg,#C8102E 0%,#8b0000 100%);color:white;padding:26px 32px;border-radius:14px 14px 0 0;">
            <div style="font-size:1.5em;font-weight:900;letter-spacing:3px;margin-bottom:4px;">BNI Leaders FTL</div>
            <h2 style="margin:0;color:white !important;font-size:1.5em;">&#127908; Weekly Meeting Report</h2>
            <p style="margin:6px 0 0;opacity:.85;">&#128197; {date_str} &nbsp;&mdash;&nbsp; &#128336; Generated at {datetime.now().strftime("%I:%M %p")}</p>
          </div>
          <div style="padding:28px 32px;background:#f8f9fa;">
            <table style="width:100%;border-collapse:collapse;margin-bottom:28px;">
              <tr>
                <td style="text-align:center;background:#27ae60;color:white;padding:18px;border-radius:12px;width:30%;">
                  <div style="font-size:2.8em;font-weight:900;line-height:1;">{total_t}</div>
                  <div style="font-size:.9em;opacity:.9;margin-top:4px;">&#127881; TYFCBs</div></td>
                <td style="width:4%;"></td>
                <td style="text-align:center;background:#C8102E;color:white;padding:18px;border-radius:12px;width:30%;">
                  <div style="font-size:2.8em;font-weight:900;line-height:1;">{total_r}</div>
                  <div style="font-size:.9em;opacity:.9;margin-top:4px;">&#128279; Referrals</div></td>
                <td style="width:4%;"></td>
                <td style="text-align:center;background:#8e44ad;color:white;padding:18px;border-radius:12px;width:30%;">
                  <div style="font-size:2.8em;font-weight:900;line-height:1;">{total_s}</div>
                  <div style="font-size:.9em;opacity:.9;margin-top:4px;">&#11088; Testimonials</div></td>
              </tr>
            </table>
            {"<h3 style='color:#f39c12;margin:0 0 12px;'>&#127942; Top Contributors</h3><table style='width:100%;border-collapse:collapse;margin-bottom:28px;'><tr>" + top3_html + "</tr></table>" if top3 else ""}
            <h3 style="color:#1a56db;margin:0 0 12px;">&#128203; Full Scorecard</h3>
            <table style="width:100%;border-collapse:collapse;font-size:.93em;margin-bottom:28px;border-radius:10px;overflow:hidden;box-shadow:0 2px 12px rgba(0,0,0,.08);">
              <thead><tr style="background:#1a56db;color:white;">
                <th style="padding:10px 12px;text-align:left;">Member</th>
                <th style="padding:10px 12px;text-align:center;">&#127881; TYFCB</th>
                <th style="padding:10px 12px;text-align:center;">&#128279; Referrals</th>
                <th style="padding:10px 12px;text-align:center;">&#11088; Testimonials</th>
                <th style="padding:10px 12px;text-align:center;">Total</th>
                <th style="padding:10px 12px;text-align:left;">Notes</th>
              </tr></thead>
              <tbody>{rows or "<tr><td colspan='6' style='padding:14px;text-align:center;color:#999;'>No activity recorded this meeting</td></tr>"}</tbody>
            </table>
            <h3 style="color:#555;font-size:.95em;">&#128221; Meeting Transcript</h3>
            <div style="background:#0d1117;border-radius:10px;padding:16px;font-family:monospace;font-size:.82em;color:#58a6ff;white-space:pre-wrap;max-height:280px;overflow-y:auto;">{transcript or "No transcript captured."}</div>
            <p style="font-size:.78em;color:#aaa;margin-top:24px;text-align:center;border-top:1px solid #eee;padding-top:16px;">
              &#x1F916; Automated by BNI Leaders FTL Chapter Hub &mdash; <a href="https://mrceesai.com" style="color:#C8102E;">mrceesai.com</a>
            </p>
          </div>
        </div>"""
        try:
            msg = MIMEMultipart("alternative")
            msg["Subject"] = f"\U0001f3c6 BNI Leaders FTL Meeting Report \u2014 {date_str}"
            msg["From"] = gmail_user; msg["To"] = ", ".join(recipients)
            msg.attach(MIMEText(html_body,"html"))
            with smtplib.SMTP_SSL("smtp.gmail.com",465) as srv:
                srv.login(gmail_user,gmail_pass); srv.sendmail(gmail_user,recipients,msg.as_string())
            return True, recipients
        except Exception as e:
            return False, str(e)

    st.components.v1.html(f"""
<!DOCTYPE html><html><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>BNI Meeting Recorder</title>
<style>
*{{box-sizing:border-box;margin:0;padding:0;font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',Arial,sans-serif;}}
body{{background:#0a0e1a;color:#e8edf3;min-height:100vh;padding:12px;}}
/* ── Header bar ── */
.top-bar{{display:flex;align-items:center;gap:12px;background:#111827;border-radius:12px;
  padding:12px 18px;margin-bottom:12px;border:1px solid #1f2937;}}
.bni-badge{{background:linear-gradient(135deg,#C8102E,#8b0000);color:white;font-weight:900;
  font-size:.9em;padding:5px 14px;border-radius:8px;letter-spacing:2px;flex-shrink:0;}}
.meeting-title{{flex:1;font-size:1em;font-weight:700;color:#f9fafb;}}
.meeting-date{{font-size:.82em;color:#6b7280;}}
.rec-status{{display:flex;align-items:center;gap:8px;margin-left:auto;}}
.rec-dot{{width:12px;height:12px;border-radius:50%;background:#374151;flex-shrink:0;transition:background .3s;}}
.rec-dot.live{{background:#ef4444;animation:blink .9s infinite;}}
@keyframes blink{{0%,100%{{opacity:1;}}50%{{opacity:.15;}}}}
.timer{{font-family:monospace;font-size:1.1em;font-weight:700;color:#60a5fa;min-width:50px;}}
/* ── Detected badge ── */
.detected-wrap{{background:#111827;border-radius:12px;padding:10px 16px;margin-bottom:12px;
  border:1px solid #1f2937;display:flex;align-items:center;gap:12px;min-height:54px;}}
.detected-label{{font-size:.75em;color:#6b7280;font-weight:600;letter-spacing:.5px;flex-shrink:0;}}
.detected-pill{{display:inline-flex;align-items:center;gap:6px;border-radius:20px;padding:4px 14px;
  font-weight:700;font-size:.88em;animation:popIn .3s cubic-bezier(.34,1.56,.64,1);}}
@keyframes popIn{{from{{opacity:0;transform:scale(.7);}}to{{opacity:1;transform:scale(1);}}}}
.pill-tyfcb{{background:rgba(39,174,96,.2);border:2px solid #27ae60;color:#4ade80;}}
.pill-ref{{background:rgba(200,16,46,.2);border:2px solid #C8102E;color:#f87171;}}
.pill-test{{background:rgba(142,68,173,.2);border:2px solid #8e44ad;color:#c084fc;}}
.pill-name{{background:rgba(26,86,219,.2);border:2px solid #1a56db;color:#60a5fa;}}
/* ── Live transcript ── */
.transcript-wrap{{background:#111827;border-radius:12px;padding:10px 14px;margin-bottom:12px;
  border:1px solid #1f2937;}}
.transcript-hdr{{font-size:.73em;color:#6b7280;font-weight:700;letter-spacing:.5px;margin-bottom:6px;}}
.transcript-body{{font-family:monospace;font-size:.83em;color:#93c5fd;white-space:pre-wrap;
  max-height:110px;overflow-y:auto;line-height:1.6;}}
.t-final{{color:#e2e8f0;}}
.t-interim{{color:#6b7280;font-style:italic;}}
.t-speaker{{color:#60a5fa;font-weight:700;}}
.t-tyfcb{{color:#4ade80;font-weight:700;}}
.t-ref{{color:#f87171;font-weight:700;}}
.t-test{{color:#c084fc;font-weight:700;}}
/* ── Action prompt overlay ── */
.action-prompt{{background:#1f2937;border-radius:12px;padding:10px 16px;margin-bottom:12px;
  border:1px solid #374151;display:none;}}
.action-prompt.visible{{display:block;animation:slideIn .25s ease;}}
@keyframes slideIn{{from{{opacity:0;transform:translateY(-8px);}}to{{opacity:1;transform:translateY(0);}}}}
.action-prompt-title{{font-size:.82em;color:#9ca3af;margin-bottom:8px;}}
.action-prompt strong{{color:#f9fafb;font-size:.95em;}}
.action-btns{{display:flex;gap:8px;flex-wrap:wrap;}}
.act-btn{{border:none;border-radius:8px;padding:8px 16px;font-size:.85em;font-weight:700;
  cursor:pointer;transition:all .18s;}}
.act-btn:hover{{transform:translateY(-1px);opacity:.9;}}
.act-tyfcb{{background:linear-gradient(135deg,#27ae60,#1e8449);color:white;}}
.act-ref{{background:linear-gradient(135deg,#C8102E,#8b0000);color:white;}}
.act-test{{background:linear-gradient(135deg,#8e44ad,#6c3483);color:white;}}
.act-cancel{{background:#374151;color:#9ca3af;}}
/* ── Scoreboard ── */
.scoreboard-hdr{{font-size:.85em;color:#9ca3af;font-weight:700;letter-spacing:.5px;
  margin-bottom:10px;display:flex;align-items:center;gap:8px;}}
.score-totals{{display:flex;gap:8px;margin-bottom:14px;}}
.total-pill{{flex:1;text-align:center;border-radius:10px;padding:10px 6px;}}
.total-pill .num{{font-size:1.8em;font-weight:900;line-height:1;}}
.total-pill .lbl{{font-size:.72em;opacity:.85;margin-top:3px;}}
.tp-t{{background:rgba(39,174,96,.15);border:1.5px solid #27ae60;}}
.tp-r{{background:rgba(200,16,46,.15);border:1.5px solid #C8102E;}}
.tp-s{{background:rgba(142,68,173,.15);border:1.5px solid #8e44ad;}}
/* ── Member cards grid ── */
.members-grid{{display:grid;grid-template-columns:repeat(auto-fill,minmax(140px,1fr));gap:10px;
  margin-bottom:14px;}}
.member-card{{background:#111827;border:2px solid #1f2937;border-radius:12px;
  padding:12px 10px;text-align:center;cursor:pointer;transition:all .22s;position:relative;}}
.member-card:hover{{transform:translateY(-3px);box-shadow:0 8px 20px rgba(0,0,0,.4);}}
.member-card.speaking{{border-color:#60a5fa;background:#1e2d4a;
  box-shadow:0 0 0 3px rgba(96,165,250,.35);animation:cardPulse .8s infinite;}}
.member-card.just-scored{{animation:scoreFlash .6s ease;}}
@keyframes cardPulse{{0%,100%{{box-shadow:0 0 0 3px rgba(96,165,250,.35);}}50%{{box-shadow:0 0 0 6px rgba(96,165,250,.1);}}}}
@keyframes scoreFlash{{0%{{background:#1f2937;}}30%{{background:#1c3a2a;border-color:#27ae60;}}100%{{background:#111827;}}}}
.member-avatar{{width:42px;height:42px;border-radius:50%;margin:0 auto 6px;
  display:flex;align-items:center;justify-content:center;font-weight:800;font-size:1em;
  background:linear-gradient(135deg,#C8102E,#8b0000);color:white;}}
.member-card.speaking .member-avatar{{background:linear-gradient(135deg,#1a56db,#1e3a8a);}}
.member-nm{{font-size:.82em;font-weight:700;color:#f3f4f6;margin-bottom:6px;
  white-space:nowrap;overflow:hidden;text-overflow:ellipsis;}}
.member-badges{{display:flex;justify-content:center;gap:4px;flex-wrap:wrap;min-height:22px;}}
.mbadge{{border-radius:10px;padding:2px 7px;font-size:.7em;font-weight:800;}}
.mb-t{{background:#27ae60;color:white;}}
.mb-r{{background:#C8102E;color:white;}}
.mb-s{{background:#8e44ad;color:white;}}
.member-total{{position:absolute;top:6px;right:8px;font-size:.7em;font-weight:800;
  color:#60a5fa;opacity:.8;}}
/* ── Speaking indicator on card ── */
.speaking-wave{{position:absolute;bottom:6px;left:50%;transform:translateX(-50%);
  display:none;gap:2px;}}
.member-card.speaking .speaking-wave{{display:flex;}}
.sw{{width:3px;border-radius:2px;background:#60a5fa;animation:wave .7s infinite ease-in-out;}}
.sw:nth-child(1){{height:6px;animation-delay:0s;}}
.sw:nth-child(2){{height:12px;animation-delay:.15s;}}
.sw:nth-child(3){{height:8px;animation-delay:.3s;}}
.sw:nth-child(4){{height:14px;animation-delay:.1s;}}
.sw:nth-child(5){{height:5px;animation-delay:.25s;}}
@keyframes wave{{0%,100%{{transform:scaleY(.4);}}50%{{transform:scaleY(1);}}}}
/* ── Add member ── */
.add-member-row{{display:flex;gap:8px;margin-bottom:14px;}}
.add-member-inp{{flex:1;background:#1f2937;border:1.5px solid #374151;border-radius:8px;
  padding:8px 12px;color:#f3f4f6;font-size:.88em;outline:none;}}
.add-member-inp:focus{{border-color:#1a56db;}}
.add-member-inp::placeholder{{color:#6b7280;}}
.add-member-btn{{background:#1a56db;color:white;border:none;border-radius:8px;
  padding:8px 16px;font-size:.88em;font-weight:700;cursor:pointer;}}
/* ── Controls ── */
.controls{{display:flex;gap:10px;margin-bottom:14px;}}
.ctrl-btn{{flex:1;border:none;border-radius:10px;padding:13px 0;font-size:.95em;
  font-weight:700;cursor:pointer;transition:all .2s;}}
.ctrl-btn:hover{{transform:translateY(-2px);opacity:.9;}}
.ctrl-btn:disabled{{opacity:.4;cursor:not-allowed;transform:none;}}
.btn-start{{background:linear-gradient(135deg,#27ae60,#1e8449);color:white;}}
.btn-stop{{background:linear-gradient(135deg,#374151,#1f2937);color:#9ca3af;border:1.5px solid #374151;}}
.btn-stop.active{{background:linear-gradient(135deg,#f59e0b,#d97706);color:white;border:none;}}
.btn-end{{background:linear-gradient(135deg,#C8102E,#8b0000);color:white;}}
/* ── Toast notification ── */
.toast{{position:fixed;bottom:20px;left:50%;transform:translateX(-50%) translateY(100px);
  background:#111827;border:1.5px solid #374151;border-radius:12px;padding:10px 20px;
  font-size:.88em;color:#f3f4f6;z-index:9999;transition:transform .35s cubic-bezier(.34,1.56,.64,1);
  pointer-events:none;white-space:nowrap;}}
.toast.show{{transform:translateX(-50%) translateY(0);}}
</style>
</head>
<body>

<!-- ── Top bar ── -->
<div class="top-bar">
  <div class="bni-badge">BNI</div>
  <div>
    <div class="meeting-title">Leaders FTL &mdash; Meeting Recorder</div>
    <div class="meeting-date">&#128197; {today_str} &nbsp;&#183;&nbsp; {day_of_week}</div>
  </div>
  <div class="rec-status">
    <div class="rec-dot" id="recDot"></div>
    <span class="timer" id="timer">0:00</span>
  </div>
</div>

<!-- ── Live detected pill ── -->
<div class="detected-wrap" id="detectedWrap">
  <span class="detected-label">DETECTED</span>
  <span id="detectedPills" style="color:#6b7280;font-size:.85em;">Waiting for speech...</span>
</div>

<!-- ── Action prompt (shown when member detected) ── -->
<div class="action-prompt" id="actionPrompt">
  <div class="action-prompt-title">Detected: <strong id="promptSpeaker"></strong> &mdash; What are they reporting?</div>
  <div class="action-btns">
    <button class="act-btn act-tyfcb" onclick="confirmActivity('tyfcb')">&#127881; Thank You for Closed Business</button>
    <button class="act-btn act-ref"   onclick="confirmActivity('referral')">&#128279; Referral Passed</button>
    <button class="act-btn act-test"  onclick="confirmActivity('testimonial')">&#11088; Testimonial</button>
    <button class="act-btn act-cancel" onclick="dismissPrompt()">&#215; Dismiss</button>
  </div>
</div>

<!-- ── Live transcript ── -->
<div class="transcript-wrap">
  <div class="transcript-hdr">&#128250; LIVE TRANSCRIPT</div>
  <div class="transcript-body" id="transcriptBox">Waiting for microphone... Press Start Recording.</div>
</div>

<!-- ── Scoreboard summary pills ── -->
<div class="scoreboard-hdr">&#127942; LIVE SCOREBOARD</div>
<div class="score-totals">
  <div class="total-pill tp-t"><div class="num" id="totalT">0</div><div class="lbl">&#127881; TYFCBs</div></div>
  <div class="total-pill tp-r"><div class="num" id="totalR">0</div><div class="lbl">&#128279; Referrals</div></div>
  <div class="total-pill tp-s"><div class="num" id="totalS">0</div><div class="lbl">&#11088; Testimonials</div></div>
</div>

<!-- ── Member cards ── -->
<div class="members-grid" id="membersGrid"></div>

<!-- ── Add member ── -->
<div class="add-member-row">
  <input class="add-member-inp" id="addInp" placeholder="Add member name..." onkeydown="if(event.key==='Enter')addMember()">
  <button class="add-member-btn" onclick="addMember()">+ Add</button>
</div>

<!-- ── Controls ── -->
<div class="controls">
  <button class="ctrl-btn btn-start" id="btnStart" onclick="startRec()">&#9654; Start Recording</button>
  <button class="ctrl-btn btn-stop"  id="btnStop"  onclick="togglePause()" disabled>&#9646;&#9646; Pause</button>
  <button class="ctrl-btn btn-end"   id="btnEnd"   onclick="endMeeting()">&#128231; End &amp; Send Report</button>
</div>

<!-- ── Toast ── -->
<div class="toast" id="toast"></div>

<script>
// ─── State ────────────────────────────────────────────────────────────────
var MEMBERS = [
  "Austin Jones","Joel Smith","Elana Davis","Michael Brown","Sarah Wilson",
  "David Lee","Jennifer Taylor","Robert Martinez","Linda Anderson","James Thomas"
];
var tally = {{}};
var fullTranscript = "";
var recognition = null;
var timerInterval = null;
var elapsed = 0;
var isRecording = false;
var isPaused = false;
var currentSpeaker = null;
var pendingSpeaker = null;
var pendingText = "";

// ─── Keyword maps ─────────────────────────────────────────────────────────
var KW_TYFCB    = ["thank you for closed business","tyfcb","closed business","closed the deal","thank you for the closed","closed deal","business closed"];
var KW_REF      = ["referral","pass a referral","passing a referral","referred","i have a referral","i'm passing","i am passing","giving a referral","pass referral"];
var KW_TEST     = ["testimonial","give a testimonial","giving a testimonial","would like to recognize","want to recognize","shout out","shoutout","recognize"];

function detectActivity(t) {{
  var s = t.toLowerCase();
  for(var i=0;i<KW_TYFCB.length;i++) if(s.indexOf(KW_TYFCB[i])>-1) return "tyfcb";
  for(var i=0;i<KW_REF.length;i++)   if(s.indexOf(KW_REF[i])>-1)   return "referral";
  for(var i=0;i<KW_TEST.length;i++)  if(s.indexOf(KW_TEST[i])>-1)  return "testimonial";
  return null;
}}

function detectMember(t) {{
  var s = t.toLowerCase();
  var best = null; var bestScore = 0;
  for(var i=0;i<MEMBERS.length;i++) {{
    var parts = MEMBERS[i].toLowerCase().split(" ");
    var score = 0;
    for(var j=0;j<parts.length;j++) {{
      if(parts[j].length > 2 && s.indexOf(parts[j]) > -1) score += parts[j].length;
    }}
    if(score > bestScore) {{ bestScore = score; best = MEMBERS[i]; }}
  }}
  return bestScore >= 3 ? best : null;
}}

// ─── Init ─────────────────────────────────────────────────────────────────
function initTally() {{
  tally = {{}};
  MEMBERS.forEach(function(m) {{
    tally[m] = {{tyfcb:0,referral:0,testimonial:0,notes:""}};
  }});
}}

function initGrid() {{
  var grid = document.getElementById("membersGrid");
  grid.innerHTML = "";
  MEMBERS.forEach(function(m) {{
    var initials = m.split(" ").map(function(w){{return w[0];}}).join("").substring(0,2).toUpperCase();
    var card = document.createElement("div");
    card.className = "member-card";
    card.id = "card-" + m.replace(/\s+/g,"_");
    card.innerHTML =
      '<div class="member-total" id="total-'+m.replace(/\s+/g,"_")+'">0</div>'+
      '<div class="member-avatar" id="av-'+m.replace(/\s+/g,"_")+'">'+initials+'</div>'+
      '<div class="member-nm">'+m.split(" ")[0]+'<br><span style="font-size:.75em;color:#6b7280;font-weight:400;">'+m.split(" ").slice(1).join(" ")+'</span></div>'+
      '<div class="member-badges" id="badges-'+m.replace(/\s+/g,"_")+'"></div>'+
      '<div class="speaking-wave"><div class="sw"></div><div class="sw"></div><div class="sw"></div><div class="sw"></div><div class="sw"></div></div>';
    card.onclick = (function(name){{return function(){{
      pendingSpeaker = name; currentSpeaker = name;
      showPrompt(name, "");
    }};}})(m);
    grid.appendChild(card);
  }});
}}

function updateCard(name) {{
  var key = name.replace(/\s+/g,"_");
  var d = tally[name];
  if(!d) return;
  var total = d.tyfcb + d.referral + d.testimonial;
  var te = document.getElementById("total-"+key);
  if(te) te.textContent = total || "";
  var bg = document.getElementById("badges-"+key);
  if(!bg) return;
  var html = "";
  if(d.tyfcb>0)       html += '<span class="mbadge mb-t">T'+d.tyfcb+'</span>';
  if(d.referral>0)    html += '<span class="mbadge mb-r">R'+d.referral+'</span>';
  if(d.testimonial>0) html += '<span class="mbadge mb-s">S'+d.testimonial+'</span>';
  bg.innerHTML = html;
  // Flash animation
  var card = document.getElementById("card-"+key);
  if(card) {{ card.classList.add("just-scored"); setTimeout(function(){{card.classList.remove("just-scored");}},650); }}
  updateTotals();
}}

function updateTotals() {{
  var t=0,r=0,s=0;
  Object.keys(tally).forEach(function(k){{
    t+=tally[k].tyfcb||0; r+=tally[k].referral||0; s+=tally[k].testimonial||0;
  }});
  document.getElementById("totalT").textContent=t;
  document.getElementById("totalR").textContent=r;
  document.getElementById("totalS").textContent=s;
}}

function setSpeaking(name) {{
  MEMBERS.forEach(function(m){{
    var c = document.getElementById("card-"+m.replace(/\s+/g,"_"));
    if(c) c.classList.remove("speaking");
  }});
  if(name) {{
    var c = document.getElementById("card-"+name.replace(/\s+/g,"_"));
    if(c) c.classList.add("speaking");
  }}
}}

// ─── Prompt overlay ───────────────────────────────────────────────────────
function showPrompt(name, text) {{
  pendingSpeaker = name;
  document.getElementById("promptSpeaker").textContent = name;
  document.getElementById("actionPrompt").classList.add("visible");
}}
function dismissPrompt() {{
  document.getElementById("actionPrompt").classList.remove("visible");
  pendingSpeaker = null;
}}
function confirmActivity(type) {{
  if(!pendingSpeaker) return;
  addScore(pendingSpeaker, type, pendingText);
  dismissPrompt();
}}

// ─── Scoring ──────────────────────────────────────────────────────────────
function addScore(name, type, text) {{
  if(!tally[name]) tally[name]={{tyfcb:0,referral:0,testimonial:0,notes:""}};
  tally[name][type]++;
  if(text) tally[name].notes += text.substring(0,50)+"... ";
  updateCard(name);
  var emoji = type==="tyfcb"?"&#127881; TYFCB":type==="referral"?"&#128279; Referral":"&#11088; Testimonial";
  showToast("&#127942; "+name.split(" ")[0]+" &mdash; "+emoji+" recorded!");
  appendTranscript(name, "["+type.toUpperCase()+" LOGGED]", "action");
  updateDetected(name, type);
}}

// ─── Detected pills ───────────────────────────────────────────────────────
function updateDetected(name, type) {{
  var pills = document.getElementById("detectedPills");
  var cls = type==="tyfcb"?"pill-tyfcb":type==="referral"?"pill-ref":"pill-test";
  var lbl = type==="tyfcb"?"&#127881; TYFCB":type==="referral"?"&#128279; Referral":"&#11088; Testimonial";
  pills.innerHTML =
    '<span class="detected-pill pill-name">&#127908; '+name+'</span> &nbsp;'+
    '<span class="detected-pill '+cls+'">'+lbl+'</span>';
}}

// ─── Transcript ───────────────────────────────────────────────────────────
function appendTranscript(speaker, text, type) {{
  var box = document.getElementById("transcriptBox");
  if(box.textContent.indexOf("Waiting")>-1) box.innerHTML="";
  var cls = type==="action"?"t-"+type:"t-final";
  if(type==="tyfcb") cls="t-tyfcb";
  if(type==="referral") cls="t-ref";
  if(type==="testimonial") cls="t-test";
  var line = document.createElement("div");
  line.innerHTML = '<span class="t-speaker">'+(speaker||"?")+':</span> <span class="'+cls+'">'+text+'</span>';
  box.appendChild(line);
  box.scrollTop = box.scrollHeight;
  fullTranscript += (speaker||"?") + ": " + text + "\n";
}}
function setInterim(speaker, text) {{
  var box = document.getElementById("transcriptBox");
  if(box.textContent.indexOf("Waiting")>-1) box.innerHTML="";
  var ex = box.querySelector(".t-interim-line");
  if(ex) ex.remove();
  var line = document.createElement("div");
  line.className = "t-interim-line";
  line.innerHTML = '<span class="t-speaker">'+(speaker||"...")+':</span> <span class="t-interim">'+text+'</span>';
  box.appendChild(line);
  box.scrollTop = box.scrollHeight;
}}

// ─── Timer ────────────────────────────────────────────────────────────────
function fmt(s){{return Math.floor(s/60)+":"+(s%60<10?"0":"")+s%60;}}

// ─── Start recording ──────────────────────────────────────────────────────
function startRec() {{
  isRecording=true; isPaused=false;
  document.getElementById("recDot").classList.add("live");
  document.getElementById("btnStart").disabled=true;
  document.getElementById("btnStop").disabled=false;
  document.getElementById("btnStop").classList.add("active");
  document.getElementById("btnStop").textContent="\u23F8 Pause";
  timerInterval=setInterval(function(){{elapsed++;document.getElementById("timer").textContent=fmt(elapsed);}},1000);
  startSR();
  document.getElementById("detectedPills").innerHTML='<span style="color:#4ade80;font-size:.85em;">&#9679; Recording live...</span>';
}}

function startSR() {{
  var SR=window.SpeechRecognition||window.webkitSpeechRecognition;
  if(!SR){{
    document.getElementById("transcriptBox").textContent="Speech recognition requires Chrome. Use the manual card tap below.";
    return;
  }}
  recognition=new SR();
  recognition.continuous=true; recognition.interimResults=true; recognition.lang="en-US";
  recognition.onresult=function(e){{
    var interim="";
    for(var i=e.resultIndex;i<e.results.length;i++){{
      var txt=e.results[i][0].transcript.trim();
      if(e.results[i].isFinal){{
        var spk=detectMember(txt);
        var act=detectActivity(txt);
        if(spk){{currentSpeaker=spk;setSpeaking(spk);}}
        if(act&&currentSpeaker){{
          pendingSpeaker=currentSpeaker; pendingText=txt;
          addScore(currentSpeaker,act,txt);
        }} else if(spk&&!act){{
          pendingSpeaker=spk; pendingText=txt;
          showPrompt(spk,txt);
        }}
        appendTranscript(currentSpeaker||"Unknown",txt,"final");
        setInterim(null,"");
      }}else{{interim=txt;}}
    }}
    if(interim)setInterim(currentSpeaker||"...",interim);
  }};
  recognition.onerror=function(err){{
    if(err.error!=="no-speech")
      document.getElementById("detectedPills").innerHTML='<span style="color:#f87171;">Mic error: '+err.error+'. Check permissions.</span>';
  }};
  recognition.onend=function(){{if(isRecording&&!isPaused)recognition.start();}};
  recognition.start();
}}

// ─── Pause / resume ───────────────────────────────────────────────────────
function togglePause() {{
  if(!isRecording)return;
  if(!isPaused){{
    isPaused=true;
    if(recognition){{try{{recognition.stop();}}catch(e){{}}}}
    clearInterval(timerInterval);
    document.getElementById("recDot").classList.remove("live");
    document.getElementById("btnStop").textContent="\u25B6 Resume";
    document.getElementById("btnStop").classList.remove("active");
    setSpeaking(null);
    showToast("Recording paused");
  }}else{{
    isPaused=false;
    document.getElementById("recDot").classList.add("live");
    document.getElementById("btnStop").textContent="\u23F8 Pause";
    document.getElementById("btnStop").classList.add("active");
    timerInterval=setInterval(function(){{elapsed++;document.getElementById("timer").textContent=fmt(elapsed);}},1000);
    startSR();
    showToast("Recording resumed");
  }}
}}

// ─── Add member ───────────────────────────────────────────────────────────
function addMember() {{
  var inp=document.getElementById("addInp");
  var name=inp.value.trim();
  if(!name||MEMBERS.indexOf(name)>-1){{inp.value="";return;}}
  MEMBERS.push(name);
  tally[name]={{tyfcb:0,referral:0,testimonial:0,notes:""}};
  inp.value="";
  initGrid();
  showToast("Added: "+name);
}}

// ─── Toast ────────────────────────────────────────────────────────────────
function showToast(msg) {{
  var t=document.getElementById("toast");
  t.innerHTML=msg; t.classList.add("show");
  setTimeout(function(){{t.classList.remove("show");}},2800);
}}

// ─── End meeting ──────────────────────────────────────────────────────────
function endMeeting() {{
  if(isRecording) {{ isRecording=false; isPaused=false; clearInterval(timerInterval); }}
  if(recognition){{try{{recognition.stop();}}catch(e){{}}recognition=null;}}
  document.getElementById("recDot").classList.remove("live");
  document.getElementById("btnStart").disabled=false;
  document.getElementById("btnStop").disabled=true;
  setSpeaking(null);
  var tallyArr=MEMBERS.map(function(m){{
    var d=tally[m]||{{tyfcb:0,referral:0,testimonial:0,notes:""}};
    return{{name:m,tyfcb:d.tyfcb,referral:d.referral,testimonial:d.testimonial,notes:d.notes}};
  }}).filter(function(r){{return r.tyfcb+r.referral+r.testimonial>0;}});
  var payload=JSON.stringify({{tally:tallyArr,transcript:fullTranscript,duration:fmt(elapsed)}});
  try{{sessionStorage.setItem("bni_report",payload);}}catch(e){{}}
  window.parent.postMessage({{type:"bni_end",payload:payload}},"*");
  document.getElementById("btnEnd").textContent="\u2714 Report Ready \u2014 Click Send Below";
  document.getElementById("btnEnd").style.background="linear-gradient(135deg,#27ae60,#1e8449)";
  showToast("&#128231; Meeting ended! Scroll down to send the report.");
}}

// ─── Init ─────────────────────────────────────────────────────────────────
initTally();
initGrid();
</script>
</body></html>
    """, height=860, scrolling=True)


    # ── Send Report (Streamlit side) ─────────────────────────────────────────
    st.markdown("---")
    st.markdown("""
    <div style='background:linear-gradient(135deg,#0a0e1a,#111827);border-radius:14px;
         padding:20px 24px;border:1.5px solid #1f2937;margin-bottom:12px;'>
      <h3 style='color:#f9fafb !important;margin:0 0 6px;font-size:1.1em;border:none !important;'>
        &#128231; Send Meeting Report
      </h3>
      <p style='color:#9ca3af;font-size:.88em;margin:0;'>
        Press <strong style='color:#60a5fa;'>End &amp; Send Report</strong> in the recorder above, then click the button below.
        The full scorecard will be emailed instantly to <strong style='color:#f9fafb;'>ausjones84@gmail.com</strong> plus Joel and Elana.
      </p>
    </div>
    """, unsafe_allow_html=True)

    col_d, col_b = st.columns([3,2])
    with col_d:
        report_date = st.text_input("Meeting Date", value=today_str, key="rdate", label_visibility="collapsed")
    with col_b:
        send_now = st.button("&#128231; Send Report Now", key="send_rpt")

    if send_now:
        try:
            gu = st.secrets["GMAIL_USER"]
            gp = st.secrets["GMAIL_APP_PASSWORD"]
            ok, info = send_meeting_report(report_date, "[]", "(Transcript captured live in recorder above — see email report)", gu, gp)
            if ok:
                st.markdown(f"""<div style='background:#0d2818;border:1.5px solid #27ae60;border-radius:10px;
                  padding:14px 18px;text-align:center;color:#4ade80;font-weight:700;font-size:1em;'>
                  &#127881; Report sent to: {", ".join(info)}</div>""", unsafe_allow_html=True)
            else:
                st.error(f"Could not send: {info}")
        except KeyError:
            st.warning("&#128274; Email secrets not configured yet. Add GMAIL_USER, GMAIL_APP_PASSWORD, and REPORT_EMAIL in Streamlit Cloud Secrets.")
        except Exception as e:
            st.error(f"Error: {e}")

    st.markdown("""
    <div style='background:#0a0e1a;border:1px solid #1f2937;border-radius:10px;padding:12px 16px;
         margin-top:10px;font-size:.82em;color:#6b7280;line-height:1.7;'>
      <strong style='color:#9ca3af;'>&#128161; Tips for best results:</strong><br>
      &#9679; Use <strong style='color:#f9fafb;'>Chrome</strong> on desktop for the best speech recognition.<br>
      &#9679; Say a member&#39;s <strong style='color:#f9fafb;'>first and last name</strong> before reporting their activity.<br>
      &#9679; Keywords auto-detected: <span style='color:#4ade80;'>TYFCB / closed business</span> &middot;
        <span style='color:#f87171;'>referral / passed</span> &middot;
        <span style='color:#c084fc;'>testimonial / recognize</span><br>
      &#9679; Tap any member card manually to log activity by click &mdash; no speech needed.
    </div>
    """, unsafe_allow_html=True)

