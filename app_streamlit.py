import streamlit as st
import smtplib
import ssl
import pandas as pd
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

# --- Helper Functions ---

def load_personal_credentials():
    # Loads sender email and App Password securely from Streamlit secrets
    try:
        sender_email = st.secrets["email_credentials"]["sender_email"]
        sender_password = st.secrets["email_credentials"]["app_password"]
        return {sender_email: sender_password}
    except KeyError:
        return {}

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
st.title("Bulk Email Sender Utility 🚀")

# Load and verify sender account
accounts = load_personal_credentials()
account_choices = list(accounts.keys())

# --- Section 1: Sender Account Status ---
st.header("1. Sender Account Status")

if accounts:
    selected_account = account_choices[0]
    st.success(f"Sender account loaded securely: {selected_account}")
else:
    st.error("Sender credentials not found. Please configure them in Streamlit Secrets.")
    selected_account = None

st.divider()

# --- Section 2: Compose Email ---
st.header("2. Compose Email")
subject = st.text_input("Email Subject")

use_html = st.checkbox("Use HTML template for email body?")
if use_html:
    email_body = st.text_area("HTML Content", height=300, help="Paste your HTML code here.")
else:
    email_body = st.text_area("Plain Text Content", height=200, help="Enter your email message here.")

st.divider()

# --- Section 3: Recipient List ---
st.header("3. Upload Recipient List")
uploaded_file = st.file_uploader("Upload an Excel file (.xlsx) with recipient emails in the **first column**.", type=["xlsx"])
if uploaded_file:
    try:
        df = pd.read_excel(uploaded_file)
        # Assuming the first column (index 0) contains the emails
        recipients = df.iloc[:, 0].dropna().tolist()
        st.success(f"Loaded {len(recipients)} recipients.")
    except Exception as e:
        st.error(f"Error reading file: {e}")
        recipients = []
else:
    recipients = []

st.divider()

# --- Section 4: Send Emails ---
st.header("4. Send Emails")

if not selected_account:
    st.warning("Cannot send. Secure sender account not available.")
else:
    # Button is disabled unless all inputs are ready
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
                    # Specific error guidance for authentication failure
                    st.error(f"Failed to send from {selected_account}. Check your App Password in Streamlit Secrets and ensure 2FA is enabled.")