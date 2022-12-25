from app.etl.DataSources.Database.Database import Database
from app.etl.DataSources.Database.EDatabase import DatabaseType
from app.etl.DataSources.Flatfile.EFlatfile import EFlatfile
from app.etl.DataSources.Flatfile.Flatfile import Flatfile
from app.etl.DataSources.Media.EMedia import EMedia
from app.etl.DataSources.IDataSource import IDataSource
from app.etl.DataSources.Media.Media import Media
from app.etl.DataSources.Console.EConsole import EConsoleTypes
from app.etl.DataSources.Console.Console import Console
class DataSourceFactory():

    @classmethod
    def createDataSource(cls ,data_source) -> IDataSource:
        Type=cls._determineType(data_source)
        handlers={
            DatabaseType.MSSQL: (lambda : Database(DatabaseType.MSSQL,data_source)),
            DatabaseType.SQLLITE: (lambda : Database(DatabaseType.SQLLITE,data_source)),
            EFlatfile.JSON:(lambda : Flatfile(EFlatfile.JSON,)),
            EFlatfile.HTML:(lambda : Flatfile(EFlatfile.HTML)),
            EFlatfile.CSV:(lambda : Flatfile(EFlatfile.CSV)),
            EFlatfile.EXCEL:(lambda : Flatfile(EFlatfile.EXCEL)),
            EMedia.VIDEO:(lambda : Media(EMedia.VIDEO)),
            EMedia.IMAGE:(lambda : Media(EMedia.IMAGE)),
            EMedia.FRAMES:(lambda : Media(EMedia.FRAMES)),
            EConsoleTypes.STDOUT:(lambda: Console(EConsoleTypes.STDOUT)),
            EConsoleTypes.CUSTOM:(lambda: Console(EConsoleTypes.CUSTOM))
        }
        return handlers[Type]()
    
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
        elif(T=='frames'):
            return EMedia.FRAMES
        elif(T=='img'):
            return EMedia.IMAGE
        elif (T == 'stdout'):
            return EConsoleTypes.STDOUT
        elif(T == 'custom'):
            return EConsoleTypes.CUSTOM
        else:
            raise ValueError(T+" is not supported datasource type")