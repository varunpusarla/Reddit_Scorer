import praw
from praw.models import MoreComments
from decouple import config

reddit = praw.Reddit(client_id=config('client_id', default=''),
                     client_secret=config('client_secret', default=''),
                     username=config('username', default=''),
                     password=config('password', default=''),
                     user_agent=config('user_agent', default=''))

subreddit_list = reddit.subreddits.default(limit=50)

for subreddit in subreddit_list:
    print(f"\n\nSubreddit: {subreddit.display_name}")

    # Getting the top 10 posts in the subreddit
    top_posts = subreddit.top(limit=10)

    # Calculating the subreddit score
    subreddit_score = 0
    num_posts = 0

    # Looping through the top 10 posts
    for post in top_posts:
        num_posts += 1

        # Calculating the post score

        post_score = 0
        for comment in post.comments:
            if isinstance(comment, MoreComments):
                continue

            if comment.score > 0:
                post_score += comment.score / post.num_comments

        print(f"Post number {num_posts} Score:{post_score:.2f}")
        subreddit_score += post_score

    # Calculating the subreddit score
    if num_posts > 0:
        subreddit_score /= num_posts

    print(f"Subreddit score: {subreddit_score:.2f}")
