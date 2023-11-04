import git
from git import Repo
import os
import shutil
import datetime

def repo_stats(repo_url):
    # Get directory name from the link
    directory_name = repo_url.split('/')[-1]
    # If the directory already exists, append what was previously from the url to the name
    if os.path.exists(directory_name):
        directory_name += repo_url.split('/')[-2]
    # If the name is still taken, write that you cannot perform the operation due to project collisions
    if os.path.exists(directory_name):
        raise Exception("Could not perform operation due to project collisions")
    # Check if the specified location is a git repository, if so, do not download
    if not os.path.exists(f'{directory_name}/.git'):
        repo = Repo.clone_from(repo_url, directory_name)
    else:
        repo = Repo(directory_name)

    # Then return a list of commits along with their messages, titles and dates
    commits = list(repo.iter_commits('master'))
    commit_data = [{'title': commit.summary, 'message': commit.message, 'date': datetime.datetime.fromtimestamp(commit.committed_date).strftime('%Y:%m:%d')} for commit in commits]
    
    # After finishing work, delete the folder even if it is not empty.
    shutil.rmtree(directory_name)
    
    return commit_data
