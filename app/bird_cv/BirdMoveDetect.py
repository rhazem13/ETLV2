import cv2
import pathlib
import os
from app.bird_cv.motionDetection.motionv2 import ClsMotion
import pandas as pd
from numpy import nan

class BirdMoveDetect:
    def __init__(self):
        current_directory = pathlib.Path(__file__).parent.resolve()
        cascade_path = os.path.join(current_directory,'static','birds1.xml')
        self.birdsCascade = cv2.CascadeClassifier(cascade_path)
        pass

    def get_count(self, frame) -> int:
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        birds = self.birdsCascade.detectMultiScale(
            gray,
            scaleFactor=1.4,
            minNeighbors=2,
            #minSize=(10, 10),
            maxSize=(30, 30),
            flags=cv2.CASCADE_SCALE_IMAGE
        )
        return len(birds)

    def get_changes(self, framesPath):
        motion = ClsMotion()
        changes_arr = motion.process_frames(framesPath) 
        return changes_arr

    def get_changes_for_video(self, video_path):
        motion = ClsMotion()
        changes_arr = motion.process_videos(video_path) 
        return changes_arr

    def convert_to_pd(self, bird_dict):
        frames = []
        for time, bird in bird_dict.items():
            output_dict = dict()
            output_dict['time'] = time
            output_dict['head_movement'] = nan
            output_dict['leg_movement'] = nan
            output_dict['tail_movement'] = nan
            output_dict['wing_movement'] = nan
            if(0 in bird):
                output_dict['head_movement'] = True
                output_dict['head_movement_time_span'] = bird[0][0]
                output_dict['head_movement_time_start'] = bird[0][1]

            if(1 in bird):
                output_dict['leg_movement'] = True
                output_dict['leg_movement_time_span'] = bird[1][0]
                output_dict['leg_movement_time_start'] = bird[1][1]

            if(2 in bird):
                output_dict['wing_movement'] = True
                output_dict['wing_movement_time_span'] = bird[2][0]
                output_dict['wing_movement_time_start'] = bird[2][1]

            if(3 in bird):
                output_dict['tail_movement'] = True
                output_dict['tail_movement_time_span'] = bird[3][0]
                output_dict['tail_movement_time_start'] = bird[3][1]

            frames.append(output_dict)
        return pd.DataFrame(frames)
