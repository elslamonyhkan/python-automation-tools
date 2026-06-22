import requests
import subprocess
import os
import asyncio
import pickle
import random
from datetime import datetime
import cv2
import numpy as np
import json
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload

# ========== الإعدادات ==========
BASE_PATH = r"C:\Users\Win10\Desktop\video_maker"
ASSETS_PATH = os.path.join(BASE_PATH, "assets")
SPEECH_PATH = os.path.join(BASE_PATH, "speech.mp3")
OUTPUT_PATH = os.path.join(BASE_PATH, "final_video.mp4")
TEMP_VIDEO = os.path.join(BASE_PATH, "temp_video.mp4")
CLIENT_SECRET_FILE = os.path.join(BASE_PATH, "client_secret.json")
SCOPES = ["https://www.googleapis.com/auth/youtube.upload"]
# ==============================

TRENDING_TOPICS = [
    {
        "type": "did_you_know",
        "title_prefix": "🤯 Did You Know?",
        "tags": ["didyouknow", "facts", "amazing", "mindblown", "viral", "trending", "fyp", "shorts"],
        "category": "28",
        "color": (26, 115, 232),
        "facts": [
            "The first computer bug was an actual insect - a moth found in 1947!",
            "A day on Venus is longer than a year on Venus! Mind blowing!",
            "Honey never spoils - archaeologists found 3000-year-old edible honey!",
            "Bananas are berries, but strawberries aren't! Shocking right?",
            "The Eiffel Tower grows 6 inches taller in summer due to heat!",
            "Octopuses have three hearts and blue blood! Nature is wild!",
            "A cloud can weigh more than a million pounds! Unbelievable!"
        ]
    },
    {
        "type": "psychology",
        "title_prefix": "🧠 Psychology Facts!",
        "tags": ["psychology", "facts", "mind", "humanbehavior", "darkpsychology", "viral", "trending", "shorts"],
        "category": "27",
        "color": (147, 52, 230),
        "facts": [
            "Your brain is more creative when you're tired! Stay up late!",
            "People who speak two languages may shift personalities between them!",
            "The color blue boosts productivity and focus instantly!",
            "Music affects your mood more than you realize! Science proves it!",
            "Laughter is contagious due to mirror neurons in your brain!",
            "Your memory works best in the morning! Study early!",
            "Deja vu is your brain checking its own memory! Creepy right?"
        ]
    },
    {
        "type": "history",
        "title_prefix": "📜 Weird History!",
        "tags": ["history", "facts", "weird", "shocking", "true", "viral", "trending", "shorts"],
        "category": "27",
        "color": (255, 109, 0),
        "facts": [
            "Ancient Egyptians used slabs of stone as pillows! Uncomfortable!",
            "Napoleon was once attacked by a horde of rabbits! True story!",
            "The shortest war in history lasted only 38 minutes!",
            "Oxford University is older than the Aztec Empire! Think about that!",
            "Ketchup was sold as medicine in the 1830s! Seriously!",
            "Cleopatra lived closer to the iPhone than to the pyramids!",
            "Vikings used urine to start fires! Gross but true!"
        ]
    },
    {
        "type": "space",
        "title_prefix": "🚀 Space Facts!",
        "tags": ["space", "universe", "facts", "mindblowing", "nasa", "viral", "trending", "shorts"],
        "category": "28",
        "color": (0, 0, 128),
        "facts": [
            "There is a planet made entirely of diamonds - 55 Cancri e!",
            "Neutron stars spin 600 times per SECOND! Mind blowing speed!",
            "Space is completely silent - no air for sound to travel!",
            "The Sun makes up 99.86% of the entire Solar System!",
            "Footprints on the Moon will last 100 million years!",
            "A teaspoon of a neutron star weighs 6 billion tons!",
            "Saturn could float in water if you found a big enough pool!"
        ]
    },
    {
        "type": "animals",
        "title_prefix": "🐾 Amazing Animals!",
        "tags": ["animals", "facts", "nature", "wildlife", "cute", "viral", "trending", "shorts"],
        "category": "27",
        "color": (52, 168, 83),
        "facts": [
            "Dolphins sleep with one eye open! They never fully sleep!",
            "Elephants are the only animals that CANNOT jump!",
            "Butterflies taste with their FEET! Nature is amazing!",
            "Cows have best friends and get stressed when separated!",
            "A group of flamingos is called a flamboyance! Fancy!",
            "Sea otters hold hands while sleeping to stay together! Cute!",
            "Penguins propose to their mates with a pebble! Romantic!"
        ]
    },
    {
        "type": "life_hack",
        "title_prefix": "💡 Life Hacks!",
        "tags": ["lifehacks", "tips", "useful", "tricks", "daily", "viral", "trending", "shorts"],
        "category": "26",
        "color": (232, 170, 26),
        "facts": [
            "Put a wooden spoon across a boiling pot to prevent overflow!",
            "Freeze grapes to chill wine without watering it down! Genius!",
            "Put your phone in airplane mode to charge it TWICE as fast!",
            "Use toothpaste to clean foggy car headlights instantly!",
            "Rub a walnut on scratched furniture to hide the marks! Magic!",
            "Freeze a candle before burning - it lasts TWICE as long!",
            "Use a straw to remove strawberry stems in one second!"
        ]
    },
    {
        "type": "reddit_story",
        "title_prefix": "😱 AITA Story!",
        "tags": ["reddit", "aita", "story", "storytime", "viral", "trending", "shorts", "redditstories"],
        "category": "22",
        "color": (180, 0, 0),
        "facts": [
            "My husband ate the birthday cake I made for MY birthday before I even got a slice. I cried and he said I was being dramatic. AITA?",
            "I told my best friend her boyfriend was cheating on her. She got mad at ME and blocked me. Now they broke up and she wants to be friends again. AITA for ignoring her?",
            "My roommate uses my expensive shampoo without asking. When I hid it, she called me petty. I told her to buy her own. AITA?",
            "I refused to lend my brother money for his third failed business. My parents said family helps family. AITA for saying no?",
            "I skipped my sister's wedding because she planned it on my final exam day. I offered to celebrate later but she disinvited me. AITA?",
            "My coworker takes credit for my work in meetings. I told our boss and now everyone says I threw her under the bus. AITA?",
            "I asked my neighbor to stop parking in my spot. He said I don't need it since I work from home. I had him towed. AITA?"
        ]
    }
]

def get_background(content_type):
    """اختيار خلفية حسب نوع المحتوى"""
    if content_type == "reddit_story":
        minecraft_path = os.path.join(ASSETS_PATH, "minecraft.mp4")
        if os.path.exists(minecraft_path):
            print("الخلفية: Minecraft Parkour (Reddit Story)")
            return minecraft_path
    
    all_files = os.listdir(ASSETS_PATH)
    files = [f for f in all_files if f.endswith((".mp4", ".jpg", ".png")) and f != "minecraft.mp4"]
    if files:
        chosen = random.choice(files)
        print(f"الخلفية: {chosen}")
        return os.path.join(ASSETS_PATH, chosen)
    return None

def get_content():
    """جلب محتوى تريند"""
    if random.random() < 0.4:
        topic = [t for t in TRENDING_TOPICS if t["type"] == "reddit_story"][0]
    else:
        topic = random.choice(TRENDING_TOPICS)
    
    print(f"النوع: {topic['type']}")
    
    facts = random.sample(topic["facts"], 3)
    if topic["type"] == "reddit_story":
        text = f"Am I the bad guy here? {facts[0]} Also, {facts[1]} And finally, {facts[2]}"
    else:
        text = f"{facts[0]} Also, {facts[1]} And here is one more: {facts[2]}"
    
    endings = [
        " Subscribe for more amazing content daily!",
        " Follow for daily stories and facts!",
        " Like and subscribe for more!",
        " Stay tuned for more!"
    ]
    text += random.choice(endings)
    
    print(f"تم جلب المحتوى: {text[:100]}...")
    return text, topic

async def generate_speech(text):
    """تحويل النص إلى كلام"""
    print("توليد الصوت...")
    clean = text.replace('"', '').replace("'", "").replace("\n", " ").replace("&", "and")
    
    from gtts import gTTS
    tts = gTTS(text=clean, lang='en', slow=False)
    tts.save(SPEECH_PATH)
    
    size = os.path.getsize(SPEECH_PATH)
    print(f"تم الصوت! الحجم: {size} بايت")

def create_shorts_video(bg_path, content_type, facts_text):
    """إنشاء فيديو Shorts احترافي بكل التأثيرات"""
    print("إنشاء فيديو Shorts احترافي...")
    
    sentences = [s.strip() + "." for s in facts_text.replace(" Also, ", "|").replace(" And here is one more: ", "|").replace(" And finally, ", "|").split("|") if s.strip()]
    sentences = [s for s in sentences if "subscribe" not in s.lower() and "follow" not in s.lower() and "stay tuned" not in s.lower() and "like and" not in s.lower()]
    
    emoji_map = {
        "did_you_know": ["🤯", "💡", "🔥"],
        "psychology": ["🧠", "💭", "🔮"],
        "history": ["📜", "👑", "⚔️"],
        "space": ["🚀", "🌌", "🪐"],
        "animals": ["🐾", "🦁", "🐬"],
        "life_hack": ["💡", "🔧", "✨"],
        "reddit_story": ["😱", "🍿", "💀"]
    }
    emojis = emoji_map.get(content_type["type"], ["🔥", "💡", "🤯"])
    
    if bg_path.endswith((".jpg", ".png")):
        img = cv2.imread(bg_path)
        use_video = False
    else:
        cap = cv2.VideoCapture(bg_path)
        use_video = True
    
    probe = subprocess.run(f'ffprobe -i "{SPEECH_PATH}" -show_entries format=duration -v quiet -of json', 
                          shell=True, capture_output=True, text=True)
    duration = float(json.loads(probe.stdout)["format"]["duration"])
    fps = 30
    total_frames = int(duration * fps)
    
    width, height = 720, 1280
    
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter(TEMP_VIDEO, fourcc, fps, (width, height))
    
    color = content_type["color"]
    b, g, r = int(color[0]), int(color[1]), int(color[2])
    
    sentence_timings = []
    if len(sentences) > 0:
        time_per_sentence = duration / len(sentences)
        for i in range(len(sentences)):
            sentence_timings.append((i * time_per_sentence, (i + 1) * time_per_sentence))
    
    for frame_num in range(total_frames):
        progress = frame_num / total_frames
        t = frame_num / fps
        
        if use_video:
            ret, frame = cap.read()
            if not ret:
                cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
                ret, frame = cap.read()
            h, w = frame.shape[:2]
            new_w = int(h * 9 / 16)
            x_start = (w - new_w) // 2
            frame = frame[:, x_start:x_start+new_w]
            frame = cv2.resize(frame, (width, height))
        else:
            effect = frame_num // 45 % 3
            
            if effect == 0:
                zoom = 1.0 + progress * 0.6
                shift_x, shift_y = 0, 0
            elif effect == 1:
                zoom = 1.5
                shift_x = int((1 - progress) * 100)
                shift_y = int(progress * 80)
            else:
                zoom = 1.3
                shift_x = int(progress * 150)
                shift_y = 50
            
            h, w = img.shape[:2]
            crop_w = int(w * 0.55)
            x_center = w // 2
            cropped = img[:, x_center - crop_w//2:x_center + crop_w//2]
            
            new_h, new_w = cropped.shape[:2]
            scaled_w = int(new_w * zoom)
            scaled_h = int(new_h * zoom)
            
            x_start = min(max(shift_x, 0), scaled_w - width)
            y_start = min(max(shift_y, 0), scaled_h - height)
            
            if scaled_w > 0 and scaled_h > 0:
                scaled = cv2.resize(cropped, (scaled_w, scaled_h))
                frame = scaled[y_start:y_start+height, x_start:x_start+width].copy()
            else:
                frame = np.zeros((height, width, 3), dtype=np.uint8)
        
        # شريط علوي
        cv2.rectangle(frame, (0, 0), (width, 80), (b, g, r), -1)
        
        topic_names = {
            "did_you_know": "DID YOU KNOW?",
            "psychology": "PSYCHOLOGY FACTS",
            "history": "WEIRD HISTORY",
            "space": "SPACE FACTS",
            "animals": "AMAZING ANIMALS",
            "life_hack": "LIFE HACKS",
            "reddit_story": "REDDIT STORYTIME"
        }
        topic_text = topic_names.get(content_type["type"], "FACTS")
        cv2.putText(frame, topic_text, (30, 55), 
                   cv2.FONT_HERSHEY_DUPLEX, 1.3, (255, 255, 255), 2)
        
        # عداد
        current_fact_num = 1
        for i, (start_time, end_time) in enumerate(sentence_timings):
            if t >= start_time and i < len(sentences):
                current_fact_num = i + 1
        
        counter_text = f"Fact {current_fact_num}/3"
        counter_size = cv2.getTextSize(counter_text, cv2.FONT_HERSHEY_DUPLEX, 0.8, 2)[0]
        cv2.rectangle(frame, (width - counter_size[0] - 30, 8), (width - 5, 72), (0, 0, 0), -1)
        cv2.rectangle(frame, (width - counter_size[0] - 30, 8), (width - 5, 72), (b, g, r), 3)
        cv2.putText(frame, counter_text, (width - counter_size[0] - 15, 50), 
                   cv2.FONT_HERSHEY_DUPLEX, 0.8, (255, 255, 255), 2)
        
        # كتابة النص مع حركة
        current_sentence = ""
        current_idx = 0
        for i, (start_time, end_time) in enumerate(sentence_timings):
            if start_time <= t <= end_time and i < len(sentences):
                current_sentence = sentences[i]
                current_idx = i
                break
        
        if current_sentence:
            sentence_start = sentence_timings[current_idx][0]
            time_in_sentence = t - sentence_start
            anim_progress = min(time_in_sentence / 0.3, 1.0)
            alpha = min(anim_progress, 1.0)
            
            words = current_sentence.split()
            lines = []
            current_line = ""
            for word in words:
                test_line = current_line + " " + word if current_line else word
                if len(test_line) < 28:
                    current_line = test_line
                else:
                    if current_line:
                        lines.append(current_line)
                    current_line = word
            if current_line:
                lines.append(current_line)
            
            text_height = len(lines) * 55 + 40
            base_y = height // 2 - text_height // 2 - 120
            
            slide_offset = int((1 - anim_progress) * 80)
            y_start_text = base_y + slide_offset
            
            if anim_progress > 0.1:
                overlay = frame.copy()
                cv2.rectangle(overlay, (20, y_start_text), (width - 20, y_start_text + text_height), (0, 0, 0), -1)
                frame = cv2.addWeighted(frame, 1 - 0.45 * alpha, overlay, 0.45 * alpha, 0)
            
            if anim_progress > 0.3:
                emoji = emojis[current_idx % len(emojis)]
                cv2.putText(frame, emoji, ((width - cv2.getTextSize(emoji, cv2.FONT_HERSHEY_DUPLEX, 2.8, 4)[0][0]) // 2, y_start_text - 40), 
                           cv2.FONT_HERSHEY_DUPLEX, 2.8, (255, 255, 255), 4)
            
            for i, line in enumerate(lines):
                text_size = cv2.getTextSize(line, cv2.FONT_HERSHEY_DUPLEX, 0.85, 2)[0]
                text_x = (width - text_size[0]) // 2
                text_y = y_start_text + 45 + i * 55
                
                cv2.putText(frame, line, (text_x + 2, text_y + 2), 
                           cv2.FONT_HERSHEY_DUPLEX, 0.85, (0, 0, 0), 2)
                cv2.putText(frame, line, (text_x, text_y), 
                           cv2.FONT_HERSHEY_DUPLEX, 0.85, (255, 255, 255), 2)
        
        # شريط سفلي
        if int(t) % 4 < 3:
            overlay2 = frame.copy()
            cv2.rectangle(overlay2, (0, height-100), (width, height), (0, 0, 0), -1)
            frame = cv2.addWeighted(frame, 0.7, overlay2, 0.3, 0)
            
            sub_text = "SUBSCRIBE FOR MORE! 🔔"
            text_size = cv2.getTextSize(sub_text, cv2.FONT_HERSHEY_DUPLEX, 0.85, 2)[0]
            text_x = (width - text_size[0]) // 2
            cv2.putText(frame, sub_text, (text_x, height-45), 
                       cv2.FONT_HERSHEY_DUPLEX, 0.85, (255, 255, 255), 2)
        
        # وميض
        for i, (start_time, _) in enumerate(sentence_timings):
            if abs(t - start_time) < 0.08:
                flash = np.ones_like(frame) * 255
                frame = cv2.addWeighted(frame, 0.7, flash, 0.3, 0)
                break
        
        out.write(frame)
    
    if use_video:
        cap.release()
    out.release()
    
    cmd = f'ffmpeg -i "{TEMP_VIDEO}" -i "{SPEECH_PATH}" -c:v libx264 -preset fast -crf 28 -c:a aac -shortest -y "{OUTPUT_PATH}"'
    subprocess.run(cmd, shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    
    if os.path.exists(TEMP_VIDEO):
        os.remove(TEMP_VIDEO)
    
    print("تم فيديو Shorts احترافي!")

def upload_to_youtube(video_file, title, description, tags, category):
    """رفع إلى يوتيوب"""
    print("رفع إلى يوتيوب...")
    credentials = None
    token_path = os.path.join(BASE_PATH, "token.pickle")
    
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
    
    youtube = build("youtube", "v3", credentials=credentials)
    
    body = {
        "snippet": {
            "title": title,
            "description": description,
            "tags": tags,
            "categoryId": category
        },
        "status": {
            "privacyStatus": "public",
            "selfDeclaredMadeForKids": False
        }
    }
    
    media = MediaFileUpload(video_file, chunksize=-1, resumable=True)
    request = youtube.videos().insert(part=",".join(body.keys()), body=body, media_body=media)
    response = request.execute()
    print(f"✅ رابط: https://youtube.com/shorts/{response['id']}")
    return response['id']

async def main():
    print("=" * 60)
    print("🎬 إنشاء YouTube Shorts تريند...")
    print("=" * 60)
    
    content_text, content_type = get_content()
    
    bg_path = get_background(content_type["type"])
    if not bg_path:
        print("❌ مفيش خلفيات!")
        return
    
    await generate_speech(content_text)
    create_shorts_video(bg_path, content_type, content_text)
    
    title_templates = {
        "did_you_know": [
            "This Fact Will BLOW Your Mind! 🤯 #{}",
            "You Won't Believe This Is TRUE! 😱 #{}",
            "This Changed Everything I Knew! 🤯 #{}"
        ],
        "psychology": [
            "Your Brain Does THIS In Secret! 🧠 #{}",
            "This Psychology Trick Works EVERY Time! 😱 #{}",
            "The Dark Side of Your Mind! 🧠 #{}"
        ],
        "history": [
            "This Historical Fact Sounds FAKE! 📜 #{}",
            "They Never Taught You THIS In School! 📚 #{}",
            "The Weirdest Thing In History! 🤯 #{}"
        ],
        "space": [
            "This Planet Is Made of DIAMONDS! 💎 #{}",
            "Space Is SCARIER Than You Think! 🌌 #{}",
            "NASA Doesnt Want You To Know THIS! 🚀 #{}"
        ],
        "animals": [
            "This Animal Has THREE Hearts! 🐙 #{}",
            "Animals Are SMARTER Than You Think! 🐬 #{}",
            "CUTEST Animal Facts Ever! 🐾 #{}"
        ],
        "life_hack": [
            "This Simple Hack Will SAVE You! 💡 #{}",
            "You've Been Doing This WRONG! 😱 #{}",
            "GENIUS Life Hacks You NEED! 🧠 #{}"
        ],
        "reddit_story": [
            "AITA For THIS?! 😱🍿 #{}",
            "This Story Will SHOCK You! 💀 #{}",
            "Reddit Said I Was WRONG! 😱 #{}",
            "Am I The Bad Guy Here?! 🍿 #{}"
        ]
    }
    
    templates = title_templates.get(content_type["type"], title_templates["did_you_know"])
    title = random.choice(templates).format(random.randint(100, 999))
    
    description = f"""{content_text}

━━━━━━━━━━━━━━━━━━━━
📌 Daily Dose of Facts - New Videos Every Day!

🔥 SUBSCRIBE for daily amazing facts!
🔔 Turn ON notifications so you never miss a video!

━━━━━━━━━━━━━━━━━━━━
#shorts #facts #trending #viral #fyp #mindblown #amazing"""
    
    try:
        upload_to_youtube(OUTPUT_PATH, title, description, content_type["tags"], content_type["category"])
    except Exception as e:
        print(f"فشل: {e}")
        print("تم حفظ الفيديو محلياً في مجلد المشروع")
    
    print("=" * 60)

asyncio.run(main())