import imaplib
import email
import time
from email.header import decode_header

EMAIL = "saikoo2020@yahoo.com"
PASSWORD = "epyiupdjqxbxekhl"
IMAP_SERVER = "imap.mail.yahoo.com"

IMPORTANT = ["upwork", "fiverr", "linkedin", "typewise", "job", "hiring", "interview", "application"]

def check():
    try:
        mail = imaplib.IMAP4_SSL(IMAP_SERVER)
        mail.login(EMAIL, PASSWORD)
        mail.select("inbox")
        
        status, messages = mail.search(None, '(UNSEEN SINCE "21-Jun-2026")')
        
        if messages[0]:
            for msg_id in messages[0].split()[-5:]:
                status, msg_data = mail.fetch(msg_id, "(RFC822)")
                msg = email.message_from_bytes(msg_data[0][1])
                
                subject = str(decode_header(msg["Subject"])[0][0]) if msg["Subject"] else ""
                sender = str(msg["From"])
                
                for word in IMPORTANT:
                    if word in sender.lower() or word in subject.lower():
                        print(f"\n🔔 {subject[:80]}")
                        print(f"   من: {sender}")
                        break
        
        mail.close()
        mail.logout()
    except:
        pass

print("🤖 بوت خفيف - بيفحص كل 60 ثانية...\n")
while True:
    check()
    time.sleep(60)