import os
import re
import email
import mailbox
import pandas as pd
from collections import defaultdict
from datetime import datetime
import plotly.express as px
from textblob import TextBlob
import argparse
from pathlib import Path
from typing import Tuple, List
from typing import Callable, Optional


def read_mbox(mbox_file: str) -> mailbox.mbox:
    try:
        mbox = mailbox.mbox(mbox_file)
    except FileNotFoundError:
        print(f"The mbox file '{mbox_file}' was not found.")
        exit(1)
    return mbox


def extract_domain(email_address: str) -> str:
    try:
        return re.search("@[\w.]+", email_address).group()
    except AttributeError:
        return ""


def process_mbox(mbox: mailbox.mbox, filters: dict) -> Tuple[defaultdict, defaultdict, defaultdict, defaultdict, list]:
    senders = defaultdict(int)
    recipients = defaultdict(int)
    dates = defaultdict(int)
    domains = defaultdict(int)
    subjects = []

    for msg in mbox:
        try:
            date = email.utils.parsedate_to_datetime(msg['Date'])
        except (TypeError, ValueError):
            continue

        # Apply date range filter
        if filters['start_date'] and date < filters['start_date']:
            continue
        if filters['end_date'] and date > filters['end_date']:
            continue

        date_key = date.strftime('%Y-%m')
        dates[date_key] += 1

        sender = msg['From']
        if sender:
            # Apply sender filter
            if not filters['sender'] or sender in filters['sender']:
                senders[sender] += 1
                domain = extract_domain(sender)
                if domain:
                    domains[domain] += 1

        recipient_list = email.utils.getaddresses(msg.get_all('To', []) + msg.get_all('Cc', []) + msg.get_all('Bcc', []))
        for recipient in recipient_list:
            # Apply recipient filter
            if not filters['recipient'] or recipient[1] in filters['recipient']:
                recipients[recipient[1]] += 1
                domain = extract_domain(recipient[1])
                if domain:
                    domains[domain] += 1

        subject = msg['Subject']
        if subject:
            # Apply subject filter
            if not filters['subject'] or any(keyword in subject for keyword in filters['subject']):
                subjects.append(subject)

    return senders, recipients, dates, domains, subjects


def plot_emails_per_month(dates: defaultdict, output_file: str) -> None:
    sorted_dates = sorted(dates.items(), key=lambda x: x[0])

    # Add this check to handle empty sorted_dates:
    if not sorted_dates:
        print("No emails found for the given filters.")
        return

    date_labels, date_counts = zip(*sorted_dates)

    fig = px.bar(x=date_labels, y=date_counts, labels={'x': 'Months', 'y': 'Number of Emails'}, title='Emails per Month')
    fig.write_html(output_file)
    fig.show()


def plot_emails_by_domain(domains: defaultdict, output_file: str) -> None:
    sorted_domains = sorted(domains.items(), key=lambda x: x[1], reverse=True)

    # Add this check to handle empty sorted_domains:
    if not sorted_domains:
        print("No emails found for the given filters.")
        return

    domain_labels, domain_counts = zip(*sorted_domains)

    fig = px.bar(x=domain_labels, y=domain_counts, labels={'x': 'Email Domains', 'y':'Number of Emails'}, title='Emails by Domain')
    fig.write_html(output_file)
    fig.show()


def plot_top_senders_recipients(senders: defaultdict, recipients: defaultdict, output_file: str, n: int = 10) -> None:
    sorted_senders = sorted(senders.items(), key=lambda x: x[1], reverse=True)[:n]

    # Add this check to handle empty sorted_senders:
    if not sorted_senders:
        print("No senders found for the given filters.")
    else:
        sender_labels, sender_counts = zip(*sorted_senders)
        fig = px.bar(x=sender_labels, y=sender_counts, labels={'x': 'Top Senders', 'y': 'Number of Emails'}, title=f'Top {n} Senders')
        fig.write_html(output_file + "_top_senders.html")
        fig.show()

    sorted_recipients = sorted(recipients.items(), key=lambda x: x[1], reverse=True)[:n]

    # Add this check to handle empty sorted_recipients:
    if not sorted_recipients:
        print("No recipients found for the given filters.")
    else:
        recipient_labels, recipient_counts = zip(*sorted_recipients)
        fig = px.bar(x=recipient_labels, y=recipient_counts, labels={'x': 'Top Recipients', 'y': 'Number of Emails'}, title=f'Top {n} Recipients')
        fig.write_html(output_file + "_top_recipients.html")
        fig.show()


def plot_subject_sentiment(subjects: list, output_file: str) -> None:
    sentiment_values = [TextBlob(subject).sentiment.polarity for subject in subjects]
    sentiment_labels = ['Negative', 'Neutral', 'Positive']
    sentiment_counts = [sum(1 for sentiment in sentiment_values if sentiment < 0),
                        sum(1 for sentiment in sentiment_values if sentiment == 0),
                        sum(1 for sentiment in sentiment_values if sentiment > 0)]
    fig = px.bar(x=sentiment_labels, y=sentiment_counts, labels={'x': 'Sentiment', 'y': 'Number of Subjects'}, title='Subject Sentiment')
    fig.write_html(output_file)
    fig.show()

def export_to_csv(senders, recipients, dates, domains, subjects, output_file_prefix='email_data'):
    senders_df = pd.DataFrame(list(senders.items()), columns=['sender', 'count'])
    recipients_df = pd.DataFrame(list(recipients.items()), columns=['recipient', 'count'])
    dates_df = pd.DataFrame(list(dates.items()), columns=['date', 'count'])
    domains_df = pd.DataFrame(list(domains.items()), columns=['domain', 'count'])
    subjects_df = pd.DataFrame(subjects, columns=['subject'])

    senders_df.to_csv(output_file_prefix + "_senders.csv", index=False)
    recipients_df.to_csv(output_file_prefix + "_recipients.csv", index=False)
    dates_df.to_csv(output_file_prefix + "_dates.csv", index=False)
    domains_df.to_csv(output_file_prefix + "_domains.csv", index=False)
    subjects_df.to_csv(output_file_prefix + "_subjects.csv", index=False)


def parse_arguments():
    parser = argparse.ArgumentParser(description='Analyze and visualize mbox files.')
    parser.add_argument('mbox_file', type=str, help='Path to mbox file')
    parser.add_argument('--start_date', type=lambda x: datetime.strptime(x, '%Y-%m-%d'), default=None, help='Start date for filtering emails (YYYY-MM-DD format)')
    parser.add_argument('--end_date', type=lambda x: datetime.strptime(x, '%Y-%m-%d'), default=None, help='End date for filtering emails (YYYY-MM-DD format)')
    parser.add_argument('--output_prefix', type=str, default='email_analysis', help='Output file prefix for charts and CSV files')
    parser.add_argument('--n', type=int, default=10, help='Number of top senders and recipients to display')
    return parser.parse_args()

def analyze_email(mbox_files: List[str], start_date: Optional[datetime], end_date: Optional[datetime], keyword: str, cancel_callback: Callable):
    # Create a filters dictionary
    filters = {
        'start_date': start_date,
        'end_date': end_date,
        'sender': None,
        'recipient': None,
        'subject': [keyword] if keyword else None
    }

    # Process mbox files
    all_senders, all_recipients, all_dates, all_domains, all_subjects = defaultdict(int), defaultdict(int), defaultdict(int), defaultdict(int), []

    for mbox_file in mbox_files:
        mbox = read_mbox(mbox_file)
        senders, recipients, dates, domains, subjects = process_mbox(mbox, filters)

        for key, value in senders.items():
            all_senders[key] += value
        for key, value in recipients.items():
            all_recipients[key] += value
        for key, value in dates.items():
            all_dates[key] += value
        for key, value in domains.items():
            all_domains[key] += value
        all_subjects.extend(subjects)

        if cancel_callback():
            break

    # Visualize and export the results
    output_prefix = "email_analysis"

    plot_emails_per_month(all_dates, output_prefix + '_emails_per_month.html')
    plot_emails_by_domain(all_domains, output_prefix + '_domains.html')
    plot_top_senders_recipients(all_senders, all_recipients, output_prefix)
    plot_subject_sentiment(all_subjects, output_prefix + '_subject_sentiment.html')

    export_to_csv(all_senders, all_recipients, all_dates, all_domains, all_subjects, output_prefix)


def main():
    args = parse_arguments()

    mbox_file = args.mbox_file
    start_date = args.start_date
    end_date = args.end_date
    output_prefix = args.output_prefix
    n = args.n

    senders, recipients, dates, domains, subjects = process_mbox_file(mbox_file, start_date, end_date)

    plot_senders_over_time(dates, output_prefix + '_senders_over_time.html')
    plot_emails_by_domain(domains, output_prefix + '_domains.html')
    plot_top_senders_recipients(senders, recipients, output_prefix, n)
    plot_subject_sentiment(subjects, output_prefix + '_subject_sentiment.html')

    export_to_csv(senders, recipients, dates, domains, subjects, output_prefix)


if __name__ == "__main__":
    main()


