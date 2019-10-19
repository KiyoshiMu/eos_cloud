import os
import argparse
import random
from collections import defaultdict
import json

import numpy as np
import cv2

random.seed(42)

def _middle(cnt):
    M = cv2.moments(cnt)
    if M['m00'] == 0:
        return (0, 0)
    cx = int(M['m10']/M['m00'])
    cy = int(M['m01']/M['m00'])
    return (cx, cy)

def from_label(label_img_p):
    """Read one labeled image, and save the interested location.
    label_img_p (str), the path of a labeled image."""
    frame = cv2.imread(label_img_p)
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    lower_green = np.array([50,100, 50])
    upper_green = np.array([70,255, 255])
    mask = cv2.inRange(hsv, lower_green, upper_green)
    # res = cv2.bitwise_and(frame,frame, mask= mask)
    cnts = cv2.findContours(mask, cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)[-2]
    points = [_middle(cnt) for cnt in cnts]
    return points

def draw_box(img, point, length=22):
    use_color = (0, 255, 0)
    x_length = random.randint(length-2, length+2)
    y_length = random.randint(length-2, length+2)
    x_random = random.randint(-2, 2)
    y_random = random.randint(-2, 2)
    x, y = point
    x += x_random
    y += y_random
    x_min = x - x_length
    y_min = y - y_length
    x_max = x + x_length
    y_max = y + y_length
    cv2.rectangle(img, (x_min, y_min), 
                (x_max, y_max), use_color, 2)
    return dict(zip(('x_min', 'y_min', 'x_max', 'y_max'), (x_min, y_min, x_max, y_max)))

def path_list(img_dir) -> list:
    img_p_list = [os.path.join(item[0], f_p) for item in os.walk(img_dir) for f_p in item[2] if item[2]]
    return img_p_list

def get_name(p):
    return os.path.splitext(os.path.basename(p))[0].replace('_label', '')

def path_matcher(img_dir, label_dir):
    img_path_list = path_list(img_dir)
    label_path_list = path_list(label_dir)
    label_path_dict = dict([(get_name(p), p) for p in label_path_list])
    for img_path in img_path_list:
        name = get_name(img_path)
        label_path = label_path_dict.get(name)
        if label_path:
            yield img_path, label_path, name
        else:
            print(img_path)

def main(write=False):
    parse = argparse.ArgumentParser()
    parse.add_argument('--img_dir', default='e:/Data/EOS/imgs')
    parse.add_argument('--label_dir', default='e:/Data/EOS/nor_labels')
    parse.add_argument('--dst', default='e:/Data/dst')
    cmds = parse.parse_args()
    img_dir = cmds.img_dir
    label_dir = cmds.label_dir
    dst = cmds.dst
    # count = 0
    ret = defaultdict(dict)
    for img_p, label_p, name in path_matcher(img_dir, label_dir):

        img = cv2.imread(img_p)
        points = from_label(label_p)
        temp = {}
        for idx, point in enumerate(points):
            temp[idx] = draw_box(img, point)
        ret[name]['boxs'] = temp
        ret[name]['img_p'] = img_p
        ret[name]['label_p'] = label_p
        if write:
            cv2.imwrite(os.path.join(dst, f'{name}.png'), img)

    with open('rets.json', 'w') as ret_json:
        json.dump(ret, ret_json)

if __name__ == "__main__":
    main()
