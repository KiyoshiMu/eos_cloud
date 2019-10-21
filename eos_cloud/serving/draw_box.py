import cv2
import json
import os

def get_respond(f_p):
    with open(f_p, 'r') as ret_:
        temp = ret_.read().replace("\'", "\"")
        content = json.loads(temp)
        scores = [item[1]
                for item in content['predictions'][0]['detection_multiclass_scores']]
        # print(scores)
        boxes = [item for item in content['predictions'][0]['detection_boxes']]
        f_n = os.path.basename(f_p)
        return f_n, scores, boxes

def drawing(f_n, scores, boxes, dst='e:/Data/EOS/automl/pred_imgs'):
    os.makedirs(dst, exist_ok=True)
    w = 960
    h = 720
    pad = 100
    img = cv2.imread(os.path.join('e:/Data/EOS/automl/test/imgs', 
                    f'{f_n}.jpg'))
    count = 0
    score_min = 1
    score_max = 0
    min_cor = (0, 0)
    max_cor = (0, 0)
    for score, box in zip(scores, boxes):
        if score < 0.3:
            continue
        y_min, x_min, y_max, x_max = box
        x_min = int(x_min * w)
        y_min = int(y_min * h)
        x_max = int(x_max * w)
        y_max = int(y_max * h)
        cv2.rectangle(img, (x_min, y_min), (x_max, y_max), (255,0,0), 2)
        count += 1
        if score < score_min:
            score_min = score
            min_cor = (x_min, y_min)
        if score > score_max:
            score_max = score
            max_cor = (x_min, y_min)
    
    cv2.putText(img, f'{score_min:.3f}', min_cor, cv2.FONT_HERSHEY_SIMPLEX,  
                0.7, (255,0,0), 1, cv2.LINE_AA)
    cv2.putText(img, f'{score_max:.3f}', max_cor, cv2.FONT_HERSHEY_SIMPLEX,  
                0.7, (255,0,0), 1, cv2.LINE_AA)
    cv2.putText(img, str(count), (w-pad, h-pad), cv2.FONT_HERSHEY_SIMPLEX,  
                1.5, (255,0,0), 2, cv2.LINE_AA) 
    cv2.imwrite(os.path.join(dst, f'{f_n}.jpg'), img)

def main(dir_p):
    for f_n in os.listdir(dir_p):
        f_p = os.path.join(dir_p, f_n)
        f_n, scores, boxes = get_respond(f_p)
        drawing(f_n, scores, boxes)

if __name__ == "__main__":
    dir_p = 'e:/Data/EOS/automl/ret_container'
    main(dir_p)
