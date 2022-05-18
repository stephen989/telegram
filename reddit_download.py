import ffmpeg
import youtube_dl
import praw
from os import remove
with open("auth/reddit.txt") as f:
    reddit_id, reddit_secret = f.read().splitlines()

def send(n, id, bot, sub = "aww"):
    reddit = praw.Reddit(client_id=reddit_id, client_secret=reddit_secret, user_agent='my_user_agent')
    ydl_opts = {
    'outtmpl': 'aww/%(title)s.%(ext)s'
}
    posts = list(reddit.subreddit(sub).hot(limit=5*n))
    posts = [post for post in posts if post.is_video][:n]
    for post in posts:
        if post.is_video:
            with youtube_dl.YoutubeDL(ydl_opts) as ydl:
                ydl.download([post.url])
                title = ydl.extract_info(post.url, download = False)["title"]
                bot.send_video(id, video = open(f"aww/{title}.mp4", "rb"))
                remove(f"aww/{title}.mp4")
            