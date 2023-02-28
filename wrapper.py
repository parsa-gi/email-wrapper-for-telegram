import imaplib
import email
import re
import requests
# Set up email account
mail = imaplib.IMAP4_SSL('IMAP_URL')
mail.login('MAIL_USERNAME', 'MAIL_PASSWORD')
mail.select('inbox')
# Search for unread messages
SENDER = 'SENDER_EMAIL'
search_criteria = f'(UNSEEN FROM "{SENDER}")'
status, data = mail.search(None, search_criteria)
# Iterate through messages
for num in data[0].split():
    status, data = mail.fetch(num, '(RFC822)')
    email_message = email.message_from_bytes(data[0][1])

    # Extract email details
    sender = email.utils.parseaddr(email_message['From'])[1]
    subject = email_message.get('Subject')
    if email_message.is_multipart():
    # If the message has multiple parts, iterate over them and check for a text/plain part
        for part in email_message.get_payload():
            if part.get_content_type() == 'text/plain':
                body = part.get_payload(decode=True).decode('utf-8')
                break
    else:
    # If the message is not multipart, extract the text payload directly
        body = email_message.get_payload(decode=True).decode('utf-8')
    # Format message for Telegram
    message = f"*From:* {sender}\n*Subject:* {subject}\n*Message:* {body}"
    message = re.sub(r'<.*?>', '', message)  # Remove HTML tags
    chat_id = 'CHAT_ID'
    TOKEN = "BOT_TOKEN"

    message_chunks = [message[i:i+4096] for i in range(0, len(message), 4096)]
    for message_chunk in message_chunks:

        url = f"https://api.telegram.org/bot{TOKEN}/sendMessage?chat_id={chat_id}&text={message_chunk}"
        print(requests.get(url).json())
    mail.store(num, '+FLAGS', '\\Seen')

# Close email connection
mail.close()
mail.logout()
