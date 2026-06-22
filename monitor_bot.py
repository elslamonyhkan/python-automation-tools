import imaplib
import email
import time
import json
import os
from email.header import decode_header

# ========== الإعدادات ==========
EMAIL = "saikoo2020@yahoo.com"
PASSWORD = "epyiupdjqxbxekhl"
IMAP_SERVER = "imap.mail.yahoo.com"
ALERT_FILE = r"C:\Users\Win10\Desktop\video_maker\alerts.txt"
# ==============================

IMPORTANT = {
    "upwork": "🟢 Upwork",
    "fiverr": "🟢 Fiverr", 
    "linkedin": "🔵 LinkedIn",
    "youtube": "🔴 YouTube",
    "typewise": "🟠 Typewise",
    "mixrank": "🟠 MixRank",
    "job": "💼 وظيفة",
    "hiring": "💼 توظيف",
    "interview": "⭐ مقابلة",
    "application": "📝 تقديم",
    "offer": "💰 عرض",
    "congratulations": "🎉 مبروك",
    "order": "🛒 طلب",
    "message": "💬 رسالة"
}

def alert(platform, subject, sender):
    """حفظ تنبيه في ملف"""
    msg = f"\n{'='*50}\n{platform}\nمن: {sender}\nالموضوع: {subject}\nالوقت: {time.strftime('%H:%M:%S')}\n{'='*50}\n"
    
    with open(ALERT_FILE, "a", encoding="utf-8") as f:
        f.write(msg)
    
    print(f"\n🔔 {platform}: {subject[:60]}")

def check_email():
    """فحص الإيميلات المهمة"""
    try:
        mail = imaplib.IMAP4_SSL(IMAP_SERVER)
        mail.login(EMAIL, PASSWORD)
        mail.select("inbox")
        
        status, messages = mail.search(None, '(UNSEEN SINCE "21-Jun-2026")')
        
        if messages[0]:
            ids = messages[0].split()[-10:]  # آخر 10
            for msg_id in ids:
                status, msg_data = mail.fetch(msg_id, "(RFC822)")
                msg = email.message_from_bytes(msg_data[0][1])
                
                subject = str(decode_header(msg["Subject"])[0][0]) if msg["Subject"] else ""
                if isinstance(subject, bytes):
                    subject = subject.decode('utf-8', errors='ignore')
                sender = str(msg["From"]).lower()
                
                for keyword, platform in IMPORTANT.items():
                    if keyword in sender or keyword in subject.lower():
                        alert(platform, subject, msg["From"])
                        break
        
        mail.close()
        mail.logout()
    except:
        pass

# --- تشغيل ---
print("=" * 60)
print("🤖 بوت المراقبة الشامل")
print("=" * 60)
print("✅ Fiverr    ✅ LinkedIn")
print("✅ Upwork    ✅ YouTube")
print("✅ Gmail     ✅ وظايف")
print("=" * 60)
print(f"📁 التنبيهات محفوظة في: {ALERT_FILE}")
print("(اضغط Ctrl+C للخروج)\n")

while True:
    check_email()
    time.sleep(120)  # كل دقيقتين