import streamlit as st
import smtplib
import ssl
import os
import pandas as pd
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

# File to store login credentials for multiple accounts
CREDENTIALS_FILE = "credentials.txt"

# --- Helper Functions (Same as above) ---
def load_credentials():
    if not os.path.exists(CREDENTIALS_FILE):
        return {}
    accounts = {}
    with open(CREDENTIALS_FILE, "r") as file:
        for line in file:
            try:
                email, password = line.strip().split(':')
                accounts[email] = password
            except ValueError:
                pass
    return accounts

def save_credentials(accounts):
    with open(CREDENTIALS_FILE, "w") as file:
        for email, password in accounts.items():
            file.write(f"{email}:{password}\n")

def send_email(sender_email, sender_password, recipient_list, subject, body, is_html=False):
    smtp_server = "smtp.gmail.com"
    port = 465
    context = ssl.create_default_context()
    
    try:
        with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
            server.login(sender_email, sender_password)
            for recipient in recipient_list:
                msg = MIMEMultipart("alternative")
                msg["Subject"] = subject
                msg["From"] = sender_email
                msg["To"] = recipient
                
                if is_html:
                    msg.attach(MIMEText(body, "html"))
                else:
                    msg.attach(MIMEText(body, "plain"))
                
                server.sendmail(sender_email, recipient, msg.as_string())
        return True
    except smtplib.SMTPAuthenticationError:
        return False
    except Exception as e:
        st.error(f"An error occurred while sending email from {sender_email}: {e}")
        return False

# --- Streamlit UI ---
st.title("Bulk Email Sender")

# Section 1: Manage Accounts
st.header("1. Manage Accounts")
st.markdown("Enter your Gmail address and App Password. You must have 2-Step Verification enabled to use an App Password.")
st.markdown("App Passwords can be generated from [your Google Account security settings](https://myaccount.google.com/security).")

with st.expander("Add New Account"):
    new_email = st.text_input("Gmail Address")
    new_password = st.text_input("App Password", type="password")
    if st.button("Add Account"):
        if new_email and new_password:
            accounts = load_credentials()
            accounts[new_email] = new_password
            save_credentials(accounts)
            st.success(f"Account {new_email} added.")
            st.experimental_rerun()
        else:
            st.warning("Please enter both email and password.")

accounts = load_credentials()
if accounts:
    st.success(f"Loaded {len(accounts)} email accounts.")
    account_choices = list(accounts.keys())
else:
    st.error("No email accounts loaded. Please add one.")
    account_choices = []

st.divider()

# Section 2: Email Content
st.header("2. Compose Email")
subject = st.text_input("Email Subject")

use_html = st.checkbox("Use HTML template for email body?")
if use_html:
    email_body = st.text_area("HTML Content", height=300, help="Paste your HTML code here.")
else:
    email_body = st.text_area("Plain Text Content", height=200, help="Enter your email message here.")

st.divider()

# Section 3: Recipient List
st.header("3. Upload Recipient List")
uploaded_file = st.file_uploader("Upload an Excel file (.xlsx) with recipient emails in the first column.", type=["xlsx"])
if uploaded_file:
    try:
        df = pd.read_excel(uploaded_file)
        recipients = df.iloc[:, 0].dropna().tolist()
        st.success(f"Loaded {len(recipients)} recipients.")
    except Exception as e:
        st.error(f"Error reading file: {e}")
        recipients = []
else:
    recipients = []

st.divider()

# Section 4: Send Emails
st.header("4. Send Emails")

if not account_choices:
    st.warning("Please add an account in Section 1 to enable sending.")
else:
    selected_account = st.selectbox("Select an account to send from:", account_choices)
    
    if st.button("Send Emails", type="primary", disabled=not recipients or not subject):
        if not recipients:
            st.error("Recipient list is empty.")
        elif not subject:
            st.error("Subject cannot be empty.")
        else:
            selected_password = accounts[selected_account]
            
            with st.spinner(f"Attempting to send emails from {selected_account}..."):
                if send_email(selected_account, selected_password, recipients, subject, email_body, is_html=use_html):
                    st.success(f"Successfully sent all emails from {selected_account}.")
                    st.balloons()
                else:
                    st.error(f"Failed to send from {selected_account}. Please check your credentials or try a different account.")