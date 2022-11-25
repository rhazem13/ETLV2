from msilib.schema import Media
from app.etl.DataSources.Database.Database import Database
from app.etl.DataSources.Database.EDatabase import DatabaseType
from app.etl.DataSources.Flatfile.EFlatfile import EFlatfile
from app.etl.DataSources.Flatfile.Flatfile import Flatfile
from app.etl.DataSources.Media.EMedia import EMedia


class FileFactory():
    def __init__(self,data_source):
        self.Type=self.determineType(data_source)
        self.handlers={
            DatabaseType.MSSQL: Database(DatabaseType.MSSQL),
            DatabaseType.SQLLITE: Database(DatabaseType.SQLLITE),
            EFlatfile.JSON:Flatfile(EFlatfile.JSON),
            EFlatfile.HTML:Flatfile(EFlatfile.HTML),
            EFlatfile.CSV:Flatfile(EFlatfile.CSV),
            EFlatfile.EXCEL:Flatfile(EFlatfile.EXCEL),
            EMedia.VIDEO:Media(EMedia.VIDEO),
            EMedia.IMAGE:Media(EMedia.IMAGE)
        }
    
    
    def determineType(self,data_source):
        T=data_source.split(':')[0]
        if(T=='mssql'):
            return DatabaseType.MSSQL
        elif(T=='sqllite'):
            return DatabaseType.SQLLITE
        elif(T=='json'):
            return EFlatfile.JSON
        elif(T=='html'):
            return EFlatfile.HTML
        elif(T=='csv'):
            return EFlatfile.CSV
        elif(T=='xml'):
            return EFlatfile.XML
        elif(T=='excel'):
            return EFlatfile.EXCEL
        elif(T=='video'):
            return EMedia.VIDEO
        elif(T=='img'):
            return EMedia.IMAGE
    