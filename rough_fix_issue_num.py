import re
from repository import Repository


with open("E:\\experimentalData\\private\\rough_issue_num.txt", "w", encoding="utf8") as fi:
    fi.write("REPO\tGIT_LOG\tPULL_REQUEST\n")

with open("E:\\experimentalData\\private\\repo_star500_commit2000_list2.txt", "r", encoding="utf8") as f:
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

        with open("E:\\experimentalData\\private\\gitLogs\\{}".format(filename), "r", encoding="utf8") as f1:
            for line1 in f1:
                if re.search(pattern, line1):
                    count_git_log += 1

        with open("E:\\experimentalData\\private\\pullRequests\\{}".format(filename), "r", encoding="utf8") as f2:
            for line2 in f2:
                if re.search(pattern, line2):
                    count_pull_request += 1

        with open("E:\\experimentalData\\private\\rough_issue_num.txt", "a", encoding="utf8") as fi:
            fi.write("{}\t{}\t{}\n".format(filename, count_git_log, count_pull_request))

print("ALL IS FINE!")
