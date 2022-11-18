from app.bird_cv.detector import CVDetector
from app.bird_cv.reader import CVReader
from queue import Queue
import pandas as pd
import cv2


def extract_count_of_birds_from_video(filepath, atributes=None) -> pd.DataFrame:
    SENTINEL = object()
    queue = Queue()
    output_path = 'static/birds.csv'
    attrs = dict()
    cap = cv2.VideoCapture(filepath)
    cv_reader = CVReader(cap, queue, SENTINEL)
    cv_detector = CVDetector(cap, queue, output_path, SENTINEL, attrs)
    cv_reader.start()
    cv_detector.start()
    cv_reader.join()
    cv_detector.join()
    return attrs['df']


#extract_count_of_birds_from_video(
#    "C:\\Users\\rhaze\\Desktop\\Projects\\ETLV2\\app\\bird_cv\\static\\birds.mp4")
