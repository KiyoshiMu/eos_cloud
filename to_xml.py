import json
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
		<width>1920</width>
		<height>1440</height>
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

def main():
    with open('rets.json') as ret_json:
        raw_info = json.load(ret_json)
    for item in raw_info.values():
        boxs = item['boxs']
        # path = item['img_p']
        path = item['label_p']
        obs = '\n'.join(OBS.format(box['x_min'], box['y_min'], box['x_max'], box['y_max'])
                for box in boxs.values())
        f_n = os.path.basename(path)
        xml_content = XMLBASE.format(f_n, path, obs)
        with open(os.path.join('e:/Data/EOS/xmls/', f'{os.path.splitext(f_n)[0]}.xml'),
                 'w') as xml_:
            xml_.write(xml_content)

if __name__ == "__main__":
    main()