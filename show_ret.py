import json
import re
import os


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
CATCH = re.compile(r'normalized_vertices \{.*\n.*(\d\.\d+)[\n].*(\d\.\d+)[\n].*\}')

def main():
    fn = '18.10_011--3_1'
    with open('18.10_011--3_1.json', 'r') as ret:
        content = ret.read()
    coords = []
    obs = []
    for idx, (x, y) in enumerate(CATCH.findall(content)):
        x_ = int(float(x) * 960)
        y_ = int(float(y) * 720)
        if idx != 0 and idx % 2 == 0:
            obs.append(OBS.format(*coords))
            coords = []
        coords.extend([x_, y_])
    if idx % 2 == 0:
        obs.append(OBS.format(coords))

    with open(os.path.join('e:/Data/EOS/pred_xml', f'{fn}.xml'), 'w') as xml:
        img_n = f'{fn}.jpg'
        img_p = os.path.join('e:/Data/EOS/jpgs', img_n)
        xml.write(XMLBASE.format(img_n, img_p, ''.join(obs)))

if __name__ == "__main__":
    main()