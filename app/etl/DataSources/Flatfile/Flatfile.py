from DataSources import IDataSource
class Flatfile(IDataSource):
    def __init__(self, type) -> None:
        super().__init__(type)

    def load(self, file_path):
        print('load flatfile')

    def extract(self, file_path):
        print('extract flatfile')