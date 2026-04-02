# BNI Visitor Intake Form
> AI-powered guest registration with automated weekly email report

A clean, branded Streamlit web app for BNI chapters to capture visitor information. Share one link — visitors fill it out, data goes to a Google Sheet, and you get a beautiful weekly report every Monday at 8:30 AM (right after your meeting ends).

## What It Does
- Branded form with BNI red theme
- Captures contact info, social media, business details, networking goals, and interest level
- Saves every submission to a Google Sheet automatically
- Sends a formatted HTML email report every Monday at 8:30 AM EST (after your 7-9 AM meeting)
- Can also be triggered manually from the GitHub Actions tab anytime

## Deploy in 5 Steps

### Step 1 — Set up Google Sheet
1. Create a new Google Sheet named `BNI Visitors`
2. Add this header row (row 1):
```
Timestamp | First Name | Last Name | Email | Phone | City | Website | LinkedIn | Instagram | Facebook | X/Twitter | Business Name | Industry | Elevator Pitch | Years in Business | Ideal Referral | Top Clients | How Heard | Invited By | Looking For | BNI Experience | Biggest Challenge | Interest Level | Notes
```
3. Go to [console.cloud.google.com](https://console.cloud.google.com)
4. Create a new project > Enable **Google Sheets API** and **Google Drive API**
5. Create a **Service Account** > Download the JSON key
6. Share your Google Sheet with the service account email (Editor access)

### Step 2 — Deploy to Streamlit Cloud (Free)
1. Go to [share.streamlit.io](https://share.streamlit.io)
2. Connect your GitHub account
3. Select repo: `ausjones84/bni-visitor-intake` and main file: `app.py`
4. Click **Deploy**
5. In the app settings, go to **Secrets** and paste:
```toml
GOOGLE_CREDS = '''{ paste your entire service account JSON here }'''
SHEET_NAME = "BNI Visitors"
```

### Step 3 — Add GitHub Secrets for the Weekly Report
In your repo > **Settings** > **Secrets and variables** > **Actions**, add:

| Secret Name | Value |
|---|---|
| `GOOGLE_CREDS` | Paste the full service account JSON |
| `SHEET_NAME` | `BNI Visitors` |
| `REPORT_EMAIL` | Email address to receive the weekly report |
| `GMAIL_USER` | Your Gmail address |
| `GMAIL_APP_PASSWORD` | Gmail App Password (Google Account > Security > 2-Step > App Passwords) |

### Step 4 — Share Your Link
Your Streamlit URL will look like:
```
https://ausjones84-bni-visitor-intake-app-xxxxx.streamlit.app
```
Share this link in your BNI chapter — visitors can fill it out on any device.

### Step 5 — Run the Report Manually (optional)
Go to **Actions** tab > **Weekly BNI Visitor Report** > **Run workflow** to trigger the report at any time.

## Report Schedule
- Runs automatically every **Monday at 8:30 AM EST**
- Right after your 7:00–8:30 AM BNI meeting
- Reports cover the past 7 days of submissions

## Tech Stack
| Component | Technology |
|---|---|
| UI / Form | Streamlit |
| Styling | Custom CSS (BNI Red theme) |
| Data Storage | Google Sheets (via gspread) |
| Scheduler | GitHub Actions (cron) |
| Email | Gmail SMTP + HTML template |
| Hosting | Streamlit Community Cloud (free) |

---
Built by **ausjones84** · Powered by Python + Streamlit + GitHub Actions
