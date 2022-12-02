import cv2
import pandas as pd
from threading import *
import pathlib
import os


class CVDetector(Thread):
    def __init__(self,cap, queue, path, lock, sentinel, attrs):
        super().__init__()
        self.queue = queue
        self.sentinel = sentinel
        self.MAX_NUM_BIRDS = 0
        self.path = path
        self.birdsCascade = cv2.CascadeClassifier(path)
        self.cap = cap
        self.attrs = attrs
        self.lock = lock

    def get_pose(self, frame):
        """ Return a list of dict
        A dict for each bird in the frame
        If a frame contains one bird then the liat contains one dict
        [{H:R, Leg:up, T:L, w:on}]
        If a frame contains two birds then the list contains two dict
        i.e
        [{H:L,leg:down, T:C, W:off},
        {H:c, leg:up, T:R, w:on}]
        return [{'headpose': 1, 'legpose': 3, 'wingpose': 2, 'tailpose': 4}, {'headpose': 55, 'legpose': 2, 'wingpose': 2, 'tailpose': 14}, {'headpose': 11, 'legpose': 23, 'wingpose': 32, 'tailpose': 44}] 
        """

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
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            birds = self.birdsCascade.detectMultiScale(
                gray,
                scaleFactor=1.4,
                minNeighbors=2,
                #minSize=(10, 10),
                maxSize=(30, 30),
                flags=cv2.CASCADE_SCALE_IMAGE
            )
            if (len(birds) >= self.MAX_NUM_BIRDS):
                self.MAX_NUM_BIRDS = len(birds)
            frame = self.queue.get()
            count += 1
            if (count/frames_count) > last_percent+0.03:
                last_percent = count/frames_count
                print('Processing... ', int(last_percent*100), '%')
        print('max number is: ', self.MAX_NUM_BIRDS)
        data = {str(self.MAX_NUM_BIRDS)}
        df = pd.DataFrame(data, columns=['MAX_COUNT_OF_BIRDS'])
        self.attrs['df'] = df
        self.lock.release()

    def run(self):
        self.process()
