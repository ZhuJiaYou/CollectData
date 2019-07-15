class PullRequest:
    def __init__(self, line):
        elem_list = line.split("\t")
        self.number = elem_list[0]
        self.title = elem_list[1]
        self.author = elem_list[2]
        self.create_time = elem_list[3]
        self.merge_commit = elem_list[4]
        self.description = elem_list[5]
        self.first_comment_author = elem_list[6]
        self.first_comment_time = elem_list[7]
        self.first_comment = elem_list[8]
