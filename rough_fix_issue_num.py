import re
from repository import Repository


with open("/srv/bug_repo_info/rough_issue_num.txt", "w") as fi:
    fi.write("REPO\tGIT_LOG\tPULL_REQUEST\n")

with open("/srv/bug_repos/repo_star500_commit2000_list.txt", "r") as f:
    for line in f:
        if line[:6] != "NOTICE" and line[:8] != "LANGUAGE":
            repo = Repository(line.strip())
        else:
            print(line)
            continue

        count_git_log = 0
        count_pull_request = 0
        pattern = r"\bfix(s|es|d|ed)?\s*(#|issue|issues)?\s*\d+"
        filename = "{}_{}_{}.txt".format(repo.language, repo.owner, repo.name)

        with open("/srv/bug_repo_info/git_log/{}".format(filename), "r") as f1:
            for line1 in f1:
                if re.search(pattern, line1):
                    count_git_log += 1

        with open("/srv/bug_repo_info/pull_request/{}".format(filename), "r") as f2:
            for line2 in f2:
                if re.search(pattern, line2):
                    count_pull_request += 1

        with open("/srv/bug_repo_info/rough_issue_num.txt", "a") as fi:
            fi.write("{}\t{}\t{}\n".format(filename, count_git_log, count_pull_request))

print("ALL IS FINE!")
