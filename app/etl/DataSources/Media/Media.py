from app.etl.DataSources.IDataSource import IDataSource

class Media(IDataSource):
    def __init__(self, type) -> None:
        super().__init__(type)

    def extract(self, file_path):
        print('extracting from media')

    def load(self, file_path):
        print('loading from media')
