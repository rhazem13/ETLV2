from DataSources import IDataSource
from Flatfile.EFlatfile import EFlatfile
import pandas as pd
class Flatfile(IDataSource):
    def __init__(self, type:EFlatfile) -> None:
        super().__init__(type)
        self.extractCallbacks = {
            f'{EFlatfile.HTML}': (lambda path: pd.read_html(path)),
            f'{EFlatfile.JSON}': (lambda path: pd.read_json(path)),
            f'{EFlatfile.XML}': (lambda path: pd.read_xml(path)),
            f'{EFlatfile.CSV}': (lambda path: pd.read_csv(path)),
            f'{EFlatfile.EXCEL}': (lambda path: pd.read_excel(path))
        }
        self.loadCallbacks = {
            f'{EFlatfile.HTML}': (lambda data, path: data.to_html(path)),
            f'{EFlatfile.JSON}': (lambda data,  path: data.to_json(path)),
            f'{EFlatfile.XML}': (lambda path: pd.to_xml(path)),
            f'{EFlatfile.CSV}': (lambda path: pd.read_csv(path)),
            f'{EFlatfile.EXCEL}': (lambda path: pd.read_excel(path))
        }

    def load(self, file_path):
        self.callbacks[f'{self.type}'](file_path)

    def extract(self, file_path):
        self.callbacks[f'{self.type}'](file_path)