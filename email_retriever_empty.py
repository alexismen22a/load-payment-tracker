import imaplib
from datetime import datetime
from bs4 import BeautifulSoup
import re
import pandas as pd
import os

def get_raw_html_from_email(username, password, server, port, subject, from_date):
    # Connect to the IMAP server
    mail = imaplib.IMAP4_SSL(server, port)

    # Login to the email account
    mail.login(username, password)

    # Select the mailbox (e.g., 'INBOX')
    mail.select('INBOX')

    # Search for emails with the specified subject and from the given date
    search_criteria = f'(SUBJECT "{subject}") SINCE "{from_date.strftime("%d-%b-%Y")}"'
    _, message_numbers = mail.search(None, search_criteria)

    raw_emails = []
    # Iterate over each email matching the subject
    for message_number in message_numbers[0].split():
        # Fetch the email by its number
        _, data = mail.fetch(message_number, "(RFC822)")

        # Get the raw email content
        raw_email = data[0][1]
        raw_emails.append(raw_email)

    # Close the connection
    mail.logout()

    return raw_emails

# Provide your email account details, server information, and search criteria
username = 'data@data'
password = 'nice'
server = 'imap.data.com'
port = 993
subject = 'DATA'
from_date = datetime(2023, 4, 20)  # Specify the desired date

# Get the raw HTML from the emails
raw_emails = get_raw_html_from_email(username, password, server, port, subject, from_date)

# Create an empty list to store the filtered data
filtered_data_list = []

# Iterate over each raw HTML email content
for raw_email in raw_emails:
    # Create a Beautiful Soup object
    soup = BeautifulSoup(raw_email, 'html.parser')

    # Find all table elements in the HTML
    tables = soup.find_all('table')

    # Iterate over each table
    if tables:
        for table in tables:
            # Iterate over the rows of the table to extract the data
            rows = table.find_all('tr')
            for row in rows[1:]:  # Exclude the first row as it contains headers
                # Extract the data from each cell in the row
                cells = row.find_all('td')
                row_data = [cell.text.strip() for cell in cells]
                first_element = row_data[0]

                # Define the regular expression pattern
                pattern = r'^\d.*$'

                # Check if the first element matches the pattern
                if re.match(pattern, first_element):
                    # Process the row_data as required
                    first_element_parts = re.sub(r'\xa0+', ' ', re.sub(r'\s{2,}', ' ', row_data[1]))
                    first_element_parts = first_element_parts.split()  # Split the string into separate parts

                    filtered_data = [
                        ' '.join(first_element_parts),  # Combine the parts with a space
                        row_data[2].strip(),
                        row_data[7].strip()
                    ]
                    filtered_data_list.append(filtered_data)
    else:
        print("No tables found in the email.")

# Create a DataFrame from the filtered data
df = pd.DataFrame(filtered_data_list, columns=['Car_Truck_ID', 'Pay_Date', 'Line_Amt'])


# Splitting the "Car_Truck_ID" column
df[['Car_Truck_ID', 'Original_Date']] = df['Car_Truck_ID'].str.split(' ', expand=True)

# Reordering the columns
df = df[['Car_Truck_ID', 'Original_Date', 'Pay_Date', 'Line_Amt']]


output_file_path = './broker/email_retrieved_april_20_and_up.xlsx'

if os.path.exists(output_file_path):
    # Delete the file
    os.remove(output_file_path)
    print("File deleted successfully.")
else:
    print("File does not exist.")

# Save the DataFrame to an Excel file
df.to_excel(output_file_path, index=False)

print(f"Filtered data has been saved to {output_file_path}.")
