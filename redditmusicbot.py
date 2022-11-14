import json
import urllib.request
import re
import urllib
import praw
import os
from dotenv import load_dotenv

load_dotenv()


reddit = praw.Reddit(
    client_id=os.getenv('API_CLIENT'),
    client_secret=os.getenv('API_SECRET'),
    password=os.getenv('REDDIT_PASSWORD'),
    user_agent="Reddit Music Bot",
    username=os.getenv('REDDIT_USERNAME'),
)

def get_yt_url(song_name):
    search_string = song_name.replace(" ","+")
    html = urllib.request.urlopen("https://www.youtube.com/results?search_query=" + search_string)
    video_ids = ""
    data = ""
    video_ids = re.findall(r"watch\?v=(\S{11})", html.read().decode())

    params = {"format": "json", "url": "https://www.youtube.com/watch?v=%s" % video_ids[0]}
    url = "https://www.youtube.com/oembed"
    query_string = urllib.parse.urlencode(params)
    url = url + "?" + query_string

    with urllib.request.urlopen(url) as response:
        response_text = response.read()
        data = json.loads(response_text.decode())
        youtube_url = "https://www.youtube.com/watch?v=" + video_ids[0]
        youtube_music_url = "https://music.youtube.com/watch?v=" + video_ids[0]
        title = data['title']

    return youtube_url, youtube_music_url, title

target_sub = "artofml"
subreddit = reddit.subreddit(target_sub)
trigger_phrase = "!play"

for comment in subreddit.stream.comments(skip_existing=True):  
    if trigger_phrase in comment.body:  
        search_word = comment.body.replace(trigger_phrase, "")
        url_yt, url_ym, title_yt = get_yt_url(search_word)
        comment.reply(body = title_yt + " on [YouTube](" + url_yt + ")" + '\n\n' + title_yt + " on [YouTube Music](" + url_ym + ")")
        search_word, url_ym, url_yt, title_yt = None, None, None, None