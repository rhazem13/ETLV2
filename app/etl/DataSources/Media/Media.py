from app.bird_cv.core import extract_count_of_birds_from_video 
from app.etl.DataSources.IDataSource import IDataSource

class Media(IDataSource):
    def __init__(self, type) -> None:
        super().__init__(type)

    def extract(self, file_path):
        data = extract_count_of_birds_from_video(file_path)
        return data
    def load(self, file_path):
        print('not supported yet to load on media')
