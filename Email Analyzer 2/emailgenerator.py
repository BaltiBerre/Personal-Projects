import random
import sys
import argparse
from pathlib import Path
from faker import Faker
from mailbox import mbox
from email.message import EmailMessage
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication

def generate_email(fake, senders_list, recipients_list, email_categories, email_templates):
    email = MIMEMultipart()
    
    paragraphs = '\n\n'.join(fake.paragraphs())
    content = MIMEText(paragraphs, "plain")
    email.attach(content)

    email["Subject"] = "Important " + fake.sentence()
    email["From"] = random.choice(senders_list)
    email["To"] = ", ".join(random.sample(recipients_list, random.randint(1, len(recipients_list))))
    email["Date"] = fake.date_time_this_year().strftime('%a, %d %b %Y %H:%M:%S %z')
    
    if random.choice([True, False]):
        email["Cc"] = ", ".join(random.sample(recipients_list, random.randint(1, len(recipients_list))))
    
    if random.choice([True, False]):
        email["Bcc"] = ", ".join(random.sample(recipients_list, random.randint(1, len(recipients_list))))
    
    if random.choice([True, False]):
        attachment = MIMEApplication(fake.binary(1024))
        attachment.add_header('Content-Disposition', 'attachment', filename=fake.file_name())
        email.attach(attachment)
    
    if email_categories:
        email["Category"] = random.choice(email_categories)

    if email_templates:
        template = random.choice(email_templates)
        with open(template, 'r') as file:
            email_template = file.read()
        content = MIMEText(email_template, "html")
        email.attach(content)
    
    return email

def main(args):
    fake = Faker()

    senders_list = [fake.email() for _ in range(args.num_people)]
    recipients_list = [fake.email() for _ in range(args.num_people)]

    mailbox = mbox(args.mbox_file)
    
    email_categories = args.email_categories.split(',') if args.email_categories else None
    email_templates = args.email_templates.split(',') if args.email_templates else None
    
    for i in range(args.num_emails):
        email = generate_email(fake, senders_list, recipients_list, email_categories, email_templates)
        mailbox.add(email)
        print(f"Generated email {i + 1}/{args.num_emails}", end='\r')

    mailbox.flush()
    mailbox.lock()
    mailbox.unlock()
    mailbox.close()
    print(f"\n{args.num_emails} emails generated and saved to {args.mbox_file}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate random emails and save them to an mbox file.")
    parser.add_argument("num_emails", type=int, help="Number of emails to generate.")
    parser.add_argument("num_people", type=int, help="Number of people to consider.")
    parser.add_argument("mbox_file", type=str, help="Filename for the mbox file.")
    parser.add_argument("--email_categories", type=str, help="Comma-separated list of email categories.")
    parser.add_argument("--email_templates", type=str, help="Comma-separated list of email template file paths.")
    
    args = parser.parse_args()
    main(args)
