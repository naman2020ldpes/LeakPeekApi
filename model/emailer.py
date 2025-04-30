import smtplib
from email.message import EmailMessage

def sendemail(code,email):
    # Create an email message object
    msg = EmailMessage()
    msg['Subject'] = "Test Email"
    msg['From'] = "your_email@gmail.com"  # Replace with your Gmail address
    msg['To'] = email
    msg.set_content("This is your email varification code : ",code)
    
    # Establish a connection to the Gmail SMTP server and send the email
    with smtplib.SMTP('smtp.gmail.com', 587) as s:
        s.ehlo()  # Identify the client to the server
        s.starttls()  # Upgrade the connection to secure
        s.ehlo()  # Re-identify after starting TLS
        s.login(" PES1UG23CA060@pesu.pes.edu ", " uwdj cgkv mviv kidh")  # Replace with your Gmail and app password
        s.send_message(msg)