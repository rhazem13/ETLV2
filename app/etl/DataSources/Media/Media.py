from app.bird_cv.core import BirdsCV 
from app.etl.DataSources.IDataSource import IDataSource
from app.bird_cv.BirdMoveDetect import BirdMoveDetect
from app.etl.DataSources.Media.EMedia import EMedia
class Media(IDataSource):
    def __init__(self, type:EMedia) -> None:
        super().__init__(type)
        self.extractCallbacks = {
            EMedia.VIDEO: (lambda path: print('not implemented')),
            EMedia.IMAGE: (lambda path: print('not implemented') ),
            EMedia.FRAMES: (lambda path: BirdMoveDetect().get_changes(path)),
        }
    def extract(self, file_path):
        data = self.extractCallbacks[self.type](file_path)
        return data
    def load(self, file_path):
        print('not supported yet to load on media')
