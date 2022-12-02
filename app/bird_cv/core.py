from app.bird_cv.detector import CVDetector
from app.bird_cv.reader import CVReader
from queue import Queue
import pandas as pd
import cv2
import pathlib
import os
import threading
lock = threading.Semaphore(0)
class BirdsCV:
    def extract_attrs_from_video(selv, filepath, atributes=None) -> pd.DataFrame:
        SENTINEL = object()
        queue = Queue()
        attrs = dict()
        cap = cv2.VideoCapture(filepath)
        cv_reader = CVReader(cap, queue, SENTINEL)
        cv_detector = CVDetector(cap, queue, lock, SENTINEL, attrs)
        cv_reader.start()
        cv_detector.start()
        lock.acquire()
        return attrs['df']