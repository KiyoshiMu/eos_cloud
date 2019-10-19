import cv2
import os
from collections import defaultdict
import xml.etree.ElementTree as ET

XMLBASE = """\
<annotation>
	<folder>labels</folder>
	<filename>{}</filename>
	<path>{}</path>
	<source>
		<database>Unknown</database>
	</source>
	<size>
		<width>960</width>
		<height>720</height>
		<depth>3</depth>
	</size>
	<segmented>0</segmented>
    {}
</annotation>
"""

OBS = """\
    <object>
		<name>eos</name>
		<pose>Unspecified</pose>
		<truncated>0</truncated>
		<difficult>0</difficult>
		<bndbox>
			<xmin>{}</xmin>
			<ymin>{}</ymin>
			<xmax>{}</xmax>
			<ymax>{}</ymax>
		</bndbox>
	</object>
"""

def get_dst_img_n(img_p, num):
    return f'{os.path.splitext(os.path.basename(img_p))[0]}_{num}.jpg'
def get_dst_img_p(img_p, dst, num):
    return os.path.join(dst, get_dst_img_n(img_p, num))

def crop_img(img_p, dst):
    img = cv2.imread(img_p)
    cv2.imwrite(get_dst_img_p(img_p, dst, 0), img[:720, :960])
    cv2.imwrite(get_dst_img_p(img_p, dst, 1), img[:720, 960:])
    cv2.imwrite(get_dst_img_p(img_p, dst, 2), img[720:, :960])
    cv2.imwrite(get_dst_img_p(img_p, dst, 3), img[720:, 960:])

def crop_xml(xml_dir, img_dst, xml_dst):
    for f_n in os.listdir(xml_dir):
        img_n = f"{os.path.splitext(f_n.replace('_label', ''))[0]}.jpg"
        img_p = os.path.join('e:/Data/EOS/jpgs', img_n)
        crop_img(img_p, img_dst)

        xml_file = os.path.join(xml_dir, f_n)
        tree = ET.parse(xml_file)
        root = tree.getroot()
        xml_content = defaultdict(list)
        for member in root.findall('object'):
            bbx = member.find('bndbox')
            xmin = int(bbx.find('xmin').text)
            ymin = int(bbx.find('ymin').text)
            xmax = int(bbx.find('xmax').text)
            ymax = int(bbx.find('ymax').text)
            if xmin >= 940: # 20 pixle as boundary pad
                xmin -= 960
                xmax -= 960
                if ymin >= 700:
                    ymin -= 720
                    ymax -= 720
                    crop_fn = f'{os.path.splitext(img_n)[0]}_3'
                else:
                    crop_fn = f'{os.path.splitext(img_n)[0]}_1'
            else:
                if ymin >= 700:
                    ymin -= 720
                    ymax -= 720
                    crop_fn = f'{os.path.splitext(img_n)[0]}_2'
                else:
                    crop_fn = f'{os.path.splitext(img_n)[0]}_0'
            
            xml_content[crop_fn].append(OBS.format(xmin, ymin, xmax, ymax))

        for crop_fn, v in xml_content.items():
            path = os.path.join(img_dst, f'{crop_fn}.jpg')
            _xml_n = f'{crop_fn}.xml'
            with open(os.path.join(xml_dst, _xml_n), 'w') as _xml:
                _xml.write(XMLBASE.format(f'{crop_fn}.jpg', path, ''.join(v)))

def main():
    crop_xml('e:/Data/EOS/xml_adjust', 'e:/Data/EOS/tmp', 'e:/Data/EOS/tmp_xml')

if __name__ == "__main__":
    main()