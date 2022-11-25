from app.etl.DataSources.IDataSource import IDataSource
class Console(IDataSource):
    def extract():
        raise NotImplementedError('Extract method not implemented for console')

    def load(cls, data, file_path):
        print(data)