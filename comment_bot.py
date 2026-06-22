import pickle
import os
import time
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build

# ========== الإعدادات ==========
BASE_PATH = r"C:\Users\Win10\Desktop\video_maker"
CLIENT_SECRET_FILE = os.path.join(BASE_PATH, "client_secret.json")
SCOPES = ["https://www.googleapis.com/auth/youtube.force-ssl"]
# ==============================

# رسايل متنوعة
MESSAGES = [
    "Nice video! If you ever need help making Shorts, check my channel @Facts20261 - link in my bio 🔥",
    "Great content! I help small creators with Shorts - info in my channel bio 👆",
    "Love this! Check my channel @Facts20261 if you want help growing 🚀",
    "Awesome work! I make Shorts for creators - details on my channel page 💯",
    "Keep it up! My channel @Facts20261 has info if you need Shorts help 🙌"
]

def get_authenticated_service():
    """توثيق يوتيوب"""
    credentials = None
    token_path = os.path.join(BASE_PATH, "token_comment.pickle")
    
    if os.path.exists(token_path):
        with open(token_path, "rb") as token:
            credentials = pickle.load(token)
    
    if not credentials or not credentials.valid:
        if credentials and credentials.expired and credentials.refresh_token:
            credentials.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(CLIENT_SECRET_FILE, SCOPES)
            credentials = flow.run_local_server(port=0)
        with open(token_path, "wb") as token:
            pickle.dump(credentials, token)
    
    return build("youtube", "v3", credentials=credentials)

def post_comment(youtube, video_id, message):
    """ينشر تعليق على فيديو"""
    try:
        request = youtube.commentThreads().insert(
            part="snippet",
            body={
                "snippet": {
                    "videoId": video_id,
                    "topLevelComment": {
                        "snippet": {
                            "textOriginal": message
                        }
                    }
                }
            }
        )
        response = request.execute()
        print(f"✅ تم التعليق!")
        return True
    except Exception as e:
        print(f"❌ فشل: {str(e)[:100]}")
        return False

def extract_video_id(url):
    """يستخرج video ID من الرابط"""
    if "watch?v=" in url:
        return url.split("watch?v=")[1].split("&")[0]
    return url

# --- تشغيل ---
print("=" * 60)
print("🤖 بوت التعليقات - YouTube Shorts")
print("=" * 60)

# توثيق
print("\nجاري التوثيق...")
youtube = get_authenticated_service()
print("✅ تم التوثيق!")

# قراءة القنوات
print("\nجاري قراءة القنوات...")
with open("target_channels.txt", "r", encoding="utf-8") as f:
    content = f.read()

# استخراج روابط الفيديوهات
import re
video_urls = re.findall(r'https://youtube\.com/watch\?v=[a-zA-Z0-9_-]+', content)
print(f"✅ وجدنا {len(video_urls)} فيديو")

# تعليق على أول 10 فيديوهات (تجربة)
print("\nجاري نشر التعليقات...\n")
import random

count = 0
for url in video_urls[:50]:  # أول 50
    video_id = extract_video_id(url)
    message = random.choice(MESSAGES)
    
    print(f"📝 فيديو: {video_id}")
    if post_comment(youtube, video_id, message):
        count += 1
    
    time.sleep(15)  # 15 ثانية بين كل تعليق (أمان أكتر)

print(f"\n🎉 تم! {count} تعليق نُشروا بنجاح")