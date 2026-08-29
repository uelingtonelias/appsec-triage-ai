from git import Repo

class GitTools:
    def last_commit(self, repo_path):
        repo = Repo(repo_path)
        return repo.head.commit.hexsha