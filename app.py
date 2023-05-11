import praw
import luigi
import datetime as dt
# import schedule
from praw.models import MoreComments
from decouple import config


class ExtractDataTask(luigi.Task):
    """Task to extract data from the Reddit API"""

    client_id = luigi.Parameter()
    client_secret = luigi.Parameter()
    user_agent = luigi.Parameter()
    username = luigi.Parameter()
    password = luigi.Parameter()
    limit_subreddits = luigi.IntParameter(default=50)
    limit_posts = luigi.IntParameter(default=10)

    def output(self):
        return luigi.LocalTarget(f"reddit_data_{dt.datetime.now().strftime('%Y%m%d%H%M%S')}.txt")

    def run(self):
        reddit = praw.Reddit(client_id=self.client_id,
                             client_secret=self.client_secret,
                             username=self.username,
                             password=self.password,
                             user_agent=self.user_agent)

        subreddits_list = reddit.subreddits.default(limit=self.limit_subreddits)

        results = []

        for subreddit in subreddits_list:
            top_posts = subreddit.top(limit=self.limit_posts)
            post_scores = []

            for post in top_posts:
                comments = post.comments
                comment_scores = []
                for comment in comments:
                    if isinstance(comment, MoreComments):
                        continue
                    comment_scores.append(comment.score)
                if comment_scores:
                    post_scores.append(sum(comment_scores) / len(comment_scores))
            if post_scores:
                subreddit_score = sum(post_scores) / len(post_scores)
                results.append((subreddit.display_name, subreddit_score))
        with self.output().open('w') as f:
            f.write("subreddit,score\n")
            for result in results:
                f.write(f"{result[0]},{result[1]}\n")


class RedditPipeline(luigi.WrapperTask):
    """Wrapper task to run the pipeline"""

    client_id = luigi.Parameter()
    client_secret = luigi.Parameter()
    username = luigi.Parameter()
    password = luigi.Parameter()
    user_agent = luigi.Parameter()
    limit_subreddits = luigi.IntParameter(default=2)
    limit_posts = luigi.IntParameter(default=2)

    def requires(self):
        return ExtractDataTask(client_id=self.client_id,
                               client_secret=self.client_secret,
                               username=self.username,
                               password=self.password,
                               user_agent=self.user_agent,
                               limit_subreddits=self.limit_subreddits,
                               limit_posts=self.limit_posts)


if __name__ == '__main__':
    client_id = config('client_id', default='')
    client_secret = config('client_secret', default='')
    user_agent = config('user_agent', default='')
    username = config('username', default='')
    password = config('password', default='')
    limit_subreddits = 50
    limit_posts = 10
    #
    # # Define the task scheduler
    # schedule.every().day.at("06:00").do(luigi.build, [RedditPipeline(client_id=client_id,
    #                                                                  client_secret=client_secret,
    #                                                                  username=username,
    #                                                                  password=password,
    #                                                                  user_agent=user_agent,
    #                                                                  limit_subreddits=limit_subreddits,
    #                                                                  limit_posts=limit_posts)],
    #                                     local_scheduler=True)
    # schedule.every().day.at("18:00").do(luigi.build, [RedditPipeline(client_id=client_id,
    #                                                                  client_secret=client_secret,
    #                                                                  username=username,
    #                                                                  password=password,
    #                                                                  user_agent=user_agent,
    #                                                                  limit_subreddits=limit_subreddits,
    #                                                                  limit_posts=limit_posts)], local_scheduler=True)

    luigi.build([RedditPipeline(client_id=client_id,
                                client_secret=client_secret,
                                username=username,
                                password=password,
                                user_agent=user_agent,
                                limit_subreddits=limit_subreddits,
                                limit_posts=limit_posts)], local_scheduler=True)
