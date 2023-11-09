import imaplib
import email
from email.header import decode_header
from datetime import datetime, timedelta
import re
from bs4 import BeautifulSoup

# Email server settings
email_user = "****"  # Your email address
email_pass = "****"  # Your email password, generate token from gmail
email_server = "imap.gmail.com"  # IMAP server address
label_name = "Low balance" # The folder where you want to search for emails

start_date = (datetime.now() - timedelta(days=2)).strftime("%d-%b-%Y")  # Example: 7 days ago
end_date = (datetime.now() + timedelta(days=1)).strftime("%d-%b-%Y")  # Today
    
# Create an IMAP4 class with SSL
mail = imaplib.IMAP4_SSL(email_server)

# Log in to your account

def get_company_names():
    mail.login(email_user, email_pass)

    print("logged in!")

    result, mailbox_list = mail.list()

    selected_mailbox = None
    for mailbox_info in mailbox_list:
        mailbox = mailbox_info.decode("utf-8")
        if label_name.casefold() in mailbox.casefold():
            selected_mailbox = mailbox
            break
    # Select the mailbox you want to search
    mailbox_name = selected_mailbox.split(' "/" ')[1]
    mail.select(mailbox_name)

    # Search for emails from the specific sender (abc@xyz.com)
    sender_email = "****"
    search_criteria = f'(FROM "{sender_email}") SINCE {start_date} BEFORE {end_date}'

    # Search for emails matching the criteria
    status, email_ids = mail.search(None, search_criteria)

    # Split the list of email IDs
    email_id_list = email_ids[0].split()

    # Initialize a list to store company names
    company_data = []

    # Regular expression pattern to match the subject
    subject_pattern = re.compile(r'(.*?) wallet balance is running low!', re.IGNORECASE)
    balance_pattern = re.compile(r'Wallet Balance: (\d+\.\d+)', re.IGNORECASE)

    # Loop through the email IDs and fetch email subjects
    for email_id in email_id_list:
        status, msg_data = mail.fetch(email_id, "(BODY[HEADER.FIELDS (SUBJECT)])")
        status, body_data = mail.fetch(email_id, "(BODY[TEXT])")
        if status == "OK":
            msg = email.message_from_bytes(msg_data[0][1])
            subject, encoding = decode_header(msg["Subject"])[0]
            subject_text = decode_header(msg["Subject"])[1][0]

            if subject_text:
                subject_text = subject_text.decode(encoding)
            
            match_subject = subject_pattern.match(subject_text)

            # Extract the wallet balance from the email body
            email_content = email.message_from_bytes(body_data[0][1]).get_payload()
            soup = BeautifulSoup(email_content, 'html.parser')
            # Search for the wallet balance in the parsed HTML
            target_text = "Wallet Balance"
            p_elements = soup.find_all('p')

            # Iterate through the p elements to find the relevant one
            for p_element in p_elements:
                if target_text in p_element.get_text():
                    wallet_balance_text = p_element.find(string=re.compile(f'{target_text}:'))
                    # Extract the balance value
                    wallet_balance = wallet_balance_text.split(':')[-1].strip()

            company_name = match_subject.group(1)
            company_data.append({"company_name": company_name, "wallet_balance": wallet_balance})

    # Print the list of company names and wallet balances
    for data in company_data:
        print(f"Company Name: {data['company_name']}, Wallet Balance: {data['wallet_balance']}")

    # Logout and close the connection
    mail.logout()

