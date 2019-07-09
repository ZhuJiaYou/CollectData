from git import Repo, GitCommandError
import os


class Repository:
    def __init__(self, repo_str):
        repo_list = repo_str.split("\t")
        self.language = repo_list[0]
        self.name = repo_list[1]
        self.owner = repo_list[2]
        self.stars = repo_list[3]
        self.commits = repo_list[4]
        self.url = repo_list[5]
        self.description = repo_list[6]


if __name__ == '__main__':
    REPOS_DIR_PRE = "/srv/bug_repos"

    with open("/srv/bug_repos/repo_star500_commit2000_list.txt", "r") as f:
        for line in f:
            if line[:6] != "NOTICE":
                repo = Repository(line.strip())
                try:
                    Repo.clone_from(repo.url, os.path.join(REPOS_DIR_PRE, repo.language, repo.owner, repo.name),
                                    no_checkout=True)
                except GitCommandError:
                    print("{}/{} CLONE ERROR!".format(repo.owner, repo.name))
            else:
                print(line)
