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
    ret_dir = 'e:/Data/EOS/automl/edge_container'
    for f_n in os.listdir(ret_dir):
        f_p = os.path.join(ret_dir, f_n)
        from_csv_ret(f_p)

def from_csv_ret(f_p):
    with open(f_p, 'r') as _ret:
        f_n = os.path.basename(f_p)
        obs = []
        for line in _ret.readlines():
            fields = line.split(',')
            x_min, y_min, x_max, y_max = fields[1:-1]
            x_min = int(float(x_min) * 960)
            y_min = int(float(y_min) * 720)
            x_max = int(float(x_max) * 960)
            y_max = int(float(y_max) * 720)
            obs.append(OBS.format(x_min, y_min, x_max, y_max))
    with open(os.path.join('e:/Data/EOS/pred_xml', f'{f_n}.xml'), 'w') as xml:
        img_n = f'{f_n}.jpg'
        img_p = os.path.join('e:/Data/EOS/automl/test/imgs', img_n)
        xml.write(XMLBASE.format(img_n, img_p, ''.join(obs)))

if __name__ == "__main__":
    main()