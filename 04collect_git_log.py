from git import Repo, GitCommandError
from repository import Repository
import os

count1 = 0
count2 = 0
with open("E:\\experimentalData\\private\\repo_star500_commit2000_list.txt", "r", encoding="utf8") as f:
    for line in f:
        if line[:6] != "NOTICE" and line[:8] != "LANGUAGE":
            count1 += 1
            repo = Repository(line.strip())
        else:
            print(line)
            continue

        repo_dir = os.path.join("E:\\experimentalData\\private\\bugRepos", repo.language, repo.owner, repo.name)
        repo_git = Repo(repo_dir)
        git = repo_git.git
        print("AAAAAAAAAAAAAA")
        try:
            logs = git.log("--date=format-local:%Y-%m-%dT%H:%M:%SZ")
            # logs = git.log("--abbrev-commit")
            # print(logs)
        except GitCommandError:
            print("{} - {} - {} ERROR!".format(repo.language, repo.owner, repo.name))

        with open("E:\\experimentalData\\private\\gitLogs\\{}_{}_{}.txt".format(repo.language, repo.owner, repo.name),
                  "w", encoding="utf8") as fw:
            fw.write(logs.encode("utf-8", errors="xmlcharrefreplace").decode("utf-8"))
            count2 += 1

print("ALL IS FINE! {} -- {}".format(count1, count2))
