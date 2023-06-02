import cv2 as cv
import os
from PIL import Image
from pykeyboard import *
# you need install : pykeyboard pywin32 PyUserInput

def read_check(data_path, count_txt, color):
    images_list = []
    for rootpath, _, filename in os.walk(os.path.join(data_path, "images")):
        for name in filename:
            images_list.append(os.path.join(rootpath, name))
    len_origin = len(images_list)
    try:
        with open(count_txt, 'r') as f:
            count_data = int(f.read())
    except:
        with open(count_txt, 'w') as f:
            f.write("0")
        count_data = 0
    key = 0
    while key != -1:
        print(f"{count_data}.img:{images_list[count_data]}")
        img = cv.imread(images_list[count_data])
        cv.imshow('picture', img)
        key = cv.waitKey(0)
        if key == 107 or key == 75:  # k or K (kill)
            os.remove(images_list[count_data])
            os.remove(images_list[count_data].replace('images', 'labels').removesuffix(".jpg") + ".txt")
            images_list.pop(count_data)
            print(f"Kill {count_data}.img:{images_list[count_data]}")
            cv.destroyAllWindows()
        elif key == 110 or key == 78:  # n or N (next)
            cv.destroyAllWindows()
            count_data += 1
        elif key == 112 or key == 80:  # p or P (pass)
            cv.destroyAllWindows()
            count_data -= 1
        elif key == 115 or key == 83:  # s or S (stop)
            with open(count_txt, 'w') as f:
                f.write(str(count_data))
            cv.destroyAllWindows()
            print('Stop in:', count_data)
            print('Start list', len_origin)
            print('End list', len(images_list))
            exit()
        elif key == 119 or key == 87:  # w or W (write)
            img_size = Image.open(images_list[count_data])
            width, high = img_size.size
            with open(images_list[count_data].replace('images', 'labels').removesuffix(".jpg") + ".txt", 'r') as t:
                txt = t.readlines()
                image = cv.imread(images_list[count_data])
            for i in txt:
                i = i.strip().split(" ")
                cv.rectangle(image,
                             (
                             int((float(i[1]) - float(i[3]) / 2) * width), int((float(i[2]) - float(i[4]) / 2) * high)),
                             (
                             int((float(i[1]) + float(i[3]) / 2) * width), int((float(i[2]) + float(i[4]) / 2) * high)),
                             color[i[0]], 1)
            cv.imshow('picture_frame', image)
            k = PyKeyboard()
            k.tap_key('C')
            cv.waitKey(0)


if __name__ == '__main__':
    type_data = 'train'
    data_path = "./css-data/%s" % type_data
    count_txt = './css-data/count_txt/count_%s.txt' % type_data  # 计数文本
    color = {'0': (255, 0, 0), '1': (255, 140, 0), '2': (50, 205, 50), '3': (0, 0, 255), '4': (148, 0, 211),
             '5': (225, 225, 0), '6': (106, 90, 205), '7': (204, 120, 50), "8": (13, 85, 158), "9": (255, 207, 73)}
    read_check(data_path, count_txt, color)
