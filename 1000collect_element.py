import os


def collect_id_label(dir_, dest):
    ids = []
    labels = []
    data = []

    for filename in os.listdir(dir_):    
        id_ = filename.split(".")[0]
        if filename.endswith("java"):
            ids.append(id_)
            if int(id_[-3:]) >= 500:
                labels.append("True")
            else:
                labels.append("False")

    for i, l in zip(ids, labels):
        print(i, l)
        data.append(i + "\t" + l)
    print(len(data))

    with open(dest, "a") as file_obj:
        for line in data:
            file_obj.write(line)
            file_obj.write("\n")


if __name__ == '__main__':
    dir_ = "./../datasets/AspectJ/codes"
    dest = "./../datasets/AspectJ/AspectJ_ids_labels.txt"
    collect_id_label(dir_, dest)
