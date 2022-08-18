import cv2
import time
from collections import deque
from pymongo.collection import Collection
from threading import Thread, Lock
from yolo3.utils.common import setup, track, draw_rect_on_frame


class HumanRecognizer:
    def __init__(self, src:str, device:str, collection:Collection):
        self.__running = False
        self.__lock = Lock()
        self.__stack = deque()
        self.__cap = cv2.VideoCapture(src)
        self.__model, self.__classes, self.__colors, self.__tracker = setup(
            model_path='config/yolov3.cfg', 
            model_img_size=(640, 480),
            weights_path='weights/yolov3.weights',
            device=device,
            classes_path='config/coco.names',
            deepsort_weight_path='weights/ckpt.t7'
        )
        self.__collection = collection

    def start(self):
        """ 画像認識を開始する（実行するスレッドはブロッキングされる） """
        Thread(target=self.__read, daemon=True).start()
        self.__recg()

    def __read(self):
        """ 画像を読み込み、スタックに追加する """
        self.__running = True
        while self.__running:
            _, frame = self.__cap.read()
            with self.__lock:
                self.__stack.append(frame)

    def __recg(self):
        """ スタックから最新の画像を取得し、人物認識し、その結果をAMQにパブリッシュする """
        class_mask = [0, 2, 4]
        fps = 0
        skip_frames = 0
        try:
            while True:
                with self.__lock:
                    if len(self.__stack) == 0: continue
                    frame = self.__stack.pop()
                    skip_frames = len(self.__stack)
                    self.__stack.clear()

                t_start = time.time()
                if frame is None: break
                detections = track(frame, self.__model, self.__classes, class_mask, self.__tracker)
                if detections is None:
                    image = frame
                else:
                    image = draw_rect_on_frame(frame, detections, self.__classes, self.__colors)
                cv2.putText(image, text=f'FPS: {fps}', org=(3,15), fontFace=cv2.FONT_HERSHEY_SIMPLEX,
                            fontScale=0.6, color=(255, 0, 0), thickness=2)
                cv2.imshow("image", image)
                if cv2.waitKey(1) & 0xFF == ord("q"):
                    raise KeyboardInterrupt

                results = [dict(x1=int(d[0]), y1=int(d[1]), x2=int(d[2]), y2=int(d[3]), id=str(int(d[4]))) for d in detections] if detections is not None and len(detections) > 0 else []

                t_end = time.time()
                proc_time = t_end - t_start
                fps = round(1.0 / proc_time, 2)
                skip_frames = int(30 * proc_time)
                print(f'Processing time = {proc_time}, fps = {fps}, Skip frames = {skip_frames}')

                # データをAMQにパブリッシュ
                data = dict(timestamp=t_start, results=results)
                self.__collection.insert_one(data)

        except KeyboardInterrupt:
            pass

    def __enter__(self):
        return self

    def __exit__(self, ex_type, ex_value, trace):
        self.__running = False
        if self.__cap is not None: self.__cap.release()
        cv2.destroyAllWindows()
