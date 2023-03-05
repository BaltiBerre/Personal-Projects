import argparse
import re
import mailbox
from datetime import datetime
import matplotlib
matplotlib.use('TkAgg') #set the backend to TkAgg
import matplotlib.pyplot as plt
from collections import Counter
import networkx as nx



def analyze_email_chain(filename):
    """
    Analyzes an mbox file containing email messages and returns a dictionary of information
    about the email chain, including the number of emails, number of senders, number of 
    recipients, date range of emails, and frequency of emails sent by each sender.
    """
    try:
        mbox = mailbox.mbox(filename) # open mbox file
        if not mbox:
            print("Error: mbox file is empty") # print error if mbox file is empty
            return None
    except (mailbox.NoSuchMailboxError, TypeError) as e: # catch exceptions for mailbox errors
        print(f"Error opening mbox file: {e}") 
        return None

    senders = [] #list of senders 
    recipients = [] # list of all recipients
    dates = [] # list of all dates emails were sent
    for message in mbox: # iterate through each message in mbox file
        sender = re.findall(r'<(.+?)>', message['From']) 
        if sender:
            senders.append(sender[0])
        recipients.extend(re.findall(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', (message['To'] or '') + (message['Cc'] or '') + (message['Bcc'] or '')))
        try:
            date = datetime.strptime(message['Date'][:-6], '%a, %d %b %Y %H:%M:%S %z')
        except (ValueError, TypeError):
            date = None
        if date:
            dates.append(date)
    mbox.close() # close mbox files 
    if not senders: 
        print("No valid emails found in mbox file") # print error message if no valid emails found
        return None
    num_emails = len(senders) # number of mails
    unique_senders = set(senders) # set of unique senders 
    num_senders = len(unique_senders) # number of unique senders
    num_recipients = len(set(recipients)) # number of unique recipients
    if not dates:
        date_range = "No dates found" # error message if no dates found
    else:
        date_range = f"{min(dates).strftime('%Y-%m-%d')} to {max(dates).strftime('%Y-%m-%d')}"
    sender_freq = Counter(senders) # frequency of emails sent by each sender

    # Creating a network graph
  
    try:
      graph = nx.Graph()
      for sender in unique_senders:
        graph.add_node(sender)
      for recipient in set(recipients):
        graph.add_node(recipient)
      for recipient in recipients:
        graph.add_edge(sender, recipient)
      pos = nx.spring_layout(graph)
      nx.draw(graph, pos, node_color = "blue", node_size = 50, with_labels = True)
      plt.show()
    except (ValueError, TypeError) as e:
        print(f"Error creating Network Graph: {e}")
        return None 
    
    # Creating Bar Graph

    try:
      fig, ax = plt.subplots(figsize=(10, 5))
      ax.bar(sender_freq.keys(), sender_freq.values(), color='blue', width=0.4)

      # Set the tick locations
      tick_locs = range(len(sender_freq))
      ax.set_xticks(tick_locs)
      
      # Set the tick labels
      tick_labels = sender_freq.keys()
      ax.set_xticklabels(tick_labels, rotation=45, ha='right')
      
      ax.set_xlabel('Sender')
      ax.set_ylabel('Number of emails')
      ax.set_title('Number of Emails Sent by Each Sender')
      plt.tight_layout()
      plt.show()
    except (ValueError, TypeError) as e:
        print(f"Error creating bar graph: {e}")
        return None


    return {'Number of Emails': num_emails,
            'Number of Senders': num_senders,
            'Number of recipients': num_recipients,
            'Date Range': date_range,
            'Sender Frequency': sender_freq}


if __name__ == '__main__':
    filename = input("Enter the name of the mbox file to analyze: ")
    result = analyze_email_chain(filename)
    if result:
        print(result)
