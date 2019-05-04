from git import Repo, GitCommandError
from bug_item import BugItem, generate_bug_items
import os
import shutil


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
                codes_file_name = item.commit + "{:03d}".format(i) + ".java"
                shutil.copyfile(repo_dir + f, codes_dir + codes_file_name)   

            i += 1


if __name__ == '__main__':
    repo_dir = "./../datasets/repos/eclipse.platform.ui/"
    codes_dir = "./../datasets/eclipseUI/codes/"

    filename = "./../datasets/Eclipse_Platform_UI.txt"
    items = generate_bug_items(filename)
    del items[0]
    collect_git_codes(items, repo_dir, codes_dir)
