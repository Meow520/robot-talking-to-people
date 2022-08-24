import argparse
import time
from collections import deque
from threading import Thread, Lock
import cv2
from pymongo import MongoClient
from yolo3.utils.common import setup, track, draw_rect_on_frame


def main(args):
    # GPU or CPU
    device = 'cuda:0' if args.gpu else 'cpu'

    # MongoDB
    client = MongoClient(args.db_host, args.db_port)
    db = client[args.db_name]
    collection = db[args.db_collection_name]

    # Variables
    running = False
    lock = Lock()
    stack = deque()
    cap = cv2.VideoCapture(args.src)

    # Function executed by another thread
    def read():
        """ 画像を読み込み、スタックに追加する """
        running = True
        while running:
            _, frame = cap.read()
            with lock:
                stack.append(frame)

    Thread(target=read, daemon=True).start()

    # Recognition by Yolo
    model, classes, colors, tracker = setup(
        model_path='config/yolov3.cfg', 
        model_img_size=(640, 480),
        weights_path='weights/yolov3.weights',
        device=device,
        classes_path='config/coco.names',
        deepsort_weight_path='weights/ckpt.t7'
    )
    class_mask = [0, 2, 4]
    fps = 0
    skip_frames = 0
    try:
        while True:
            # スタックの一番上のデータを取得、その他を廃棄
            with lock:
                if len(stack) == 0: continue
                frame = stack.pop()
                skip_frames = len(stack)
                stack.clear()

            t_start = time.time()
            # 認識
            if frame is None: break
            detections = track(frame, model, classes, class_mask, tracker)
            # 認識結果を映像に反映
            if detections is None:
                image = frame
            else:
                image = draw_rect_on_frame(frame, detections, classes, colors)
            cv2.putText(image, text=f'FPS: {fps}', org=(3,15), fontFace=cv2.FONT_HERSHEY_SIMPLEX,
                        fontScale=0.6, color=(255, 0, 0), thickness=2)
            cv2.imshow("image", image)
            if cv2.waitKey(1) & 0xFF == ord("q"):
                raise KeyboardInterrupt
            # 認識結果を自然数値化
            results = [dict(x1=int(d[0]), y1=int(d[1]), x2=int(d[2]), y2=int(d[3]), id=str(int(d[4]))) for d in detections] if detections is not None and len(detections) > 0 else []
            # FPS計算
            t_end = time.time()
            proc_time = t_end - t_start
            fps = round(1.0 / proc_time, 2)
            skip_frames = int(30 * proc_time)
            print(f'Processing time = {proc_time}, fps = {fps}, Skip frames = {skip_frames}')

            # 認識結果をデータベースに挿入
            data = dict(timestamp=t_start, results=results)
            print(data)
            # collection.insert_one(data)

    except KeyboardInterrupt:
        pass

    running = False
    if cap is not None: cap.release()
    cv2.destroyAllWindows()


if __name__ == '__main__':
    parse = argparse.ArgumentParser()
    parse.add_argument('--gpu', action='store_true')
    parse.add_argument('--src', default='udp://127.0.0.1:5000', type=str)
    parse.add_argument('--db_host', default='mongo', type=str)
    parse.add_argument('--db_port', default=27017, type=int)
    parse.add_argument('--db_name', default='robot_talking_to_people', type=str)
    parse.add_argument('--db_collection_name', default='human_recognition', type=str)
    args = parse.parse_args()
    main(args)
