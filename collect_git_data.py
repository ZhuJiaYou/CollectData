from git import Repo, GitCommandError
from bug_item import BugItem, generate_bug_items
import os
import shutil
from random import sample


def collect_git_codes(items, repo_dir, codes_dir):
    repo = Repo(repo_dir)
    git = repo.git

    for item in items:
        i = 0
        for f in item.jfiles:
            if not f.endswith("java"):
                continue

            try:
                git.checkout(item.commit + "~1", f)  # 文件回退至bug修复补丁的上一个commit
            except GitCommandError:
                print(item.commit + "~1" + " " + f + " Not Exists!")

            if not os.path.exists(repo_dir + f):
                try:
                    git.checkout(item.commit, f)
                except GitCommandError:
                    print(item.commit + " " + f + " Not Exists!")

                if not os.path.exists(repo_dir + f):
                    print(item.bug_id + " " + item.commit + " " + f)

            if os.path.exists(repo_dir + f):
                codes_file_name = item.commit + "{:03d}".format(i + 500) + ".java"
                shutil.copyfile(repo_dir + f, codes_dir + codes_file_name)   

            i += 1


def collect_nobug_codes(items, repo_dir, codes_dir):
    bug_files = set()
    nobug_files = set()
    for item in items:
        for f in item.jfiles:
            if not f.endswith("java"):
                continue

            bug_files.add(f)

    for dirpath, dirnames, filenames in os.walk(repo_dir):
        for filename in filenames:
            fullname = os.path.join(dirpath, filename)
            name = fullname[len(repo_dir):]
            if name.endswith("java") and (name not in bug_files):
                nobug_files.add(name)

    for item in items:
        random_files = sample(nobug_files, 5)
        i = 0
        for random_file in random_files:
            if os.path.exists(repo_dir + random_file):
                codes_file_name = item.commit + "{:03d}".format(i) + ".java"
                shutil.copyfile(repo_dir + random_file, codes_dir + codes_file_name)
            i += 1


def collect_description_summary(items, repo_dir, codes_dir):
    for item in items:
        i = 0
        for filename in item.jfiles:
            filename0 = item.commit + "{:03d}".format(i + 500)
            codes_filename = filename0 + ".java"
            if os.path.exists(os.path.join(codes_dir + codes_filename)):
                description_filename = filename0 + ".description"
                with open(os.path.join(codes_dir, description_filename), "a") as file_obj:
                    file_obj.write(item.summary + " " + item.description)
            i += 1

        for i in range(0, 5):
            filename0 = item.commit + "{:03d}".format(i)
            codes_filename = filename0 + ".java"
            if os.path.exists(os.path.join(codes_dir + codes_filename)):
                description_filename = filename0 + ".description"
                with open(os.path.join(codes_dir, description_filename), "a") as file_obj:
                    file_obj.write(item.summary + " " + item.description)


def check_files(codes_dir):
    for filename in os.listdir(codes_dir):
        filename0 = filename.split(".")[0]
        if os.path.exists(os.path.join(codes_dir, filename0 + ".java")) and \
        os.path.exists(os.path.join(codes_dir, filename0 + ".description")):
            continue
        else:
            print(filename)
            return

    print("All Is Fine!!")


if __name__ == '__main__':
    repo_dir = "./../datasets/repos/org.aspectj/"
    codes_dir = "./../datasets/AspectJ/codes/"

    filename = "./../datasets/AspectJ.txt"
#    items = generate_bug_items(filename)
#    del items[0]
#    collect_git_codes(items, repo_dir, codes_dir)
#    collect_nobug_codes(items, repo_dir, codes_dir)
#    collect_description_summary(items, repo_dir, codes_dir)
    check_files(codes_dir)
