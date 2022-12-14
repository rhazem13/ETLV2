from app.bird_cv.core import BirdsCV 
from app.etl.DataSources.IDataSource import IDataSource
from app.bird_cv.BirdMoveDetect import BirdMoveDetect
class Media(IDataSource):
    def __init__(self, type) -> None:
        super().__init__(type)

    def extract(self, file_path):
        data = BirdMoveDetect().get_changes(file_path)
        return data
    def load(self, file_path):
        print('not supported yet to load on media')
