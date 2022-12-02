import pandas as pd
from app.etl.helpers import __filter
from app.etl.DataSources.factory import DataSourceFactory
from app.etl.DataSources.IDataSource import IDataSource
result = None


def extract(data_source:str) -> pd.DataFrame:
    file_path = data_source.split('::')[1]
    data_source:IDataSource = DataSourceFactory.createDataSource(data_source)
    # try: 
    print(file_path)
    data = data_source.extract(file_path)
    print("extract")
    # except: 
    #     return print("File Path not found")
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

    return data



def load(data:pd.DataFrame, data_destination:str):
    global result

    file_path = data_destination.split('::')[1]
    data_destination:IDataSource = DataSourceFactory.createDataSource(data_destination)
    result = data_destination.load(data, file_path)
    if result is None:
        result = "Eexecution Done!"
    return data
