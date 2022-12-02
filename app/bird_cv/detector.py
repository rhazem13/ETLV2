import cv2
import pandas as pd
from threading import *
from app.bird_cv.BirdMoveDetect import BirdMoveDetect

class CVDetector(Thread):
    def __init__(self,cap, queue, lock, sentinel, attrs):
        super().__init__()
        self.queue = queue
        self.sentinel = sentinel
        self.MAX_NUM_BIRDS = 0
        self.cap = cap
        self.attrs = attrs
        self.lock = lock
        self.move_detector = BirdMoveDetect()

    
    def getStats(self):

        fps = self.cap.get(cv2.CAP_PROP_FPS)
        frame_count = int(self.cap.get(cv2.CAP_PROP_FRAME_COUNT))

        codec = self.cap.get(cv2.CAP_PROP_FOURCC)
        durationSec = frame_count/fps * 1000
        return (fps, frame_count, durationSec)

    def process(self):
        frame = self.queue.get()
        frames_count = self.getStats()[1]
        count = 0
        last_percent = 0
        while frame is not self.sentinel:
            birds_count = self.move_detector.get_count(frame)
            count += 1
            if (birds_count >= self.MAX_NUM_BIRDS):
                self.MAX_NUM_BIRDS = birds_count
            frame = self.queue.get()
            if (count/frames_count) > last_percent+0.03:
                last_percent = count/frames_count
                print('Processing... ', int(last_percent*100), '%')
        data = {str(self.MAX_NUM_BIRDS)}
        df = pd.DataFrame(data, columns=['MAX_COUNT_OF_BIRDS'])
        self.attrs['df'] = df
        self.lock.release()

    def run(self):
        self.process()
