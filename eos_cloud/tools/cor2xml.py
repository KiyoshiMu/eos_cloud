import json
import os
import argparse
from eos_cloud.tools import Metadata

def main(argv=None):
    XMLBASE = Metadata.XMLBASE
    OBS = Metadata.OBS
    parser = argparse.ArgumentParser()
    parser.add_argument('--input')
    parser.add_argument('--output')
    options = parser.parse_args(argv)
    os.makedirs(options.output, exist_ok=1)
    with open(options.input) as ret_json:
        raw_info = json.load(ret_json)
    for name, item in raw_info.items():
        boxs = item['boxs']
        # path = item['img_p']
        path = item['label_p'] # convenient for validation
        obs = '\n'.join(OBS.format(box['x_min'], box['y_min'], box['x_max'], box['y_max'])
                for box in boxs.values())
        # f_n = os.path.basename(path)
        xml_content = XMLBASE.format(name, path, 1920, 1440, obs)
        with open(os.path.join(options.output,
                f'{name}_label.xml'),
                 'w') as xml_:
            xml_.write(xml_content)

if __name__ == "__main__":
    main()