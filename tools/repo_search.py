import os

class RepoSearch:
    def search(self, repo_path, text):
        matches = []
        for root, _, files in os.walk(repo_path):
            for file in files:
                path = os.path.join(root, file)
                try:
                    with open(
                        path,
                        encoding="utf8",
                        errors="ignore"
                    ) as f:
                        if text in f.read():
                            matches.append(path)
                except Exception:
                    pass
        return matches