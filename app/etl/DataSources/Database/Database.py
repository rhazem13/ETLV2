from DataSources import IDataSource
class Database(IDataSource):
    def __init__(self, type) -> None:
        super().__init__(type)

    def extract(self, file_path):
        print ('extracting from database')

    def load(self, file_path):
        print('loading from database')