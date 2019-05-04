class BugItem:
    def __init__(self, item_str):
        if item_str.strip() == "":
            print("Error string!")
            return

        contents = item_str.split("\t")
        if len(contents) < 11:
            print("Error item string!")
            return

        self.i = contents[0]
        self.bug_id = contents[1]
        self.summary = contents[2]
        self.description = contents[3]
        self.report_time = contents[4]
        self.report_times = contents[5]
        self.status = contents[6]
        self.commit = contents[7]
        self.commit_time = [8]
        
        files = contents[9].split(".java ")
        self.jfiles = []
        for f in files:
            if not f.endswith("java"):
                self.jfiles.append(f + ".java")
            else:
                self.jfiles.append(f)

        pos = contents[10].strip().split(".java ")
        self.jpos = []
        for p in pos:
            if not p.endswith("java"):
                self.jpos.append(p + ".java")
            else:
                self.jpos.append(p)

    
def generate_bug_items(filename):
    if filename.strip() == "":
        return None

    items = []
    with open(filename) as file_obj:
        for line in file_obj:
            items.append(BugItem(line))

    return items


if __name__ == '__main__':
    filename = "./../datasets/test.txt"
    items = generate_bug_items(filename)

    print(items[1].bug_id)
    for f in items[1].jfiles:
        print(f)

    for p in items[1].jpos:
        print(p)
    print(items[1].summary)
    print(items[1].description)
    print(items[1].commit)
