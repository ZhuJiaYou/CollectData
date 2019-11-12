from repository import Repository


with open("E:\\experimentalData\\private\\repo_star500_commit2000_list2.txt", "r") as f:
    for line in f:
        repo = Repository(line.strip())
        filename = "{}_{}_{}.txt".format(repo.language, repo.owner, repo.name)
        with open("/srv/bug_repo_info/selected/merged/{}".format(filename), "w") as fw:
            fw.write("COMMIT_ID\tAUTHOR\tTIME\tISSUE_NUMBER\tI_AUTHOR\tI_TIME\tTITLE\tDESCRIPTION\n"))
        with open("/srv/bug_repo_info/selected/gl/{}".format(filename), "r") as f1:
            for line1 in f1:
                # m_id = re.match(r"^commit ((\d|\w)+)", line1)
                # m_author = re.match(r"^Author: ((\d|\w|.)+ )+", line1)
                # m_date = re.match(r"^Date:\s+((\d|\w|-|:)+)", line1)
                # m_part_message = re.match(r"^    .", line1)
                if len(line1) > 6 and line1[:6] == "commit":
                    commit.commit_message = re.sub(r"\s+", " ", commit.commit_message).strip()
                    with open("/srv/bug_repo_info/selected/glf/{}".format(filename), "a") as fw:
                        fw.write("{}\t{}\t{}\t{}\n".format(commit.commit_id, commit.commit_author, 
                                                           commit.commit_time, commit.commit_message))
#                    print(commit.commit_message)
                    commit = CommitLog()
                    commit.commit_id = line1[7:-1]
#                    print(commit.commit_id)
                elif len(line1) > 6 and line1[:6] == "Author":
                    tmp_i = line1.index("<")
                    commit.commit_author = line1[8:tmp_i-1]
 #                   commit.commit_author = re.sub(r"\s+", " ", m_author.group(1)).strip()
 #                   print(commit.commit_author)
                elif len(line1) > 4 and line1[:4] == "Date":
                    commit.commit_time = line1[8:28]
#                    print(commit.commit_time)
                elif len(line1) > 4 and line1[:4] == "    ":
                    commit.commit_message += (line1.strip() + " ")
        commit.commit_message = re.sub(r"\s+", " ", commit.commit_message).strip()
        with open("/srv/bug_repo_info/selected/glf/{}".format(filename), "a") as fw:
            fw.write("{}\t{}\t{}\t{}\n".format(commit.commit_id, commit.commit_author, 
                                               commit.commit_time, commit.commit_message))
        print("{} IS OK.".format(repo.name))

print("ALL IS FINE!")
