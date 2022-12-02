from app.bird_cv.core import BirdsCV 
from app.etl.DataSources.IDataSource import IDataSource

class Media(IDataSource):
    def __init__(self, type) -> None:
        super().__init__(type)

    def extract(self, file_path):
        data = BirdsCV().extract_attrs_from_video(file_path)
        return data
    def load(self, file_path):
        print('not supported yet to load on media')
