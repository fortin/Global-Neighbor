from datetime import datetime

from atproto import Client
from decouple import config

username = config("BLUESKY_USERNAME")


def get_latest_top_level_posts(handle=username, limit=5):
    client = Client()
    password = config("BLUESKY_PASSWORD")
    client.login(username, password)

    profile = client.app.bsky.actor.get_profile(
        {"actor": username},
    )
    display_name = profile.display_name or username  # fallback just in case

    top_level_posts = []

    feed = client.app.bsky.feed.get_author_feed(
        {"actor": handle, "limit": 100},
    )

    posts = []

    for item in feed.feed:
        post = item.post
        if item.reply is not None or item.reason is not None:
            continue

        text = post.record.text
        created = post.record.created_at
        created_dt = datetime.fromisoformat(created.replace("Z", "+00:00"))
        post_url = post.uri.replace("at://", "https://bsky.app/profile/").replace(
            "/app.bsky.feed.post/", "/post/"
        )

        posts.append(
            {
                "text": text,
                "created": created_dt,
                "url": post_url,
            }
        )

        if len(posts) >= limit:
            break

    # print(f"Returning {len(posts)} top-level posts")
    return posts, display_name
