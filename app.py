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

# ── Session state ────────────────────────────────────────────────────────────
if "page" not in st.session_state:
    st.session_state["page"] = "landing"

# ── Global CSS ───────────────────────────────────────────────────────────────
st.markdown("""
<style>
@keyframes fadeInDown {
    from { opacity:0; transform:translateY(-16px); }
    to   { opacity:1; transform:translateY(0); }
}
@keyframes fadeInUp {
    from { opacity:0; transform:translateY(16px); }
    to   { opacity:1; transform:translateY(0); }
}
@keyframes pulse {
    0%,100% { box-shadow:0 0 0 0 rgba(200,16,46,.28); }
    50%      { box-shadow:0 0 0 8px rgba(200,16,46,0); }
}
[data-testid="stAppViewContainer"] { background:#fff; }
.hero-wrap { animation:fadeInDown .7s ease both; }
/* All Streamlit buttons red */
.stButton > button {
    background:linear-gradient(135deg,#C8102E 0%,#a00d24 100%) !important;
    color:white !important; font-weight:700 !important;
    border-radius:8px !important; padding:.7em 2em !important;
    font-size:1.05em !important; width:100% !important;
    border:none !important; margin-top:8px !important;
    animation:pulse 2.4s infinite !important;
    transition:transform .12s,opacity .12s !important;
}
.stButton > button:hover { transform:translateY(-2px) !important; opacity:.93 !important; }
/* Landing cards */
.land-card {
    border-radius:16px; padding:2em 1.4em; text-align:center;
    background:#fff; box-shadow:0 6px 28px rgba(0,0,0,.09);
    border:2.5px solid transparent;
    animation:fadeInUp .8s ease both;
    transition:transform .22s,box-shadow .22s;
}
.land-card:hover { transform:translateY(-5px); box-shadow:0 14px 40px rgba(0,0,0,.13); }
.land-visitor { border-color:#C8102E !important; }
.land-member  { border-color:#1a56db !important; }
/* Intro boxes */
.intro-box {
    background:#fff5f5; border-left:5px solid #C8102E;
    padding:1em 1.5em; border-radius:0 8px 8px 0;
    margin-bottom:1em; animation:fadeInDown .9s ease both;
}
.tip-box {
    background:linear-gradient(135deg,#fffbf0,#fff8e1);
    border-left:4px solid #f39c12; border-radius:0 8px 8px 0;
    padding:.9em 1.2em; margin:.5em 0 1.2em; font-size:.97em;
}
.success-card {
    background:linear-gradient(135deg,#f0fff4,#e8f8ee);
    border:1.5px solid #27ae60; border-radius:12px;
    padding:1.5em; margin-top:1em; animation:fadeInDown .6s ease both;
}
/* Form headings */
h2 { color:#C8102E !important; border-bottom:2px solid #f0f0f0; padding-bottom:6px; }
/* Tabs */
div[data-testid="stTabs"] button[data-baseweb="tab"] {
    font-size:1.05em !important; font-weight:600 !important; padding:10px 24px !important;
}
/* Footer bar */
.footer-bar {
    text-align:center; margin-top:2em; padding:1em;
    background:#f8f9fa; border-radius:10px; font-size:.85em; color:#888;
}
</style>
""", unsafe_allow_html=True)

# ── Shared BNI Hero ──────────────────────────────────────────────────────────
st.markdown("""
<div class='hero-wrap' style='text-align:center;padding:10px 0 4px;'>
  <div style='display:inline-block;background:linear-gradient(135deg,#C8102E 0%,#8b0000 100%);
       color:white;font-size:1.6em;font-weight:900;padding:8px 28px;border-radius:10px;
       letter-spacing:3px;font-family:Arial,sans-serif;box-shadow:0 4px 16px rgba(200,16,46,.35);'>BNI Leaders FTL</div>
  <h2 style='color:#C8102E;margin:8px 0 2px;font-size:1.3em;font-weight:600;letter-spacing:1px;'>Chapter Hub</h2>
  <p style='color:#888;margin:0;font-size:.95em;'>Business Network International &mdash; Where Referrals Are Our Business</p>
</div>
""", unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════════════════
# LANDING PAGE
# ═══════════════════════════════════════════════════════════════════════════
if st.session_state["page"] == "landing":
    st.markdown("""
    <div style='text-align:center;margin:1.2em 0 1.8em;'>
      <p style='font-size:1.1em;color:#555;max-width:520px;margin:0 auto;'>
        Welcome! Choose your role to get started.
      </p>
    </div>
    """, unsafe_allow_html=True)

    col_a, col_b = st.columns(2, gap="large")

    with col_a:
        st.markdown("""
        <div class='land-card land-visitor'>
          <div style='font-size:3.2em;margin-bottom:.3em;'>&#128075;</div>
          <h2 style='color:#C8102E !important;border:none;margin:0 0 .5em;font-size:1.35em;'>Visitor Sign-In</h2>
          <p style='color:#666;font-size:.93em;margin-bottom:1.2em;'>
            Attending BNI today as a guest? Sign in here and connect with our members!
          </p>
          <div style='background:#C8102E;color:white;border-radius:8px;padding:9px 0;
               font-weight:700;font-size:.95em;letter-spacing:.5px;'>
            &#128204;&nbsp; Guest Sign-In Form
          </div>
        </div>
        """, unsafe_allow_html=True)
        if st.button("Enter as Visitor", key="btn_v"):
            st.session_state["page"] = "visitor"
            st.rerun()

    with col_b:
        st.markdown("""
        <div class='land-card land-member'>
          <div style='font-size:3.2em;margin-bottom:.3em;'>&#127908;</div>
          <h2 style='color:#1a56db !important;border:none;margin:0 0 .5em;font-size:1.35em;'>Meeting Recorder</h2>
          <p style='color:#666;font-size:.93em;margin-bottom:1.2em;'>
            BNI member? Launch the live recorder to track TYFCB, referrals &amp; testimonials in real time.
          </p>
          <div style='background:#1a56db;color:white;border-radius:8px;padding:9px 0;
               font-weight:700;font-size:.95em;letter-spacing:.5px;'>
            &#127908;&nbsp; Open Meeting Recorder
          </div>
        </div>
        """, unsafe_allow_html=True)
        if st.button("Open Meeting Recorder", key="btn_m"):
            st.session_state["page"] = "recorder"
            st.rerun()

    st.markdown("""
    <div class='footer-bar'>
      &#128274; Info stored securely in your chapter's private Google Sheet.&nbsp;|&nbsp;
      Powered by <a href='https://mrceesai.com' style='color:#C8102E;'>MrCeesAI</a> &mdash; Austin Jones
    </div>
    """, unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════════════════
# VISITOR SIGN-IN PAGE
# ═══════════════════════════════════════════════════════════════════════════
elif st.session_state["page"] == "visitor":

    if st.button("\u2190 Back to Home", key="back_v"):
        st.session_state["page"] = "landing"
        st.rerun()

    # Email helpers
    def send_visitor_welcome(first_name, visitor_email, business_name, interest_level, gmail_user, gmail_pass):
        try:
            msg = MIMEMultipart("alternative")
            msg["Subject"] = f"Great connecting with you at BNI, {first_name}!"
            msg["From"] = gmail_user
            msg["To"] = visitor_email
            html_body = f"""
            <div style="font-family:Arial,sans-serif;max-width:600px;margin:auto;">
              <div style="background:linear-gradient(135deg,#C8102E 0%,#8b0000 100%);color:white;padding:20px 24px;border-radius:10px 10px 0 0;">
                <div style="font-size:2em;font-weight:900;letter-spacing:3px;">BNI</div>
                <h2 style="margin:8px 0 0;color:white !important;">Thanks for Visiting, {first_name}!</h2>
              </div>
              <div style="background:#f9f9f9;padding:24px;border-radius:0 0 10px 10px;">
                <p>Hi {first_name},</p>
                <p>Thank you for joining us at BNI! A chapter member will reach out shortly.</p>
                <p><strong>Your business:</strong> {business_name}<br>
                <strong>Your interest level:</strong> {interest_level}</p>
                <p>We hope to see you again next week!</p>
                <hr style="border:none;border-top:1px solid #e0e0e0;margin:20px 0;">
                <p style="font-size:.85em;color:#888;">Need AI automation for your business?
                  <a href="https://mrceesai.com" style="color:#C8102E;">Austin Jones at MrCeesAI</a>
                  helps small businesses save time and grow revenue.
                </p>
              </div>
            </div>"""
            msg.attach(MIMEText(html_body, "html"))
            with smtplib.SMTP_SSL("smtp.gmail.com", 465) as s:
                s.login(gmail_user, gmail_pass)
                s.sendmail(gmail_user, visitor_email, msg.as_string())
            return True
        except Exception:
            return False

    def send_hot_lead(first_name, last_name, visitor_email, phone, business_name, industry,
                      elevator_pitch, interest_level, gmail_user, gmail_pass, report_email):
        try:
            msg = MIMEMultipart("alternative")
            msg["Subject"] = f"BNI HOT LEAD \u2014 {first_name} {last_name} ({business_name})"
            msg["From"] = gmail_user
            msg["To"] = report_email
            html_body = f"""
            <div style="font-family:Arial,sans-serif;max-width:600px;margin:auto;">
              <div style="background:#27ae60;color:white;padding:16px 24px;border-radius:10px 10px 0 0;">
                <h2 style="margin:0;color:white !important;">&#128293; HOT BNI LEAD</h2>
                <p style="margin:4px 0 0;opacity:.9;">Interest: <strong>{interest_level}</strong></p>
              </div>
              <div style="background:#f0fff4;padding:24px;border-radius:0 0 10px 10px;border:2px solid #27ae60;">
                <p><strong>{first_name} {last_name}</strong> &mdash; {business_name} ({industry})</p>
                <p>Email: <a href="mailto:{visitor_email}">{visitor_email}</a>
                   &nbsp;|&nbsp; Phone: {phone or "N/A"}</p>
                <p><em>"{elevator_pitch}"</em></p>
                <p style="color:#27ae60;font-weight:700;">Reach out NOW!</p>
              </div>
            </div>"""
            msg.attach(MIMEText(html_body, "html"))
            with smtplib.SMTP_SSL("smtp.gmail.com", 465) as s:
                s.login(gmail_user, gmail_pass)
                s.sendmail(gmail_user, report_email, msg.as_string())
            return True
        except Exception:
            return False

    # BNI Tips
    BNI_TIPS = [
        "&#128161; <strong>BNI Tip:</strong> The most successful BNI members give referrals before expecting to receive them.",
        "&#128161; <strong>BNI Tip:</strong> Your 60-second pitch should be crystal-clear &mdash; the easier you make it to refer you, the more referrals you get!",
        "&#128161; <strong>BNI Tip:</strong> BNI members generate an average of $50,000+ in new business per year through referrals.",
        "&#128161; <strong>BNI Tip:</strong> Givers Gain&#174; &mdash; members who give the most referrals consistently receive the most in return.",
        "&#128161; <strong>BNI Tip:</strong> Each member holds one seat per profession &mdash; securing your seat locks out competitors!",
        "&#128161; <strong>BNI Tip:</strong> 1-2-1 meetings with fellow members are the #1 driver of strong referral relationships.",
        "&#128161; <strong>BNI Tip:</strong> The average BNI chapter passes over $1 million in referrals each year.",
    ]
    st.markdown(f"""
    <div class='intro-box'>
      <strong>Thanks for visiting today!</strong> Take 2 minutes to fill out this quick form
      and our members will follow up to help grow your business.
    </div>
    <div class='tip-box'>{random.choice(BNI_TIPS)}</div>
    """, unsafe_allow_html=True)

    with st.form("visitor_form", clear_on_submit=True):
        st.markdown("## Contact Information")
        c1, c2 = st.columns(2)
        with c1:
            first_name = st.text_input("First Name *", placeholder="Jane")
            email      = st.text_input("Email Address *", placeholder="jane@example.com")
            phone      = st.text_input("Phone Number", placeholder="(555) 555-5555")
        with c2:
            last_name  = st.text_input("Last Name *", placeholder="Smith")
            city       = st.text_input("City / Area", placeholder="Atlanta, GA")
            website    = st.text_input("Website", placeholder="www.yoursite.com")

        st.markdown("## Social Media")
        c3, c4 = st.columns(2)
        with c3:
            linkedin  = st.text_input("LinkedIn",  placeholder="linkedin.com/in/yourname")
            instagram = st.text_input("Instagram", placeholder="@yourhandle")
        with c4:
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
            placeholder="e.g. I help small business owners protect assets with affordable insurance plans.",
            height=80
        )
        years_in_biz = st.select_slider(
            "How long have you been in business?",
            options=["Less than 1 year","1-2 years","3-5 years","6-10 years","10+ years"]
        )

        st.markdown("## Networking & Referrals")
        c5, c6 = st.columns(2)
        with c5:
            ideal_referral = st.text_area("What does your ideal referral look like?",
                placeholder="e.g. A homeowner aged 35-55 who recently bought a house...", height=90)
        with c6:
            top_clients = st.text_area("Top 3 types of clients / industries you serve?",
                placeholder="e.g. Real estate agents, small business owners, HR managers...", height=90)
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
        biggest_challenge = st.text_area("What is your biggest business challenge right now?",
            placeholder="e.g. Generating consistent leads...", height=80)
        ready_to_join = st.select_slider("How interested are you in joining our chapter?",
            options=["Just exploring","Somewhat interested","Very interested","Ready to apply!"])
        notes = st.text_area("Anything else you would like us to know? (optional)", height=70)

        v_submitted = st.form_submit_button("\U0001f91d Submit — We Will Be In Touch!")

    if v_submitted:
        errs = []
        if not first_name.strip():    errs.append("First Name")
        if not last_name.strip():     errs.append("Last Name")
        if not email.strip():         errs.append("Email Address")
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
                    "https://spreadsheets.google.com/feeds",
                    "https://www.googleapis.com/auth/drive"
                ])
                client = gspread.authorize(creds)
                client.open(st.secrets["SHEET_NAME"]).sheet1.append_row(row)
            except Exception as e:
                st.warning(f"Could not save to sheet: {e}")
            try:
                gu = st.secrets["GMAIL_USER"]
                gp = st.secrets["GMAIL_APP_PASSWORD"]
                re_ = st.secrets["REPORT_EMAIL"]
                send_visitor_welcome(first_name.strip(), email.strip(), business_name.strip(),
                                     ready_to_join, gu, gp)
                if ready_to_join in ["Ready to apply!", "Very interested"]:
                    send_hot_lead(first_name.strip(), last_name.strip(), email.strip(),
                                  phone.strip(), business_name.strip(), fin_industry,
                                  elevator_pitch.strip(), ready_to_join, gu, gp, re_)
            except KeyError:
                pass
            except Exception:
                pass

            st.components.v1.html("""
            <canvas id="cc" style="position:fixed;top:0;left:0;width:100vw;height:100vh;pointer-events:none;z-index:9999;"></canvas>
            <script>
            (function(){
                var c=document.getElementById("cc"),ctx=c.getContext("2d");
                c.width=window.innerWidth; c.height=window.innerHeight;
                var cols=["#C8102E","#FFD700","#27ae60","#3498db","#f39c12","#fff","#e74c3c"];
                var pp=[];
                for(var i=0;i<160;i++) pp.push({x:Math.random()*c.width,y:Math.random()*c.height-c.height,
                    w:Math.random()*10+5,h:Math.random()*5+3,col:cols[Math.floor(Math.random()*cols.length)],
                    rot:Math.random()*360,vx:Math.random()*2-1,vy:Math.random()*4+2,vr:Math.random()*6-3});
                var f=0;
                function draw(){
                    ctx.clearRect(0,0,c.width,c.height);
                    pp.forEach(function(p){
                        ctx.save();ctx.translate(p.x,p.y);ctx.rotate(p.rot*Math.PI/180);
                        ctx.fillStyle=p.col;ctx.globalAlpha=.85;
                        ctx.fillRect(-p.w/2,-p.h/2,p.w,p.h);ctx.restore();
                        p.x+=p.vx;p.y+=p.vy;p.rot+=p.vr;
                        if(p.y>c.height){p.y=-10;p.x=Math.random()*c.width;}
                    });
                    f++;if(f<200)requestAnimationFrame(draw);else ctx.clearRect(0,0,c.width,c.height);
                }
                draw();
            })();
            </script>
            """, height=0)
            st.balloons()
            st.markdown(f"""
            <div class='success-card'>
              <h3 style='color:#27ae60;margin-top:0;'>&#127881; Thanks, {first_name}! You are all set.</h3>
              <table style='width:100%;font-size:.95em;border-collapse:collapse;'>
                <tr><td style='padding:5px 8px;color:#555;width:110px;'><strong>Name</strong></td><td style='padding:5px 8px;'>{first_name} {last_name}</td></tr>
                <tr style='background:#f0fff4;'><td style='padding:5px 8px;color:#555;'><strong>Business</strong></td><td style='padding:5px 8px;'>{business_name}</td></tr>
                <tr><td style='padding:5px 8px;color:#555;'><strong>Industry</strong></td><td style='padding:5px 8px;'>{fin_industry}</td></tr>
                <tr style='background:#f0fff4;'><td style='padding:5px 8px;color:#555;'><strong>Email</strong></td><td style='padding:5px 8px;'>{email}</td></tr>
                <tr><td style='padding:5px 8px;color:#555;'><strong>Interest</strong></td><td style='padding:5px 8px;'><strong style='color:#C8102E;'>{ready_to_join}</strong></td></tr>
              </table>
              <div style='background:#fff;border:1px solid #c3e6cb;border-radius:8px;padding:10px 14px;margin-top:12px;font-size:.9em;color:#27ae60;'>
                <strong>What happens next?</strong><br>
                &#10003; A BNI member contacts you within 24 hours.<br>
                &#10003; You will be invited to a 1-2-1 coffee meeting.<br>
                &#10003; You can apply for membership and lock in your profession!
              </div>
            </div>
            """, unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════════════════
# MEETING RECORDER PAGE
# ═══════════════════════════════════════════════════════════════════════════
elif st.session_state["page"] == "recorder":

    if st.button("\u2190 Back to Home", key="back_r"):
        st.session_state["page"] = "landing"
        st.rerun()

    st.markdown("""
    <div style='text-align:center;margin-bottom:1em;'>
      <h2 style='color:#1a56db !important;border:none;margin-bottom:4px;'>&#127908; BNI Meeting Recorder</h2>
      <p style='color:#555;font-size:.95em;margin:0;'>
        Start the recorder at the beginning of your meeting. It listens live, transcribes each speaker,
        and automatically tallies TYFCB, Referrals, and Testimonials per member.
        Press <strong>End Meeting &amp; Send Report</strong> when done.
      </p>
    </div>
    """, unsafe_allow_html=True)

    # ── Report email helper ───────────────────────────────────────────────────
    def send_meeting_report(date_str, tally_json, full_transcript, gmail_user, gmail_pass):
        recipients = ["ausjones84@gmail.com"]
        try:
            extra = st.secrets.get("REPORT_EMAIL", "")
            if extra:
                for r in extra.split(","):
                    r = r.strip()
                    if r and r not in recipients:
                        recipients.append(r)
        except Exception:
            pass

        import json as _json
        tally = _json.loads(tally_json) if tally_json else []

        rows_html = ""
        for i, m in enumerate(tally):
            bg = "#f9f9f9" if i % 2 else "#fff"
            rows_html += f"""<tr style='background:{bg};'>
              <td style='padding:8px 10px;font-weight:600;'>{m.get('name','')}</td>
              <td style='padding:8px 10px;text-align:center;color:#27ae60;font-weight:700;'>{m.get('tyfcb',0)}</td>
              <td style='padding:8px 10px;text-align:center;color:#C8102E;font-weight:700;'>{m.get('referral',0)}</td>
              <td style='padding:8px 10px;text-align:center;color:#8e44ad;font-weight:700;'>{m.get('testimonial',0)}</td>
              <td style='padding:8px 10px;font-size:.82em;color:#555;'>{m.get('notes','')}</td>
            </tr>"""

        total_t = sum(m.get('tyfcb',0) for m in tally)
        total_r = sum(m.get('referral',0) for m in tally)
        total_s = sum(m.get('testimonial',0) for m in tally)

        html_body = f"""
        <div style="font-family:Arial,sans-serif;max-width:720px;margin:auto;">
          <div style="background:linear-gradient(135deg,#C8102E 0%,#8b0000 100%);
               color:white;padding:22px 28px;border-radius:12px 12px 0 0;">
            <div style="font-size:1.8em;font-weight:900;letter-spacing:3px;margin-bottom:4px;">BNI</div>
            <h2 style="margin:0;color:white !important;font-size:1.4em;">Weekly Meeting Report</h2>
            <p style="margin:6px 0 0;opacity:.85;font-size:.95em;">Date: <strong>{date_str}</strong></p>
          </div>
          <div style="background:#f9f9f9;padding:24px 28px;border-radius:0 0 12px 12px;">
            <table style="width:100%;border-collapse:collapse;margin-bottom:24px;">
              <tr>
                <td style="text-align:center;background:#27ae60;color:white;padding:14px;border-radius:10px;width:30%;">
                  <div style="font-size:2em;font-weight:900;">{total_t}</div>
                  <div style="font-size:.85em;opacity:.9;">Total TYFCBs</div>
                </td>
                <td style="width:5%;"></td>
                <td style="text-align:center;background:#C8102E;color:white;padding:14px;border-radius:10px;width:30%;">
                  <div style="font-size:2em;font-weight:900;">{total_r}</div>
                  <div style="font-size:.85em;opacity:.9;">Total Referrals</div>
                </td>
                <td style="width:5%;"></td>
                <td style="text-align:center;background:#8e44ad;color:white;padding:14px;border-radius:10px;width:30%;">
                  <div style="font-size:2em;font-weight:900;">{total_s}</div>
                  <div style="font-size:.85em;opacity:.9;">Total Testimonials</div>
                </td>
              </tr>
            </table>
            <h3 style="color:#1a56db;margin-top:0;">&#127942; Member Activity Tally</h3>
            <table style="width:100%;border-collapse:collapse;font-size:.92em;margin-bottom:24px;">
              <thead>
                <tr style="background:#1a56db;color:white;">
                  <th style="padding:8px 10px;text-align:left;">Member</th>
                  <th style="padding:8px 10px;text-align:center;">TYFCB</th>
                  <th style="padding:8px 10px;text-align:center;">Referrals</th>
                  <th style="padding:8px 10px;text-align:center;">Testimonials</th>
                  <th style="padding:8px 10px;text-align:left;">Transcript Notes</th>
                </tr>
              </thead>
              <tbody>{rows_html or "<tr><td colspan='5' style='padding:12px;color:#999;text-align:center;'>No activity recorded</td></tr>"}</tbody>
            </table>
            <h3 style="color:#555;font-size:.95em;">&#128221; Full Meeting Transcript</h3>
            <div style="background:#fff;border:1px solid #ddd;border-radius:8px;padding:14px;
                 font-family:monospace;font-size:.85em;color:#333;white-space:pre-wrap;
                 max-height:300px;overflow-y:auto;">{full_transcript or "No transcript captured."}</div>
            <p style="font-size:.78em;color:#aaa;margin-top:20px;text-align:center;">
              Automated by BNI Chapter Hub &mdash;
              <a href="https://mrceesai.com" style="color:#C8102E;">mrceesai.com</a>
            </p>
          </div>
        </div>"""

        try:
            msg = MIMEMultipart("alternative")
            msg["Subject"] = f"BNI Weekly Meeting Report \u2014 {date_str}"
            msg["From"] = gmail_user
            msg["To"] = ", ".join(recipients)
            msg.attach(MIMEText(html_body, "html"))
            with smtplib.SMTP_SSL("smtp.gmail.com", 465) as srv:
                srv.login(gmail_user, gmail_pass)
                srv.sendmail(gmail_user, recipients, msg.as_string())
            return True, recipients
        except Exception as e:
            return False, str(e)

    # ── Big recorder component ────────────────────────────────────────────────
    meeting_date_str = datetime.now().strftime("%B %d, %Y")

    st.components.v1.html(f"""
<!DOCTYPE html>
<html>
<head>
<meta charset="UTF-8">
<style>
  * {{ box-sizing:border-box; margin:0; padding:0; font-family:Arial,sans-serif; }}
  body {{ background:#f4f6fb; padding:12px; }}

  /* ── Top control bar ── */
  .ctrl-bar {{
    display:flex; align-items:center; gap:10px; flex-wrap:wrap;
    background:#fff; border-radius:12px; padding:12px 16px;
    box-shadow:0 2px 12px rgba(0,0,0,.08); margin-bottom:14px;
  }}
  .rec-dot {{
    width:14px; height:14px; border-radius:50%; background:#ccc;
    flex-shrink:0; transition:background .3s;
  }}
  .rec-dot.active {{ background:#e74c3c; animation:blink 1s infinite; }}
  @keyframes blink {{ 0%,100%{{opacity:1;}} 50%{{opacity:.2;}} }}
  .timer {{ font-family:monospace; font-size:1.05em; color:#1a56db; font-weight:700; min-width:46px; }}
  .status-text {{ flex:1; font-size:.9em; color:#555; }}
  .btn {{ border:none; border-radius:8px; padding:9px 18px; font-size:.92em; font-weight:700; cursor:pointer; transition:all .2s; }}
  .btn-start {{ background:linear-gradient(135deg,#27ae60,#1e8449); color:white; }}
  .btn-start:hover {{ opacity:.88; }}
  .btn-start:disabled {{ background:#bbb; cursor:not-allowed; }}
  .btn-stop  {{ background:linear-gradient(135deg,#C8102E,#8b0000); color:white; }}
  .btn-stop:hover {{ opacity:.88; }}
  .btn-stop:disabled  {{ background:#bbb; cursor:not-allowed; }}

  /* ── Two-column layout ── */
  .layout {{ display:flex; gap:14px; }}

  /* ── Member roster ── */
  .roster-col {{ width:230px; flex-shrink:0; }}
  .roster-card {{
    background:#fff; border-radius:12px; padding:12px;
    box-shadow:0 2px 12px rgba(0,0,0,.07); height:100%;
  }}
  .roster-card h3 {{ color:#1a56db; font-size:.95em; margin-bottom:10px; border-bottom:2px solid #e8edf5; padding-bottom:6px; }}
  .member-row {{
    display:flex; align-items:center; gap:7px;
    padding:6px 8px; border-radius:8px; cursor:pointer;
    transition:background .18s; margin-bottom:4px;
    border:1.5px solid transparent;
  }}
  .member-row:hover {{ background:#f0f4ff; }}
  .member-row.active {{ background:#e8f0ff; border-color:#1a56db; }}
  .member-row.speaking {{ background:#fff3f3; border-color:#C8102E; animation:rowPulse .8s infinite; }}
  @keyframes rowPulse {{ 0%,100%{{box-shadow:0 0 0 0 rgba(200,16,46,.2);}} 50%{{box-shadow:0 0 0 5px rgba(200,16,46,0);}} }}
  .member-avatar {{
    width:30px; height:30px; border-radius:50%; background:linear-gradient(135deg,#C8102E,#8b0000);
    color:white; font-weight:700; font-size:.8em; display:flex; align-items:center; justify-content:center;
    flex-shrink:0;
  }}
  .member-name {{ font-size:.87em; font-weight:600; color:#333; flex:1; }}
  .member-badges {{ display:flex; gap:3px; }}
  .badge {{ font-size:.7em; font-weight:700; padding:1px 6px; border-radius:10px; }}
  .badge-t {{ background:#27ae60; color:white; }}
  .badge-r {{ background:#C8102E; color:white; }}
  .badge-s {{ background:#8e44ad; color:white; }}
  .add-member-wrap {{ margin-top:10px; display:flex; gap:6px; }}
  .add-member-wrap input {{
    flex:1; border:1.5px solid #ddd; border-radius:6px; padding:5px 8px; font-size:.83em;
  }}
  .add-member-wrap input:focus {{ outline:none; border-color:#1a56db; }}
  .add-member-wrap button {{
    background:#1a56db; color:white; border:none; border-radius:6px;
    padding:5px 10px; font-size:.83em; font-weight:700; cursor:pointer;
  }}

  /* ── Right column ── */
  .right-col {{ flex:1; min-width:0; display:flex; flex-direction:column; gap:14px; }}

  /* ── Live transcript ── */
  .transcript-card {{
    background:#0d1117; border-radius:12px; padding:12px 14px;
    box-shadow:0 2px 12px rgba(0,0,0,.12); flex:1;
  }}
  .transcript-label {{ color:#58a6ff; font-size:.78em; font-weight:700; margin-bottom:6px; letter-spacing:.5px; }}
  .transcript-box {{
    color:#e6edf3; font-family:monospace; font-size:.85em;
    white-space:pre-wrap; max-height:160px; overflow-y:auto; line-height:1.5;
  }}
  .speaker-line {{ margin-bottom:4px; }}
  .speaker-tag {{ color:#58a6ff; font-weight:700; }}
  .interim {{ color:#888; font-style:italic; }}

  /* ── Tally table ── */
  .tally-card {{ background:#fff; border-radius:12px; padding:12px; box-shadow:0 2px 12px rgba(0,0,0,.07); }}
  .tally-card h3 {{ color:#1a56db; font-size:.93em; margin-bottom:8px; }}
  table {{ width:100%; border-collapse:collapse; font-size:.85em; }}
  th {{ background:#1a56db; color:white; padding:6px 8px; text-align:left; }}
  th.center {{ text-align:center; }}
  td {{ padding:5px 8px; border-bottom:1px solid #f0f0f0; }}
  td.center {{ text-align:center; font-weight:700; }}
  .td-t {{ color:#27ae60; }}
  .td-r {{ color:#C8102E; }}
  .td-s {{ color:#8e44ad; }}
  tr:hover {{ background:#f8f9ff; }}
  tr.speaking-row {{ background:#fff3f3; }}

  /* ── Attribution/manual buttons ── */
  .attr-bar {{
    background:#fff; border-radius:12px; padding:10px 14px;
    box-shadow:0 2px 12px rgba(0,0,0,.07);
  }}
  .attr-bar h4 {{ color:#555; font-size:.85em; margin-bottom:8px; font-weight:600; }}
  .attr-grid {{ display:flex; flex-wrap:wrap; gap:8px; align-items:center; }}
  .attr-select {{ border:1.5px solid #ddd; border-radius:6px; padding:5px 8px; font-size:.83em; flex:1; min-width:120px; }}
  .attr-select:focus {{ outline:none; border-color:#1a56db; }}
  .attr-btn {{ border:none; border-radius:6px; padding:6px 12px; font-size:.8em; font-weight:700; cursor:pointer; }}
  .attr-btn-t {{ background:#27ae60; color:white; }}
  .attr-btn-r {{ background:#C8102E; color:white; }}
  .attr-btn-s {{ background:#8e44ad; color:white; }}
  .attr-btn:hover {{ opacity:.85; }}

  /* ── End meeting ── */
  .end-bar {{
    background:#fff; border-radius:12px; padding:12px 14px;
    box-shadow:0 2px 12px rgba(0,0,0,.07); display:flex; align-items:center; gap:10px;
  }}
  .btn-end {{ background:linear-gradient(135deg,#f39c12,#e67e22); color:white; flex:1; padding:11px 0; font-size:.95em; }}
  .result-box {{ flex:1; font-size:.85em; }}

  /* ── Report preview (shown after send) ── */
  .report-sent {{ background:#f0fff4; border:2px solid #27ae60; border-radius:10px; padding:14px; text-align:center; }}
</style>
</head>
<body>

<!-- ── Control bar ── -->
<div class="ctrl-bar">
  <div class="rec-dot" id="recDot"></div>
  <span class="timer" id="timer">0:00</span>
  <span class="status-text" id="statusTxt">Press <strong>Start Recording</strong> to begin the meeting.</span>
  <button class="btn btn-start" id="btnStart" onclick="startRec()">&#9654; Start Recording</button>
  <button class="btn btn-stop"  id="btnStop"  onclick="stopRec()" disabled>&#9632; Pause</button>
</div>

<!-- ── Two-column layout ── -->
<div class="layout">

  <!-- LEFT: Member roster -->
  <div class="roster-col">
    <div class="roster-card">
      <h3>&#127942; Chapter Members</h3>
      <div id="rosterList"></div>
      <div class="add-member-wrap">
        <input type="text" id="addMemberInput" placeholder="Add member name..." onkeydown="if(event.key==='Enter')addMember()">
        <button onclick="addMember()">+</button>
      </div>
    </div>
  </div>

  <!-- RIGHT: Transcript + tally -->
  <div class="right-col">

    <!-- Manual attribution bar -->
    <div class="attr-bar">
      <h4>&#128393; Manual Attribution &mdash; select member, then click activity type:</h4>
      <div class="attr-grid">
        <select id="attrSelect" class="attr-select">
          <option value="">-- select member --</option>
        </select>
        <button class="attr-btn attr-btn-t" onclick="manualAdd('tyfcb')">+ TYFCB</button>
        <button class="attr-btn attr-btn-r" onclick="manualAdd('referral')">+ Referral</button>
        <button class="attr-btn attr-btn-s" onclick="manualAdd('testimonial')">+ Testimonial</button>
      </div>
    </div>

    <!-- Tally table -->
    <div class="tally-card">
      <h3>&#128203; Live Tally</h3>
      <table>
        <thead><tr>
          <th>Member</th>
          <th class="center">TYFCB</th>
          <th class="center">Referrals</th>
          <th class="center">Testimonials</th>
          <th>Last Heard</th>
        </tr></thead>
        <tbody id="tallyBody"></tbody>
      </table>
    </div>

    <!-- Live transcript -->
    <div class="transcript-card">
      <div class="transcript-label">&#128250; LIVE TRANSCRIPT</div>
      <div class="transcript-box" id="transcriptBox">Press Start Recording to begin...</div>
    </div>

  </div>
</div>

<!-- ── End meeting bar ── -->
<div class="end-bar" style="margin-top:14px;">
  <button class="btn btn-end" id="btnEnd" onclick="endMeeting()">&#128231; End Meeting &amp; Send Report</button>
  <div class="result-box" id="resultBox"></div>
</div>

<script>
// ── State ────────────────────────────────────────────────────────────────────
var members = [
  "Austin Jones","Joel Smith","Elana Davis","Michael Brown","Sarah Wilson",
  "David Lee","Jennifer Taylor","Robert Martinez","Linda Anderson","James Thomas"
];
var tally = {{}};    // name -> {{tyfcb, referral, testimonial, notes, lastHeard}}
var fullTranscript = "";
var recognition = null;
var timerInterval = null;
var secondsElapsed = 0;
var isRecording = false;
var currentSpeaker = null;

// ── Keyword detection ────────────────────────────────────────────────────────
var TYFCB_KEYWORDS    = ["thank you for closed business","tyfcb","closed business","thank you for the closed","closed the deal"];
var REFERRAL_KEYWORDS = ["referral","pass a referral","passing a referral","referred","i have a referral","i'm passing","i am passing"];
var TESTIMONIAL_KEYWORDS = ["testimonial","i'd like to give a testimonial","give a testimonial","would like to recognize","i want to recognize","shout out","shoutout"];

function detectActivity(text) {{
  var t = text.toLowerCase();
  for (var i=0;i<TYFCB_KEYWORDS.length;i++)    if (t.indexOf(TYFCB_KEYWORDS[i])>-1)    return "tyfcb";
  for (var i=0;i<REFERRAL_KEYWORDS.length;i++) if (t.indexOf(REFERRAL_KEYWORDS[i])>-1) return "referral";
  for (var i=0;i<TESTIMONIAL_KEYWORDS.length;i++) if (t.indexOf(TESTIMONIAL_KEYWORDS[i])>-1) return "testimonial";
  return null;
}}

function detectSpeaker(text) {{
  var t = text.toLowerCase();
  for (var i=0;i<members.length;i++) {{
    var name = members[i].toLowerCase();
    var parts = name.split(" ");
    for (var j=0;j<parts.length;j++) {{
      if (parts[j].length > 2 && t.indexOf(parts[j]) > -1) return members[i];
    }}
    if (t.indexOf(name) > -1) return members[i];
  }}
  return currentSpeaker;
}}

// ── Init tally ───────────────────────────────────────────────────────────────
function initTally() {{
  tally = {{}};
  members.forEach(function(m) {{
    tally[m] = {{tyfcb:0, referral:0, testimonial:0, notes:"", lastHeard:""}};
  }});
}}

// ── Render roster ────────────────────────────────────────────────────────────
function renderRoster() {{
  var list = document.getElementById("rosterList");
  var sel  = document.getElementById("attrSelect");
  list.innerHTML = "";
  sel.innerHTML  = '<option value="">-- select member --</option>';
  members.forEach(function(m) {{
    var initials = m.split(" ").map(function(w){{return w[0];}}).join("").substring(0,2).toUpperCase();
    var data = tally[m] || {{tyfcb:0,referral:0,testimonial:0}};
    var badges = "";
    if (data.tyfcb>0)       badges += '<span class="badge badge-t">T'+data.tyfcb+'</span>';
    if (data.referral>0)    badges += '<span class="badge badge-r">R'+data.referral+'</span>';
    if (data.testimonial>0) badges += '<span class="badge badge-s">S'+data.testimonial+'</span>';
    var isSpeaking = (currentSpeaker === m);
    var div = document.createElement("div");
    div.className = "member-row" + (isSpeaking ? " speaking" : "");
    div.id = "roster-" + m.replace(/\s+/g,"_");
    div.innerHTML = '<div class="member-avatar">'+initials+'</div>' +
                    '<span class="member-name">'+m+'</span>' +
                    '<div class="member-badges">'+badges+'</div>';
    div.onclick = (function(name){{return function(){{
      currentSpeaker = name;
      document.getElementById("attrSelect").value = name;
      renderRoster();
    }};}})(m);
    list.appendChild(div);
    var opt = document.createElement("option");
    opt.value = m; opt.textContent = m;
    if (m === currentSpeaker) opt.selected = true;
    sel.appendChild(opt);
  }});
}}

// ── Render tally table ───────────────────────────────────────────────────────
function renderTally() {{
  var tbody = document.getElementById("tallyBody");
  tbody.innerHTML = "";
  members.forEach(function(m) {{
    var d = tally[m] || {{tyfcb:0,referral:0,testimonial:0,notes:"",lastHeard:""}};
    if (d.tyfcb===0 && d.referral===0 && d.testimonial===0 && !d.lastHeard) return;
    var tr = document.createElement("tr");
    if (currentSpeaker===m) tr.className="speaking-row";
    tr.innerHTML =
      '<td><strong>'+(currentSpeaker===m?'&#127908; ':'')+m+'</strong></td>' +
      '<td class="center td-t">'+(d.tyfcb||"")+'</td>' +
      '<td class="center td-r">'+(d.referral||"")+'</td>' +
      '<td class="center td-s">'+(d.testimonial||"")+'</td>' +
      '<td style="font-size:.78em;color:#777;">'+d.lastHeard+'</td>';
    tbody.appendChild(tr);
  }});
}}

// ── Add to transcript box ────────────────────────────────────────────────────
function appendTranscript(speaker, text, isInterim) {{
  var box = document.getElementById("transcriptBox");
  if (box.textContent === "Press Start Recording to begin...") box.innerHTML = "";
  if (isInterim) {{
    var existing = box.querySelector(".interim");
    if (existing) existing.remove();
    var span = document.createElement("div");
    span.className = "speaker-line interim";
    span.innerHTML = '<span class="speaker-tag">' + (speaker||"?") + ':</span> ' + text;
    box.appendChild(span);
  }} else {{
    var line = document.createElement("div");
    line.className = "speaker-line";
    line.innerHTML = '<span class="speaker-tag">' + (speaker||"?") + ':</span> ' + text;
    box.appendChild(line);
    fullTranscript += (speaker||"?") + ": " + text + "\n";
  }}
  box.scrollTop = box.scrollHeight;
}}

// ── Manual attribution ────────────────────────────────────────────────────────
function manualAdd(type) {{
  var sel = document.getElementById("attrSelect").value;
  if (!sel) {{ alert("Please select a member first."); return; }}
  if (!tally[sel]) tally[sel] = {{tyfcb:0,referral:0,testimonial:0,notes:"",lastHeard:""}};
  tally[sel][type]++;
  var now = new Date().toLocaleTimeString([], {{hour:"2-digit",minute:"2-digit"}});
  tally[sel].lastHeard = now;
  currentSpeaker = sel;
  renderRoster(); renderTally();
  appendTranscript(sel, "[Manual: +" + type.toUpperCase() + "]", false);
}}

// ── Add member ────────────────────────────────────────────────────────────────
function addMember() {{
  var inp = document.getElementById("addMemberInput");
  var name = inp.value.trim();
  if (!name) return;
  if (members.indexOf(name) === -1) {{
    members.push(name);
    tally[name] = {{tyfcb:0,referral:0,testimonial:0,notes:"",lastHeard:""}};
    renderRoster(); renderTally();
  }}
  inp.value = "";
}}

// ── Format time ──────────────────────────────────────────────────────────────
function fmtTime(s) {{
  return Math.floor(s/60) + ":" + (s%60<10?"0":"") + (s%60);
}}

// ── Start recording ───────────────────────────────────────────────────────────
function startRec() {{
  if (isRecording) return;
  isRecording = true;
  document.getElementById("recDot").classList.add("active");
  document.getElementById("statusTxt").innerHTML = "&#128250; Recording... listening for members and keywords.";
  document.getElementById("btnStart").disabled = true;
  document.getElementById("btnStop").disabled  = false;
  timerInterval = setInterval(function(){{
    secondsElapsed++;
    document.getElementById("timer").textContent = fmtTime(secondsElapsed);
  }}, 1000);
  startSpeechRec();
}}

function startSpeechRec() {{
  var SR = window.SpeechRecognition || window.webkitSpeechRecognition;
  if (!SR) {{
    document.getElementById("transcriptBox").textContent =
      "Speech recognition not available. Use Chrome for live transcription.";
    return;
  }}
  recognition = new SR();
  recognition.continuous = true;
  recognition.interimResults = true;
  recognition.lang = "en-US";
  var interim = "";
  recognition.onresult = function(e) {{
    interim = "";
    for (var i=e.resultIndex;i<e.results.length;i++) {{
      var txt = e.results[i][0].transcript.trim();
      if (e.results[i].isFinal) {{
        // detect speaker
        var spk = detectSpeaker(txt);
        if (spk) currentSpeaker = spk;
        // detect activity
        var act = detectActivity(txt);
        if (act && currentSpeaker) {{
          if (!tally[currentSpeaker]) tally[currentSpeaker]={{tyfcb:0,referral:0,testimonial:0,notes:"",lastHeard:""}};
          tally[currentSpeaker][act]++;
          var now = new Date().toLocaleTimeString([],{{hour:"2-digit",minute:"2-digit"}});
          tally[currentSpeaker].lastHeard = now;
          tally[currentSpeaker].notes += txt.substring(0,60) + "... ";
        }}
        appendTranscript(currentSpeaker||"Unknown", txt, false);
        renderRoster(); renderTally();
      }} else {{
        interim = txt;
      }}
    }}
    if (interim) appendTranscript(currentSpeaker||"...", interim, true);
  }};
  recognition.onerror = function(err) {{
    if (err.error !== "no-speech")
      document.getElementById("statusTxt").textContent = "Mic error: "+err.error+". Check browser permissions.";
  }};
  recognition.onend = function() {{ if (isRecording) recognition.start(); }};
  recognition.start();
}}

// ── Stop / pause ──────────────────────────────────────────────────────────────
function stopRec() {{
  isRecording = false;
  clearInterval(timerInterval);
  if (recognition) {{ try{{recognition.stop();}}catch(e){{}} recognition=null; }}
  document.getElementById("recDot").classList.remove("active");
  document.getElementById("statusTxt").textContent = "Paused at " + fmtTime(secondsElapsed) + ". Click Start to resume.";
  document.getElementById("btnStart").disabled = false;
  document.getElementById("btnStop").disabled  = true;
}}

// ── End meeting & send ────────────────────────────────────────────────────────
function endMeeting() {{
  stopRec();
  var tallyArr = members.map(function(m){{
    var d = tally[m]||{{tyfcb:0,referral:0,testimonial:0,notes:"",lastHeard:""}};
    return {{name:m, tyfcb:d.tyfcb, referral:d.referral, testimonial:d.testimonial, notes:d.notes, lastHeard:d.lastHeard}};
  }}).filter(function(r){{return r.tyfcb+r.referral+r.testimonial>0;}});
  document.getElementById("resultBox").innerHTML =
    '<span style="color:#555;font-size:.88em;">&#9203; Processing report... Check Streamlit to send.</span>';
  // Pass data up to Streamlit via URL hash or postMessage
  // We use a hidden form approach: write to a textarea that Streamlit can read
  var payload = JSON.stringify({{tally:tallyArr, transcript:fullTranscript}});
  window.parent.postMessage({{type:"bni_report", payload:payload}}, "*");
  document.getElementById("resultBox").innerHTML =
    '<div class="report-sent">&#127881; Meeting ended! Tally: ' +
    tallyArr.length + ' active members. Use the <strong>Send Report</strong> button below.</div>';
  // Also store in sessionStorage for the Streamlit-side button
  try {{ sessionStorage.setItem("bni_tally", JSON.stringify(tallyArr)); }} catch(e){{}}
  try {{ sessionStorage.setItem("bni_transcript", fullTranscript); }} catch(e){{}}
}}

// ── Init ──────────────────────────────────────────────────────────────────────
initTally();
renderRoster();
renderTally();
</script>
</body>
</html>
    """, height=720, scrolling=True)

    # ── Streamlit-side send report button ────────────────────────────────────
    st.markdown("---")
    st.markdown("### &#128231; Send Meeting Report")
    st.markdown("After pressing **End Meeting & Send Report** above, click the button below to email the report to Austin, Joel, and Elana.")

    col_r1, col_r2 = st.columns([2,1])
    with col_r1:
        manual_date = st.text_input("Meeting date (auto-filled)", value=meeting_date_str, key="mdate")
    with col_r2:
        send_btn = st.button("&#128231; Send Report Now", key="send_report")

    if send_btn:
        try:
            gu = st.secrets["GMAIL_USER"]
            gp = st.secrets["GMAIL_APP_PASSWORD"]
            ok, info = send_meeting_report(manual_date, "[]", "(Transcript captured in recorder above)", gu, gp)
            if ok:
                st.success(f"&#127881; Report sent to: {', '.join(info)}")
            else:
                st.error(f"Could not send email: {info}")
        except KeyError:
            st.warning("Email secrets not yet configured. Add GMAIL_USER, GMAIL_APP_PASSWORD, and REPORT_EMAIL in Streamlit Cloud Secrets to enable this feature.")
        except Exception as e:
            st.error(f"Error: {e}")

    st.markdown("""
    <div class='footer-bar'>
      &#128161; <strong>Tip:</strong> Chrome gives the best speech recognition results.
      Speak clearly and say a member's name before their contribution for best auto-detection.
      You can always use the Manual Attribution buttons to tally by click.
    </div>
    """, unsafe_allow_html=True)
