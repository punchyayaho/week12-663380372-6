# email-sms-automator/main.py
import os
import sys
import time

# Make sure the project root is on the path so the 'src' package can be imported
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from src.email_sender import EmailSender
from src.email_receiver import EmailReceiver
from src.sms_gateway import SMSGateway
from src.utils import setup_logging, get_env_variable, ensure_directory_exists

logger = setup_logging(__name__)


def main():
    """
    Main function to orchestrate email and SMS automation tasks.
    """
    base_dir = os.path.dirname(os.path.abspath(__file__))
    data_dir = os.path.join(base_dir, 'data')
    attachments_dir = os.path.join(data_dir, 'attachments')
    ensure_directory_exists(data_dir)
    ensure_directory_exists(attachments_dir)

    # --- Load Credentials from Environment Variables ---
    try:
        sender_email = get_env_variable("SENDER_EMAIL")
        sender_app_password = get_env_variable("SENDER_APP_PASSWORD").replace(" ", "")
        smtp_server = get_env_variable("SMTP_SERVER", "smtp.gmail.com")
        smtp_port = int(get_env_variable("SMTP_PORT", "587"))
        imap_server = get_env_variable("IMAP_SERVER", "imap.gmail.com")
        test_recipient_email = get_env_variable("TEST_RECIPIENT_EMAIL")
        test_sms_phone_number = get_env_variable("TEST_SMS_PHONE_NUMBER")
        test_sms_carrier = get_env_variable("TEST_SMS_CARRIER")
        # Student info shown in every email (subject + body)
        student_name = get_env_variable("STUDENT_NAME")
        student_id = get_env_variable("STUDENT_ID")
    except ValueError as e:
        logger.critical(f"Configuration error: {e}. Please set all required environment variables in your .env file.")
        sys.exit(1)

    tag = f"[{student_id} {student_name}]"
    student_block = (
        f"ชื่อ-นามสกุล (Name): {student_name}\n"
        f"รหัสนักศึกษา (Student ID): {student_id}\n"
    )

    # --- Initialize Handlers ---
    email_sender = EmailSender(smtp_server, smtp_port, sender_email, sender_app_password)
    email_receiver = EmailReceiver(imap_server, sender_email, sender_app_password)
    sms_gateway = SMSGateway(email_sender)

    # --- Task 1: Send a simple plaintext email ---
    logger.info("--- Task 1: Sending a simple plaintext email ---")
    email_sender.send_email(
        recipient_email=test_recipient_email,
        subject=f"{tag} Automated Python Test Email",
        body=(
            f"{student_block}\n"
            "Hello from your Python automation script! This is a plain text email.\n"
            "(Week 12 LabX BASIC: Automating Communications - Email & SMS)"
        ),
    )
    time.sleep(2)  # Give a short delay

    # --- Task 2: Send an email with an attachment ---
    logger.info("--- Task 2: Sending an email with an attachment ---")
    attachment_file_path = os.path.join(data_dir, 'dummy_report.pdf')
    if os.path.exists(attachment_file_path):
        email_sender.send_email(
            recipient_email=test_recipient_email,
            subject=f"{tag} Python Test Email with Attachment - Daily Report",
            body=f"{student_block}\nPlease find the daily report attached.",
            attachment_path=attachment_file_path,
        )
    else:
        logger.warning(f"Attachment file not found at '{attachment_file_path}'. Skipping attachment email.")
    time.sleep(2)

    # --- Task 3: Send an SMS via email gateway ---
    logger.info("--- Task 3: Sending an SMS via email gateway ---")
    sms_message = f"{student_name} {student_id}: Hello from Python! Automated SMS via email gateway."
    sms_ok = sms_gateway.send_sms(
        phone_number=test_sms_phone_number,
        message=sms_message,
        carrier_name=test_sms_carrier,
    )
    if not sms_ok:
        logger.warning("SMS could not be sent (carrier gateway not supported). Continuing with the next task.")
    time.sleep(5)

    # --- Task 4: Receive and process emails ---
    logger.info("--- Task 4: Receiving and processing emails ---")
    demo_subject = "Python Test: Email for Receiving Demo"
    email_sender.send_email(
        recipient_email=sender_email,  # Send to self
        subject=f"{tag} {demo_subject}",
        body=f"{student_block}\nThis email is specifically for the receiving demo. It has an attachment!",
        attachment_path=attachment_file_path if os.path.exists(attachment_file_path) else None,
    )
    logger.info("Sent a demo email to self for receiving task. Waiting a few seconds...")
    time.sleep(10)  # Give email server time to process and deliver

    uids = email_receiver.search_emails(
        criteria='UNSEEN',
        from_sender=sender_email,
        subject_contains=demo_subject,
    )

    if uids:
        logger.info(f"Found {len(uids)} matching unread email(s) for receiving demo.")
        for uid in uids:
            logger.info(f"Processing email UID: {uid.decode('utf-8')}")
            email_details = email_receiver.fetch_email_content(
                uid=uid,
                mark_as_read=True,
                download_attachments_dir=attachments_dir,
            )
            if email_details:
                logger.info(f"  Sender: {email_details['sender']}")
                logger.info(f"  Subject: {email_details['subject']}")
                logger.info(f"  Body Snippet: {email_details['body_snippet']}")
                if email_details['attachments_downloaded']:
                    logger.info(f"  Attachments downloaded: {', '.join(email_details['attachments_downloaded'])}")
                else:
                    logger.info("  No attachments downloaded for this email.")
            else:
                logger.error(f"Could not retrieve details for email UID: {uid.decode('utf-8')}")
    else:
        logger.info("No matching unread emails found for receiving demo.")

    logger.info("--- All communication automation tasks completed ---")


if __name__ == "__main__":
    main()
