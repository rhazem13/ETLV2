import cv2
import pathlib
import os

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