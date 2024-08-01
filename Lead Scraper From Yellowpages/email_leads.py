import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import csv

def send_email(to_email, business_name):
    # SMTP Configuration
    smtp_host = 'smtp.gmail.com'
    smtp_port = 587
    smtp_username = 'contact@riverbenddigitalsolutions.com'  # Your Gmail or Google Workspace email address
    smtp_password = 'Ryder1410!'  # Your Gmail or Google Workspace account password

    # Email Content
    sender_email = smtp_username
    receiver_email = to_email
    subject = f'Custom Web Design Services for {business_name}'
    body = f"Dear {business_name},\n\nWe noticed that your business does not have a website. At Riverbend Digital Solutions, we offer custom web design services tailored to your needs. Having a professional website can greatly enhance your online presence and attract more customers.\n\nIf you're interested in learning more about our services, please feel free to contact us at contact@riverbenddigitalsolutions.com.\n\nBest regards,\nRiverbend Digital Solutions"

    # Create a multipart message and set headers
    message = MIMEMultipart()
    message['From'] = sender_email
    message['To'] = receiver_email
    message['Subject'] = subject

    # Add body to email
    message.attach(MIMEText(body, 'plain'))

    # Create SMTP session
    server = smtplib.SMTP(smtp_host, smtp_port)
    server.starttls()  # Enable TLS encryption
    server.login(smtp_username, smtp_password)  # Login to Gmail/Google Workspace

    # Send email
    server.sendmail(sender_email, receiver_email, message.as_string())
    print(f"Email sent to {receiver_email} for {business_name}")

    # Quit server
    server.quit()

def main():
    with open('C:\\Users\\basse\\python_projects\\Lead Scraper From Yellowpages\\leads2.csv', mode='r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            email = row['email']
            business_name = row['name']
            if email and email != 'yp-logo@2x.png':  # Check if email exists and is not placeholder
                send_email(email, business_name)

if __name__ == "__main__":
    main()
