import git
from git import Repo
import os
import datetime

def repo_stats():
    # Check if the specified location is a git repository, if so, do not download
    if not os.path.exists('local_directory/.git'):
        repo = Repo.clone_from('https://gitlab.gnome.org/GNOME/connections', 'local_directory')
    else:
        repo = Repo('local_directory')

    # Then return a list of commits along with their messages, titles and dates
    commits = list(repo.iter_commits('master'))
    return [{'title': commit.summary, 'message': commit.message, 'date': datetime.datetime.fromtimestamp(commit.committed_date).strftime('%Y:%m:%d')} for commit in commits]