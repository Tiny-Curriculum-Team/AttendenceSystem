from tqdm import tqdm
import os
import random
import shutil
import glob


def check_data(dir, class_num):
    labels_dir = os.path.join(dir, "labels")
    path_list = []
    for (dirpath, dirnames, filenames) in os.walk(
            labels_dir):  # 使用walk函数，打开txt目录,获得一个特殊的三元组，得到当前文件路径，当前文件路径下的子文件夹名字，当前文件路径下的所有文件名字
        random.shuffle(filenames)
        filepath = [os.path.join(dirpath, filename) for filename in
                    tqdm(filenames)]  # 对当前文件路径下 所有txt的名字列表进行遍历，并获得当前txt文件的绝对路径
        for file in tqdm(filepath):
            with open(file, 'r') as f:
                lines = f.readlines()
                for line in lines:
                    if int(line[0]) in class_num:
                        path = file.removesuffix('.txt')
                        if path not in path_list:
                            path_list.append(path)
    for path in path_list:
        shutil.copy(glob.glob(path.replace('labels', 'images') + ".*")[0],
                    os.path.join(dir, "person"))


if __name__ == '__main__':
    root_path = "./css-data"  # 你存放数据的文件路径
    type_data = 'test'  # 便于你更换不同类型的标注文件夹路径
    class_num = [5]  # 在这里放置你需要获取的的标注文件类

    dir = os.path.join(root_path, type_data)
    check_data(dir, class_num)

# data construction
# --train—— images
#       |—— labels
# --test —— images
#       |—— labels
# --valid—— images
#       |—— labels

# for root,_,labels_name in os.walk(labels_path):
