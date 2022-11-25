from app.bird_cv.detector import CVDetector
from app.bird_cv.reader import CVReader
from queue import Queue
import pandas as pd
import cv2
import pathlib
import os
import threading
sem = threading.Semaphore(1)

def extract_count_of_birds_from_video(filepath, atributes=None) -> pd.DataFrame:
    SENTINEL = object()
    queue = Queue()
    current_directory = pathlib.Path(__file__).parent.resolve()
    cascade_path = os.path.join(current_directory,'static','birds1.xml')
    attrs = dict()
    cap = cv2.VideoCapture(filepath)
    cv_reader = CVReader(cap, queue, SENTINEL)
    cv_detector = CVDetector(cap, queue, cascade_path, sem, SENTINEL, attrs)
    cv_reader.start()
    cv_detector.start()
    sem.acquire()
    return attrs['df']