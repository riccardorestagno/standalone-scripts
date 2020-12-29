import praw

words_to_search = ['']
link_to_search = ''
reddit = praw.Reddit(client_id='',
                     client_secret='',
                     user_agent='')

submission = reddit.submission(url=link_to_search)

submission.comments.replace_more(limit=0)
for top_level_comment in submission.comments:
    # print(dir(top_level_comment))
    # break
    if any(words in top_level_comment.body.lower() for words in words_to_search):
        print(top_level_comment.body)
        print(top_level_comment.id)
