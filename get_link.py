import re
from collections import Counter
from repository import Repository
from git_log import CommitLog
from pull_request import PullRequest


def get_pull_request_commit_type():
    with open("/srv/bug_repo_info/selected/selected_repos.txt", "r") as f:
        for line in f:
            repo = Repository(line)
        # pattern = r"\bfix(s|es|d|ed)?\s*(#|issue|issues)?\s*\d+"
            filename = "{}_{}_{}.txt".format(repo.language, repo.owner, repo.name)

        # with open("/srv/bug_repo_info/selected/glf/{}".format(filename), "r") as f1:
        #    for line1 in f1:
        #        if re.search(pattern, line1):
        #            count_git_log += 1

            with open("/srv/bug_repo_info/selected/pr/{}".format(filename), "r") as f2:
                for line2 in f2:
                    if line2[:6] == "NUMBER":
                        continue
                    pr = PullRequest(line2)
                    if pr.merge_commit != "None" and len(pr.merge_commit) != 7:
                        print("WHY?? WHY?? WHY??")
                        print(line2)
                        print(line)

        # with open("/srv/bug_repo_info/rough_issue_num.txt", "a") as fi:
        #     fi.write("{}\t{}\t{}\n".format(filename, count_git_log, count_pull_request))


def state_pull_request_commit_info():
    gl_repeat = ['a186334', 'ebe3255', '113ab74', 'ddfa04e', '1619722', '8a4a39d', 'c3f3137', '48d7842', 'f61d434', '1eacab0', '66943ee', 'cd77ea3', 'f9b56a5', '48128ec', '4fc4030', '88acb48']
    with open("/srv/bug_repo_info/selected/selected_repos.txt", "r") as f:
        for line in f:
            repo = Repository(line)
            filename = "{}_{}_{}.txt".format(repo.language, repo.owner, repo.name)
            gl_commits = []
            gls = []
            gl_is_commits = []
            pr_commits = []
            pr_is_commits = []
            count_gl_fix_is = 0
            count_pr_fix_is = 0
            pattern = r"\bfix(s|es|d|ed)?\s+(#|issue|issues)?\s*(\d+)"
            
            with open("/srv/bug_repo_info/selected/linked/{}".format(filename), "w") as fl:
                fl.write("COMMIT_ID\tCOMMIT_TIME\tCOMMIT_AUTHOR\tISSUE_NUMBER\n")

            with open("/srv/bug_repo_info/selected/glf/{}".format(filename), "r") as f1:
                for line1 in f1:
                    if line1[:9] == "COMMIT_ID":
                        continue
                    gl = CommitLog(line1)
                    m = re.search(pattern, gl.commit_message)
                    if m:
                        gl_is_commits.append(gl.commit_id[:7])
                        with open("/srv/bug_repo_info/selected/linked/{}".format(filename), "a") as fl:
                            fl.write("{}\t{}\t{}\t{}\n".format(gl.commit_id, gl.commit_time,
                                                               gl.commit_author, m.group(3)))
                    gl_commits.append(gl.commit_id[:7])
                    gls.append(gl)

            with open("/srv/bug_repo_info/selected/pr/{}".format(filename), "r") as f2:
                for line2 in f2:
                    if line2[:6] == "NUMBER":
                        continue
                    pr = PullRequest(line2)
                    m = re.search(pattern, pr.title + " " + pr.description + " " + pr.first_comment)
                    if m:
                        if (pr.merge_commit not in gl_is_commits) and (pr.merge_commit in gl_commits):
                            pr_is_commits.append(pr.merge_commit)
                            i = gl_commits.index(pr.merge_commit)
                            with open("/srv/bug_repo_info/selected/linked/{}".format(filename), "a") as fl:
                                fl.write("{}\t{}\t{}\t{}\n".format(gls[i].commit_id, gls[i].commit_time,
                                                                   gls[i].commit_author, m.group(3)))

            # print(len(pr_is_commits) + len(gl_is_commits))
            # print(line)
            # print("*********************************")
            # print(gl_commits[-1])
            # print(gls[-1].commit_id)
            # print("*********************************")
            # counter = Counter(gl_commits)
            # for i, j in zip(counter.values(), counter.keys()):
            #     if i != 1:
            #         print("WWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWW")
            #         gl_repeat.append(j)
            #         print(j)
    print(gl_repeat)



    # i = 0 
    # for commit in pr_commits:
        # if commit not in gl_commits:
            # i += 1
    #        print("WHY WHY WHY ??")
    #        print(commit)
    #        print(line)
    #        print()
    # print(i)

            # print(gl_commits[:5])
            # print(pr_commits[:5])

        # with open("/srv/bug_repo_info/rough_issue_num.txt", "a") as fi:
        #     fi.write("{}\t{}\t{}\n".format(filename, count_git_log, count_pull_request))



if __name__ == '__main__':
    # get_pull_request_commit_type()
    state_pull_request_commit_info()
