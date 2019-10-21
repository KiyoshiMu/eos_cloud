
import sys
import os
import glob
from google.cloud import automl_v1beta1
from google.cloud.automl_v1beta1.proto import service_pb2
# 'content' is base-64-encoded image data.
def get_prediction(content):
    project_id, model_id = '887184105897', 'IOD5084392455487356928'
    prediction_client = automl_v1beta1.PredictionServiceClient()
    name = 'projects/{}/locations/us-central1/models/{}'.format(project_id, model_id)
    payload = {'image': {'image_bytes': content }}
    params = {}
    request = prediction_client.predict(name, payload, params)
    return request    # waits till request is returned
def main():
    img_dir = sys.argv[1]
    dst = sys.argv[2]
    os.makedirs(dst, exist_ok=True)
    for f_p in glob.glob('{}/**/*.jpg'.format(img_dir), recursive=True):
        with open(f_p, 'rb') as ff:
            content = ff.read()
            response = get_prediction(content)
        with open(os.path.join(dst, os.path.splitext(os.path.basename(f_p))[0]),
                              'w') as ret:
            for idx, result in enumerate(response.payload):
                ret.write('{},'.format(idx))
                ret.write(response_csv(result))
                ret.write('\n')
            # break

def response_csv(result):
    box = result.image_object_detection.bounding_box
    return ','.join(str(v) for v in (box.normalized_vertices[0].x, 
                    box.normalized_vertices[0].y, 
                    box.normalized_vertices[1].x, 
                    box.normalized_vertices[1].y, 
                    result.image_object_detection.score))

if __name__ == '__main__':
    file_path = sys.argv[1]
    # project_id = sys.argv[2]
    # model_id = sys.argv[3]
    main()