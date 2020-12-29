import praw


def reddit_bot(link, keywords):
    """If post was made longer than 10 minutes ago, module checks if wikihow link is a top-level comment
If true, post is skipped. If false, comment is made on post, then another definition is called to sticky and delete post"""
    comments_with_key_phrases = ''
    reddit = praw.Reddit(client_id='',
                         client_secret='',
                         user_agent='')

    submission = reddit.submission(url=link)

    submission.comments.replace_more(limit=0)

    # searches through top-level comments and checks if there is a wikihow link in them
    for top_level_comment in submission.comments:
        if any(phrases in top_level_comment.body.lower() for phrases in
               keywords):  # Checks if any keywords asked for are in the comments
            comments_with_key_phrases += "Comment: " + top_level_comment.body + '\n \n'
            comments_with_key_phrases += "[Link to comment]" + '(https://www.reddit.com' + top_level_comment.permalink + ')\n\n'

    return comments_with_key_phrases


def subreddit_search():
    # Use this to search for comments in several top posts in a specific subreddit
    reddit = praw.Reddit(client_id='',
                         client_secret='',
                         user_agent='')

    subreddit = reddit.subreddit('askreddit')
    submissions = subreddit.hot(limit=20)

    # gets url of newest posts on disneyvacations
    for submission in submissions:
        reddit_bot(submission.permalink, submission.title)


if __name__ == "__main__":
    comment_to_post = ''
    reddit = praw.Reddit(client_id='',
                         client_secret='',
                         user_agent='')

    subreddit = reddit.subreddit('MDD_Alerts')
    submissions = subreddit.new(limit=20)

    for submission in submissions:

        if submission.title.lower().startswith('post'):
            _, keyword_string = submission.title.split(':')
            keywords = keyword_string.lower().split(', ')
            comment_to_post = reddit_bot(submission.url, keywords)
            submission.reply(comment_to_post)
