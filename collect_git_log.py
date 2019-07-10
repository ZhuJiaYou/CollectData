from git import Repo, GitCommandError
from repository import Repository
import os

count1 = 0
count2 = 0
with open("/srv/bug_repos/repo_star500_commit2000_list.txt", "r") as f:
    for line in f:
        if line[:6] != "NOTICE" and line[:8] != "LANGUAGE":
            count1 += 1
            repo = Repository(line.strip())
        else:
            print(line)
            continue

        repo_dir = os.path.join("/srv/bug_repos", repo.language, repo.owner, repo.name)
        repo_git = Repo(repo_dir)
        git = repo_git.git
        try:
            logs = git.log("--abbrev-commit")
        except GitCommandError:
            print("{} - {} - {} ERROR!".format(repo.language, repo.owner, repo.name))

        with open("/srv/bug_repo_info/git_log/{}_{}_{}.txt".format(repo.language, repo.owner, repo.name),
                  "w") as fw:
            fw.write(logs.encode("utf-8", errors="xmlcharrefreplace").decode("utf-8"))
            count2 += 1

print("ALL IS FINE! {} -- {}".format(count1, count2))
