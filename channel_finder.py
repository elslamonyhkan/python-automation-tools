from googleapiclient.discovery import build
import os

API_KEY = "AIzaSyBxkghqlQIgMsXMJXefcAgIRfvhzlsQBAQ"

def find_channels_from_videos(keyword, max_results=100):
    """يدور على قنوات صغيرة من الفيديوهات"""
    youtube = build("youtube", "v3", developerKey=API_KEY)
    
    channels = {}
    
    request = youtube.search().list(
        q=keyword,
        type="video",
        part="snippet",
        maxResults=max_results,
        order="date",
        relevanceLanguage="en"
    )
    response = request.execute()
    
    for item in response.get("items", []):
        channel_id = item["snippet"]["channelId"]
        channel_title = item["snippet"]["channelTitle"]
        video_title = item["snippet"]["title"]
        video_id = item["id"]["videoId"]
        
        if channel_id not in channels:
            try:
                stats = youtube.channels().list(
                    part="statistics",
                    id=channel_id
                ).execute()
                
                if stats.get("items"):
                    sub_count = int(stats["items"][0]["statistics"].get("subscriberCount", 0))
                    video_count = int(stats["items"][0]["statistics"].get("videoCount", 0))
                    
                    # قنوات صغيرة ونشطة
                    if 10 < sub_count < 2000 and video_count >= 5:
                        channels[channel_id] = {
                            "title": channel_title,
                            "subscribers": sub_count,
                            "videos": video_count,
                            "channel_url": f"https://youtube.com/channel/{channel_id}",
                            "latest_video": f"https://youtube.com/watch?v={video_id}",
                            "video_title": video_title
                        }
                        print(f"✅ {channel_title} | {sub_count} مشترك | {video_count} فيديو")
            except:
                pass
    
    return list(channels.values())

# --- تشغيل ---
print("جاري البحث عن قنوات صغيرة من فيديوهات حديثة...\n")

all_channels = []
keywords = ["tech review", "gaming channel", "cooking recipe", "travel vlog", "fitness workout", "music cover", "comedy skit", "tutorial how to", "podcast episode", "product review"]
for kw in keywords:
    chs = find_channels_from_videos(kw, 50)
    all_channels.extend(chs)

# إزالة المكررين
seen = set()
unique = []
for ch in all_channels:
    if ch["channel_url"] not in seen:
        seen.add(ch["channel_url"])
        unique.append(ch)

print(f"\n🎯 وجدنا {len(unique)} قناة صغيرة")

# حفظ في ملف
with open("target_channels.txt", "w", encoding="utf-8") as f:
    for ch in unique:
        f.write(f"{ch['title']}\n")
        f.write(f"المشتركين: {ch['subscribers']} | الفيديوهات: {ch['videos']}\n")
        f.write(f"القناة: {ch['channel_url']}\n")
        f.write(f"آخر فيديو: {ch['latest_video']} - {ch['video_title']}\n")
        f.write("---\n")

print(f"✅ حفظنا {len(unique)} قناة في target_channels.txt")