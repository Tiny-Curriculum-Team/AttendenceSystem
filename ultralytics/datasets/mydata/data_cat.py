from tqdm import tqdm
import os
import random


def check_data(root, class_num): # 查看空数据
    for (dirpath, dirnames, filenames) in os.walk(
            root):  # 使用walk函数，打开txt目录,获得一个特殊的三元组，得到当前文件路径，当前文件路径下的子文件夹名字，当前文件路径下的所有文件名字
        random.shuffle(filenames)
        filepath = [os.path.join(dirpath, filename) for filename in
                    tqdm(filenames)]  # 对当前文件路径下 所有txt的名字列表进行遍历，并获得当前txt文件的绝对路径
        for x, file in enumerate(tqdm(filepath)):
            with open(file, 'r') as f:
                lines = f.readlines()
                for line in lines:
                    if not (int(line[0]) in class_num):
                        print(x, '(error_txt):', file)


if __name__ == '__main__':
    root_path = "css-data"  # 你存放数据的文件路径
    type_data = 'test'  # 便于你更换不同类型的标注文件夹路径
    class_num = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10]  # 在这里放置你的标注文件类
    labels_dir = save_catalogue = os.path.join(root_path, type_data,
                                            "labels")  # 你放置标注文件那一堆txt的文件夹路径，如‘E:\new\txt\train\’
    check_data(labels_dir, class_num)

# data construction
# --train—— images
#       |—— labels
# --test —— images
#       |—— labels
# --valid—— images
#       |—— labels

# for root,_,labels_name in os.walk(labels_path):
