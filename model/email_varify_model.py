import random
import time
from flask import Response , jsonify
import smtplib
from email.message import EmailMessage

import smtplib
from email.message import EmailMessage

def sendemail(code,email):
    # Create an email message object
    msg = EmailMessage()
    msg['Subject'] = "Test Email"
    msg['From'] = "your_email@gmail.com"  # Replace with your Gmail address
    msg['To'] = email
    msg.set_content("This is your email varification code : "+code)
    
    # Establish a connection to the Gmail SMTP server and send the email
    with smtplib.SMTP('smtp.gmail.com', 587) as s:
        s.ehlo()  # Identify the client to the server
        s.starttls()  # Upgrade the connection to secure
        s.ehlo()  # Re-identify after starting TLS
        s.login(" PES1UG23CA060@pesu.pes.edu ", " uwdj cgkv mviv kidh")  # Replace with your Gmail and app password
        s.send_message(msg)

# In-memory store (acts as a simple dictionary for tracking emails and verification codes)
verification_store = {}

# Constants
CODE_EXPIRY_SECONDS = 300       # 5 minutes
ENTRY_EXPIRY_SECONDS = 1800     # 30 minutes

def generate_code():
    """Generates a 6-digit random code."""
    return str(random.randint(100000, 999999))

def clean_stale_entries():
    """Cleans up entries that have not been interacted with for more than 30 minutes."""
    now = time.time()
    to_remove = [
        email for email, entry in verification_store.items()
        if now - entry["last_interaction"] > ENTRY_EXPIRY_SECONDS
    ]
    for email in to_remove:
        del verification_store[email]

def emailVarify(email: str, action: str, code: str = None):
    """
    Core email verification logic.
    
    :param email: The user's email.
    :param action: One of "send", "resend", or "verify".
    :param code: The verification code to verify (only for "verify" action).
    :return: dict with success/error message.
    """
    # Clean up stale entries
    clean_stale_entries()

    now = time.time()

    # Create or resend verification code
    if action in ("send", "resend"):
        
        new_code = generate_code()
        sendemail(new_code,email)
        verification_store[email] = {
            "code": new_code,
            "code_created_at": now,
            "last_interaction": now
        }
        return jsonify({
            "status": "code_sent",
            "code": new_code,  #  not return this varify code just for dmeo 
            "message": f"Verification code {'resent' if action == 'resend' else 'sent'}."
        })

    # Verify the code
    elif action == "verify":
        entry = verification_store.get(email)
        if not entry:
            return jsonify({"status": "error", "message": "No code found for this email.","check":404})

        # Check if the code has expired (more than 5 minutes)
        if now - entry["code_created_at"] > CODE_EXPIRY_SECONDS:
            del verification_store[email]
            return jsonify({"status": "error", "message": "Verification code expired.","check":404})

        # Check if the submitted code matches
        if entry["code"] == code:
            del verification_store[email]  # Delete entry after successful verification
            return jsonify({"status": "success", "message": "Email verified successfully.","page":"home","check":200})
        else:
            return jsonify({"status": "error", "message": "wrond verification code.","check":404})

    # If the action is invalid
    else:
        return jsonify({"status": "error", "message": "Invalid action specified.","check":404})
