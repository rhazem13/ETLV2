from detector import CVDetector
from reader import CVReader
from queue import Queue
from sql_metadata import Parser
import pandas as pd
import cv2
parser = Parser('SELECT * FROM birds')
def extract_count_of_birds_from_video(filepath, atributes = None) -> pd.DataFrame:
    SENTINEL =object()
    queue = Queue()
    output_path = 'static/birds.csv'
    attrs = dict()
    cap = cv2.VideoCapture(filepath)
    cv_reader = CVReader(cap , queue, SENTINEL )
    cv_detector = CVDetector(cap, queue, output_path, SENTINEL, attrs)
    cv_reader.start()
    cv_detector.start()
    cv_reader.join()
    cv_detector.join()
    return attrs['df']

print(extract_count_of_birds_from_video('static/birds.mp4'))

#s