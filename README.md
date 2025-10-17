
# 📧 Multi-Mailer: Bulk Email Sender Utility

A powerful and flexible bulk email sender built with **Python** and **Streamlit**, supporting both **local multi-account management** and **secure cloud deployment**.

---

## ✨ Features

- **🖥️ Dual Interface**  
  Includes two app versions:  
  - `app_local.py` → Local multi-account Streamlit app  
  - `app_streamlit.py` → Cloud-ready Streamlit app  

- **📬 Multi-Account Management**  
  The local version lets you add, select, and manage multiple Gmail accounts stored in a secure local file (`credentials.txt`).

- **🔒 Security-First Design**  
  Uses **Gmail App Passwords** with isolated credential handling for local and cloud use.

- **🧾 Custom Email Content**  
  Send either **plain text** or **HTML-based** emails with full template support.

- **📊 Recipient Management**  
  Automatically reads recipient addresses from the first column of an Excel `.xlsx` file.

---

## 💻 Option 1: Local Host Use (`app_local.py`)

This version is designed for **local, manual use** with multiple Gmail accounts.

### ✅ Prerequisites

1. A Gmail account with **2-Step Verification (2SV)** enabled  
2. A **Gmail App Password** generated for your sending account(s)

### ⚙️ Setup and Run

Clone the repository:
```bash
git clone https://github.com/YOUR_USERNAME/Multi-Mailer.git
cd Multi-Mailer
````

Install dependencies:

```bash
pip install -r requirements.txt
```

Run the Streamlit app:

```bash
streamlit run app_local.py
```

Use the UI to manage accounts — credentials will be stored securely in `credentials.txt`.

---

## 🌐 Option 2: Cloud Deployment (`app_streamlit.py`)

This version is optimized for **Streamlit Cloud** (or similar hosting platforms).

### 🚀 Deployment Steps

1. **Commit Files**
   Ensure `app_streamlit.py` and `requirements.txt` are included in your repository.

2. **Deploy on Streamlit Cloud**

   * Go to [Streamlit Cloud](https://share.streamlit.io/)
   * Select your GitHub repository for deployment

3. **Configure Secrets**
   Open the **Secrets** panel and paste the following:

   ```ini
   [email_credentials]
   sender_email = "YOUR_GMAIL_ADDRESS@gmail.com"
   app_password = "YOUR_16_CHARACTER_APP_PASSWORD"
   ```

4. **Set Main File**
   Make sure the main file is set to:

   ```
   app_streamlit.py
   ```

5. **Deploy!**
   Your Streamlit Cloud app is now live and secure.

---

## ⚙️ Dependencies

All required packages are listed in `requirements.txt`.

Install them using:

```bash
pip install -r requirements.txt
```

---

## 📁 Project Structure

```
Multi-Mailer/
│
├── app_local.py
├── app_streamlit.py
├── requirements.txt
├── credentials.txt        # (ignored - local only)
├── .gitignore
└── README.md
```

---

## 🧠 Tech Stack

* **Python 3.10+**
* **Streamlit**
* **smtplib / email.mime**
* **pandas / openpyxl** (for Excel file handling)

---

## 🧪 Usage Example

Here’s how to use Multi-Mailer effectively once you’ve set it up:

### 1️⃣ Prepare Recipient File

Create an Excel file named `recipients.xlsx` with your recipient list:

```
| Email Address          |
|------------------------|
| example1@gmail.com     |
| example2@yahoo.com     |
| example3@outlook.com   |
```

### 2️⃣ Launch App

```bash
streamlit run app_local.py
```

### 3️⃣ Add Account

In the app:

* Enter your Gmail address
* Paste the **App Password**
* Save — the credentials will be stored securely in `credentials.txt`

### 4️⃣ Compose & Send

* Enter **Subject** and **Body** (plain text or HTML)
* Upload your `recipients.xlsx`
* Click **Send Emails**

✅ The app will send messages in bulk through your selected Gmail account(s).

---


## 💡 Author

**Developed by:** Noman Khan

🌐 GitHub: [https://github.com/BuildWithNomi](https://github.com/BuildWithNomi)

---

## 🛡️ License

This project is licensed under the **MIT License** – see the [LICENSE](LICENSE) file for details.

---

## ⭐ Support

If you find this project useful, please give it a **⭐ Star** on GitHub to show your support!

---

```
