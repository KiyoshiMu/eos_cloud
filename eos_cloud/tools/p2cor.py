import os
import argparse
import random
from collections import defaultdict
import json
import logging

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

def _from_label(label_img_p):
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

def _cal_box(point, length=22):
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
    return x_min, y_min, x_max, y_max

def _draw_box(img, x_min, y_min, x_max, y_max):
    use_color = (0, 255, 0)
    cv2.rectangle(img, (x_min, y_min), 
                (x_max, y_max), use_color, 2)
    
def path_list(img_dir) -> list:
    img_p_list = [os.path.join(item[0], f_p) for item in os.walk(img_dir) for f_p in item[2] if item[2]]
    return img_p_list

def _get_name(p):
    return os.path.splitext(os.path.basename(p))[0].replace('_label', '')

def _path_matcher(img_dir, label_dir):
    img_path_list = path_list(img_dir)
    label_path_list = path_list(label_dir)
    label_path_dict = dict([(_get_name(p), p) for p in label_path_list])
    for img_path in img_path_list:
        name = _get_name(img_path)
        label_path = label_path_dict.get(name)
        if label_path:
            yield img_path, label_path, name
        else:
            logging.warning('%s does not match any lable', img_path)

def main(argv=None, show_draw=False):
    parser = argparse.ArgumentParser()
    parser.add_argument('--img_dir', default='e:/Data/EOS/imgs')
    parser.add_argument('--label_dir', default='e:/Data/EOS/nor_labels')
    parser.add_argument('--dst', default='e:/Data/dst')
    options = parser.parse_args(argv)
    img_dir = options.img_dir
    label_dir = options.label_dir
    dst = options.dst
    os.makedirs(dst, exist_ok=1)
    # count = 0
    ret = defaultdict(dict)
    for img_p, label_p, name in _path_matcher(img_dir, label_dir):

        img = cv2.imread(img_p)
        points = _from_label(label_p)
        temp = {}
        for idx, point in enumerate(points):
            x_min, y_min, x_max, y_max = _cal_box(point, 22)
            temp[idx] = dict(zip(('x_min', 'y_min', 'x_max', 'y_max'), 
                                 (x_min, y_min, x_max, y_max)))
            if show_draw:
                _draw_box(img, x_min, y_min, x_max, y_max)
        ret[name]['boxs'] = temp
        ret[name]['img_p'] = img_p
        ret[name]['label_p'] = label_p
        if show_draw:
            cv2.imwrite(os.path.join(dst, f'{name}.png'), img)

    with open(os.path.join(dst, 'points.json'), 'w') as ponitj:
        json.dump(ret, ponitj)

if __name__ == "__main__":
    main()
