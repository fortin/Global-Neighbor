import os

from atproto import Client, models
from decouple import config

USERNAME = config("BLUESKY_USERNAME")
PASSWORD = config("BLUESKY_PASSWORD")


def get_latest_bluesky_posts(limit=5):
    client = Client()
    client.login(USERNAME, PASSWORD)

    feed = client.app.bsky.feed.get_author_feed(
        {
            "actor": USERNAME,
            "limit": 10,
        },
    )

    posts = []

    for item in feed.feed:
        post: models.AppBskyFeedDefs.PostView = item.post
        record = post.record

        # Skip replies
        if hasattr(record, "reply") and record.reply is not None:
            continue

        posts.append(
            {"text": record.text, "timestamp": record.created_at, "uri": post.uri}
        )

        if len(posts) >= limit:
            break

    return posts
