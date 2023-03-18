Email Analysis and Generator
This project provides tools for generating random emails and analyzing mbox files with a GUI interface. It consists of three Python scripts:

emailgenerator.py: A script for generating random emails and saving them to an mbox file.
dataprocessing.py: A script for processing and analyzing mbox files, including extracting sender and recipient information, counting the number of emails sent and received, and finding the most common words in the email subject and body.
guiemail.py: A graphical user interface (GUI) for loading mbox files, running the analysis from dataprocessing.py, and displaying the results.
Requirements
Python 3.6+

Install the required Python packages with:

Copy code
pip install -r requirements.txt
Usage
Generating Random Emails
To generate random emails and save them to an mbox file, use the emailgenerator.py script with the appropriate command-line arguments:

bash
Copy code
python emailgenerator.py 100 10 "example.mbox" --email_categories "Work,Personal" --email_templates "template1.html,template2.html"
This command generates 100 random emails with 10 people to consider and saves them to the example.mbox file. The emails will have categories of "Work" and "Personal" and will use the specified HTML email templates.

Analyzing Emails with the GUI
To analyze mbox files using the GUI, run the guiemail.py script:

bash
Copy code
python guiemail.py
This will launch the GUI, where you can load an mbox file, run the analysis, and view the results.

License
This project is licensed under the MIT License - see the LICENSE file for details.

