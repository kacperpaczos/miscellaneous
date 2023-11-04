from repo_stats import repo_stats

for commit in repo_stats():
    print("Title: ", commit['title'])
    print("Message: ", commit['message'])
    print("Date: ", commit['date'])

