import os
import cv2
import re
import glob
import logging

NAME = re.compile(r'(?<=filename\>).*(?=\<)')
PATH = re.compile(r'(?<=path\>).*(?=\<)')

def to_jpg(img_p, dst_p):
    img = cv2.imread(img_p)
    cv2.imwrite(dst_p, img)

def path_change(xmls_dir):
    jpg_dir = 'E:/Data/EOS/jpgs'
    label_xml_dir = 'E:/Data/EOS/xml_label'
    os.makedirs(jpg_dir, exist_ok=1)
    os.makedirs(label_xml_dir, exist_ok=1)
    for name in os.listdir(xmls_dir):
        img_n = os.path.splitext(name.replace('_label', ''))[0]
        img_p = os.path.join('e:/Data/EOS/imgs', f'{img_n}.tif')
        dst_n = f'{img_n}.jpg'
        dst_p = os.path.join(jpg_dir, dst_n)
        # to_jpg(img_p, dst_p)
        with open(os.path.join(xmls_dir, name), 'r') as xml:
            xml_content = xml.read(200)
            xml_content = NAME.sub(dst_n, xml_content)
            xml_content = PATH.sub('dst_p', xml_content)
            xml_content = xml_content.replace('dst_p', dst_p)
            last = xml.read()
        with open(os.path.join(label_xml_dir, name.replace('_label', '')), 'w') as new_xml:
            new_xml.write(xml_content)
            new_xml.write(last)

def path_change2(xmls_dir):
    label_xml_dir = 'E:/Data/EOS/xml_adjust'
    os.makedirs(label_xml_dir, exist_ok=1)
    for name in os.listdir(xmls_dir):
        img_n = os.path.splitext(name)[0]
        img_pl = glob.glob(f"e:/Data/EOS/labels/**/{img_n}*", recursive=True)
        
        try:
            img_p = img_pl[0]
        except ImportError:
            logging.exception(f'{name} loss')
        else:
            dst_n = os.path.basename(img_p)
            with open(os.path.join(xmls_dir, name), 'r') as xml:
                xml_content = xml.read(200)
                xml_content = NAME.sub(dst_n, xml_content)
                xml_content = PATH.sub('dst_p', xml_content)
                xml_content = xml_content.replace('dst_p', img_p)
                last = xml.read()
            with open(os.path.join(label_xml_dir, f'{os.path.splitext(dst_n)[0]}.xml') ,
                    'w') as new_xml:
                new_xml.write(xml_content)
                new_xml.write(last)
    
if __name__ == "__main__":
    path_change2('e:/Data/EOS/xml_label')
    