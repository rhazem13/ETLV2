import pandas as pd
import logging
from app.etl.helpers import __filter
from app.etl.DataSources.factory import DataSourceFactory
from app.etl.DataSources.IDataSource import IDataSource
logger = logging.getLogger('ETL')
result = None
def extract(data_source:str) -> pd.DataFrame:
    file_path = data_source.split('::')[1]
    data_source:IDataSource = DataSourceFactory.createDataSource(data_source)
    logger.info('Extract Data source type is: '+data_source.__class__.__name__)
    data = data_source.extract(file_path)
    return data



def transform(data:pd.DataFrame, criteria:dict) -> pd.DataFrame:
    # filtering
    if criteria['FILTER']:
        data = __filter(data, criteria['FILTER'])

    # columns
    if criteria['COLUMNS'] != '__all__':
        data = data.filter(items=criteria['COLUMNS'])


    # distinct
    if criteria['DISTINCT']:
        data = data.drop_duplicates()

    # ordering
    if criteria['ORDER']:
        column = criteria['ORDER'][0]
        data = data.sort_values(column, ascending=criteria['ORDER'][1] == 'ASC')

    # limit
    if criteria['LIMIT']:
        data = data[:criteria['LIMIT']]

    if criteria['DATA_SOURCE_TYPE'] == 'video':
        max_nans = len(data.columns) -1 if 'time' in data.columns or'__all__' not in['COLUMNS'] else len(data.columns)
        hightech_export= data.loc[data.isnull().sum(axis=1)<max_nans]

    return hightech_export.fillna('')



def load(data:pd.DataFrame, data_destination:str):
    # print(data)
    global result
    file_path = data_destination.split('::')[1]
    data_destination:IDataSource = DataSourceFactory.createDataSource(data_destination)
    logger.info('Load Data distination type is: '+data_destination.__class__.__name__)
    result = data_destination.load(data, file_path)

    if result is None:
        result = "Eexecution Done!"
    return data
