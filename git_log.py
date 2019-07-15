class CommitLog:
    def __init__(self, line):
        elem_list = line.split("\t")
        self.commit_id = elem_list[0]
        self.commit_time = elem_list[2]
        self.commit_author = elem_list[1]
        self.commit_message = elem_list[3]
