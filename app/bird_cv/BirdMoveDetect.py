import cv2
import pathlib
import os
from app.bird_cv.motionDetection.motion import ClsMotion
import pandas as pd
class BirdMoveDetect:
    def __init__(self):
        current_directory = pathlib.Path(__file__).parent.resolve()
        cascade_path = os.path.join(current_directory,'static','birds1.xml')
        self.birdsCascade = cv2.CascadeClassifier(cascade_path)
        pass

    def get_pose(self, frame):
        """
        Return a list of dict
        A dict for each bird in the frame
        If a frame contains one bird then the liat contains one dict
        [{H:R, Leg:up, T:L, w:on}]
        If a frame contains two birds then the list contains two dict
        i.e
        [{H:L,leg:down, T:C, W:off},
        {H:c, leg:up, T:R, w:on}]"""
        return [{'headpose': 1, 'legpose': 3, 'wingpose': 2, 'tailpose': 4}, {'headpose': 55, 'legpose': 2, 'wingpose': 2, 'tailpose': 14}, {'headpose': 11, 'legpose': 23, 'wingpose': 32, 'tailpose': 44}]

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
        changes_converted = self.convert_to_pd(changes_arr)
        #changes_converted = changes_converted.reset_index(drop=True)
        return changes_converted.fillna('')

    def convert_to_pd(self, bird_dict):
        frames = []
        for time, bird in bird_dict.items():
            output_dict = dict()
            output_dict['time'] = time
            output_dict['head_movement'] = ''
            output_dict['leg_movement'] = ''
            output_dict['tail_movement'] = ''
            output_dict['wing_movement'] = ''
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
