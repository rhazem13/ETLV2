from app.etl.DataSources.Database.Database import Database
from app.etl.DataSources.Database.EDatabase import DatabaseType
from app.etl.DataSources.Flatfile.EFlatfile import EFlatfile
from app.etl.DataSources.Flatfile.Flatfile import Flatfile
from app.etl.DataSources.Media.EMedia import EMedia
from app.etl.DataSources.IDataSource import IDataSource
from app.etl.DataSources.Media.Media import Media
class DataSourceFactory():

    @classmethod
    def createDataSource(cls ,data_source) -> IDataSource:
        Type=cls._determineType(data_source)
        handlers={
            DatabaseType.MSSQL: Database(DatabaseType.MSSQL,data_source),
            DatabaseType.SQLLITE: Database(DatabaseType.SQLLITE,data_source),
            EFlatfile.JSON:Flatfile(EFlatfile.JSON,),
            EFlatfile.HTML:Flatfile(EFlatfile.HTML),
            EFlatfile.CSV:Flatfile(EFlatfile.CSV),
            EFlatfile.EXCEL:Flatfile(EFlatfile.EXCEL),
            EMedia.VIDEO:Media(EMedia.VIDEO),
            EMedia.IMAGE:Media(EMedia.IMAGE)
        }
        return handlers[Type]
    
    @classmethod
    def _determineType(cls,data_source):
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
    