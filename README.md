# Week 12: Automating Communications (Email & SMS)

This project demonstrates how to automate sending and receiving emails, and sending SMS messages, using Python. It uses `smtplib` for sending, `imaplib` for receiving, and email-to-SMS gateways for text messages. Credentials are loaded securely from a `.env` file with `python-dotenv`.

**Student:** see `STUDENT_NAME` / `STUDENT_ID` — every email sent by this script shows the student's name and ID in the subject and body.

## Screenshot: email notification from running the code

![Email notification](screenshots/email_notification.png)

## Key Concepts Demonstrated

* **Email Sending (SMTP)**: secure TLS connection to Gmail, login with an App Password, multipart emails (`email.mime`) with plain text and a PDF attachment, UTF-8 headers so Thai text displays correctly.
* **Email Receiving (IMAP)**: search for `UNSEEN` emails by sender and subject, fetch and parse the message, download attachments to `data/attachments/`, mark as read.
* **SMS via Email Gateway**: carrier email-to-SMS addresses (US carriers). Thai carriers (AIS / TrueMove H / dtac) don't offer a public gateway, so Task 3 logs a warning and the script continues.
* **Secure Credential Handling**: `.env` + `python-dotenv`; `.env` is listed in `.gitignore` and never committed (`.env.example` is the template).
* **Modular Design**: `email_sender.py`, `email_receiver.py`, `sms_gateway.py`, `utils.py`.
* **Logging**: informative console output for every task.

## Setup & How to Run

1. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```
2. **Create a Gmail App Password**: Google Account → Security → 2-Step Verification (turn on) → App passwords → create one (16 characters).
3. **Configure `.env`**: copy `.env.example` to `.env` and fill in:
   ```ini
   SENDER_EMAIL=your_email@gmail.com
   SENDER_APP_PASSWORD=your_16_char_app_password
   SMTP_SERVER=smtp.gmail.com
   SMTP_PORT=587
   IMAP_SERVER=imap.gmail.com
   TEST_RECIPIENT_EMAIL=your_email@gmail.com
   TEST_SMS_PHONE_NUMBER=0812345678
   TEST_SMS_CARRIER=ais
   STUDENT_NAME=ชื่อ นามสกุล
   STUDENT_ID=663380372-6
   ```
4. **Sample attachment**: `data/dummy_report.pdf` is included (re-create with `python create_dummy_report.py`).
5. **Run**
   ```bash
   python main.py
   ```
   The script will:
   * **Task 1**: send a plain-text email to `TEST_RECIPIENT_EMAIL`
   * **Task 2**: send an email with `dummy_report.pdf` attached
   * **Task 3**: try to send an SMS via the carrier's email gateway (skipped if the carrier is unsupported)
   * **Task 4**: send a demo email to yourself, find it via IMAP, print sender, subject and body, download the attachment, and mark it as read

## Project Structure

```
email-sms-automator/
├── src/
│   ├── __init__.py
│   ├── email_sender.py      # Sending emails (SMTP)
│   ├── email_receiver.py    # Receiving emails (IMAP)
│   ├── sms_gateway.py       # Email-to-SMS
│   └── utils.py             # Logging, .env loading, directory helpers
├── data/
│   ├── attachments/         # Downloaded attachments
│   └── dummy_report.pdf     # Sample attachment
├── screenshots/
│   └── email_notification.png
├── .env.example             # Template for .env (the real .env is NOT committed)
├── create_dummy_report.py
├── main.py
├── requirements.txt
├── .gitignore
└── README.md
```

## Fixes made to the lab's starter code

* `main.py` imported modules via `sys.path` + `from email_sender import ...`, which breaks the relative imports in `src/`. Changed to `from src.email_sender import ...`.
* Subject and body are encoded as UTF-8 (`Header`, `MIMEText(..., 'utf-8')`) so Thai names don't break sending.
* IMAP search and fetch use real UIDs (`mail.uid(...)`), so the IDs stay valid after reconnecting.
* The App Password is used with its spaces removed (Google shows it as `abcd efgh ijkl mnop`).

## Debugging

* **`Environment variable '...' not set`**: `.env` is missing or a value is empty.
* **`SMTPAuthenticationError`**: use a Gmail **App Password**, not your normal password; 2-Step Verification must be on.
* **Emails not arriving**: check the Spam folder.
* **SMS not arriving**: expected for Thai carriers (no email-to-SMS gateway).
