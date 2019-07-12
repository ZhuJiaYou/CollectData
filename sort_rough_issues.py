repo_fix_issue = []


with open("/srv/bug_repo_info/rough_issue_num.txt", "r") as f:
    for line in f:
        if line[:4] != "REPO":
            info_list = line.split("\t")
            repo_fix_issue.append((info_list[0], int(info_list[1]), int(info_list[2])))

repo_fix_issue = sorted(repo_fix_issue, key=lambda d: d[1] + d[2], reverse=True)

with open("/srv/bug_repo_info/rough_issue_num_sorted.txt", "w") as fi:
    fi.write("REPO\tGIT_LOG\tPULL_REQUEST\n")
    for data in repo_fix_issue:
        print(data)
        fi.write("{}\t{}\t{}\n".format(data[0], data[1], data[2]))
