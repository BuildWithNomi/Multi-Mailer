import streamlit as st
import smtplib
import ssl
import pandas as pd
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

# --- CORE SENDING FUNCTION ---

# NOTE: Since credentials are now session-based, this function relies on
# the email and password being passed to it directly from the UI state.
def send_email(sender_email, sender_password, recipient_list, subject, body, is_html=False):
    """Sends emails using the provided user credentials."""
    smtp_server = "smtp.gmail.com"
    port = 465
    context = ssl.create_default_context()
    
    try:
        # Use a high timeout (30s) for potential network delays during bulk send
        with smtplib.SMTP_SSL(smtp_server, port, context=context, timeout=30) as server:
            server.login(sender_email, sender_password)
            
            # Send one email at a time for simplicity and control
            for recipient in recipient_list:
                msg = MIMEMultipart("alternative")
                msg["Subject"] = subject
                msg["From"] = sender_email
                msg["To"] = recipient
                
                if is_html:
                    # Attach both plain text (fallback) and HTML versions
                    msg.attach(MIMEText("Please enable HTML viewing.", "plain"))
                    msg.attach(MIMEText(body, "html"))
                else:
                    msg.attach(MIMEText(body, "plain"))
                
                server.sendmail(sender_email, recipient, msg.as_string())
            
        return True
    except smtplib.SMTPAuthenticationError:
        # Authentication failure is reported without crashing the app
        st.session_state.auth_error = True
        return False
    except Exception as e:
        st.session_state.generic_error = str(e)
        return False

# --- Streamlit UI Initialization ---

# Initialize session state for storing credentials and managing errors
if 'sender_email' not in st.session_state:
    st.session_state.sender_email = ""
if 'sender_password' not in st.session_state:
    st.session_state.sender_password = ""
if 'auth_error' not in st.session_state:
    st.session_state.auth_error = False
if 'generic_error' not in st.session_state:
    st.session_state.generic_error = ""


st.title("Bulk Email Sender (Public Multi-Mailer) 🚀")
st.caption("Enter your credentials for this session only. Nothing is saved.")

# --- Section 1: Sender Account Input ---
st.header("1. Your Sender Credentials")

with st.expander("Enter Your Credentials"):
    st.markdown("⚠️ **Warning:** You must use a **Gmail App Password**, not your main account password.")
    
    # Use a key to ensure Streamlit treats the input fields correctly on rerun
    email_input = st.text_input("Your Gmail Address", key="email_input")
    password_input = st.text_input("Your App Password", type="password", key="password_input")
    
    if st.button("Set Credentials for Session"):
        if email_input and password_input:
            st.session_state.sender_email = email_input
            st.session_state.sender_password = password_input
            st.session_state.auth_error = False
            st.session_state.generic_error = ""
            st.success("Credentials saved for this session.")
        else:
            st.warning("Please enter both email and password.")

# Display current status
if st.session_state.sender_email:
    st.info(f"Current Sender: **{st.session_state.sender_email}**")
else:
    st.warning("Please set your credentials above to enable sending.")

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
        recipients = df.iloc[:, 0].dropna().tolist()
        st.success(f"Loaded **{len(recipients)}** recipients.")
    except Exception as e:
        st.error(f"Error reading file: {e}")
        recipients = []
else:
    recipients = []

st.divider()

# --- Section 4: Send Emails ---
st.header("4. Send Emails")

send_disabled = not recipients or not subject or not st.session_state.sender_email

if st.button("SEND EMAILS NOW", type="primary", disabled=send_disabled):
    if not st.session_state.sender_email:
        st.error("Please set your credentials in Section 1.")
    elif not recipients:
        st.error("Recipient list is empty.")
    elif not subject:
        st.error("Subject cannot be empty.")
    else:
        st.session_state.auth_error = False
        st.session_state.generic_error = ""
        
        with st.spinner(f"Attempting to send {len(recipients)} emails..."):
            
            if send_email(st.session_state.sender_email, st.session_state.sender_password, recipients, subject, email_body, is_html=use_html):
                st.success(f"Success! All {len(recipients)} emails sent from {st.session_state.sender_email}.")
                st.balloons()
            else:
                if st.session_state.auth_error:
                    st.error("Authentication Failed! Please double-check your Gmail address and 16-character App Password.")
                    st.markdown("Ensure 2-Step Verification is enabled on your Gmail account.")
                elif st.session_state.generic_error:
                    st.error(f"Sending Error: {st.session_state.generic_error}. Check recipient list and network.")
                else:
                    st.error("An unknown error occurred during the send process.")
