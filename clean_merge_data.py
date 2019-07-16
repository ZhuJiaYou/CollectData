from repository import Repository


with open("/srv/bug_repo_info/selected/selected_repos.txt", "r") as f:
    for line in f:
        repo = Repository(line.strip())
        filename = "{}_{}_{}.txt".format(repo.language, repo.owner, repo.name)
        file_data = ""
        with open("/srv/bug_repo_info/selected/merged/{}".format(filename), "r") as fr:
            for liner in fr:
                elem_list = liner.strip().split("\t")
                if elem_list[-1] == "None" and elem_list[-2] == "None":
                    continue
                file_data += liner
        with open("/srv/bug_repo_info/selected/merged_clean/{}".format(filename), "w") as fw:
            fw.write(file_data)

        print("{} IS FINE.".format(repo.name))
print("ALL IS FINE!")
