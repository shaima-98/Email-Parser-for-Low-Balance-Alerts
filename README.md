# Email Parser for Low Balance client list

1. Introduction

This Python script is designed to parse emails from a specified mailbox and extract information about companies with low wallet balances. It connects to an IMAP server using the provided credentials, searches for emails matching specific criteria, and extracts relevant data from the email subjects and bodies.

2. Dependencies

- `imaplib`: Library for accessing and manipulating mail using the Internet Message Access Protocol (IMAP).
- `email`: Provides tools for parsing and handling email messages.
- `email.header`: Allows decoding email headers.
- `datetime`: Provides functionality to work with dates and times.
- `re`: Module for regular expressions.
- `bs4` (Beautiful Soup): Library for pulling data out of HTML and XML files.

3. Configuration

  A. Generating App password for gmail account:

- Go to your Google Account.
- Select Security.
- Under "Signing in to Google," select 2-Step Verification.
- At the bottom of the page, select App passwords.
- Enter a name that helps you remember where you’ll use the app password.
- Select Generate.
- The generated app password will be displayed. Copy it to a secure location, as you won't be able to see it again.
- Use App Password in Your Script. Replace the 'email_pass' variable in your script with the generated app password.

  B. Email Server Settings:

- email_user: Your email address.
- email_pass: Generated app password
- email_server: IMAP server address (e.g., "imap.gmail.com").
- label_name: The folder where you want to search for emails (e.g., "Low balance").

  C. Date Range Settings:

- start_date: The start date for searching emails 
- end_date: The end date for searching emails

  D. Sender Email:

- sender_email: The specific sender's email address to filter emails.

4. Functionality

- **Log in to Email Account**: The script logs in to the specified email account using the provided credentials.
- **Select Mailbox**: It selects the mailbox where the search for low balance alerts will be performed.
- **Search Criteria**: Emails are searched based on the sender's email address and within the specified date range.
- **Data Extraction**: The script extracts company names and wallet balances from email subjects and bodies.
- **Output**: The parsed data (company names and wallet balances) is sent to an excel file.
- **Logout**: Finally, the script logs out and closes the connection to the email server.

5. Usage

- Replace placeholders (`email_user`, `email_pass`, `email_server`, `label_name`, and `sender_email`) with your actual email and server information.
- Ensure that the required dependencies (`imaplib`, `email`, `datetime`, `re`, `bs4`) are installed.
- Run the script.
