import praw
from datetime import datetime, timedelta


def hours_posted(submission):
    """Gets the time that passed (in hours) from when the post was made. (All time is converted to UTC)"""
    time_created = submission.created_utc
    current_time = datetime.utcnow()
    time_posted = datetime.utcfromtimestamp(time_created)
    time_difference_in_hours = (current_time - time_posted) / timedelta(hours=1)
    return time_difference_in_hours


def post_made_today_check(user, link):
    """ Returns true if the user who just posted, has already made a previous post within the past 24 hours
		Returns false otherwise"""

    reddit = praw.Reddit(client_id='',
                         client_secret='',
                         user_agent='')

    subreddit = reddit.subreddit('')
    submissions = subreddit.new(limit=50)  # Change limit accordingly (max 1000)

    for submission in submissions:
        if link == submission.permalink:  # Ignores the post we are checking
            continue
        # If a post has been made in the past 24 hours by the same user, return true
        if user == submission.author.name and hours_posted(submission) < 24:
            return True

    return False


if __name__ == "__main__":

    reddit = praw.Reddit(client_id='',
                         client_secret='',
                         user_agent='',
                         username='',
                         password='')

    subreddit = reddit.subreddit('')  # Enter
    submissions = subreddit.new(limit=50)  # Change limit accordingly (max 1000)

    for submission in submissions:
        if post_made_today_check(submission.author.name, submission.permalink):
            submission.reply("Enter Reply Here")  # replies to post
            submission.mod.remove()  # Deletes the post
        break
