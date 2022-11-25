import pandas as pd
from app.etl.extract import __extract_from_csv,__extract_from_video, __extract_from_sqlite, __extract_from_mssql, __extract_from_html, __extract_from_json, __extract_from_xml, __extract_from_excel
from app.etl.helpers import __get_source_type, __filter
from app.etl.load import __load_to_csv, __load_to_sqlite, __load_to_mssql, __load_to_html, __load_to_json, __load_to_xml, __load_to_excel
from app.etl.DataSources.factory import DataSourceFactory
from app.etl.DataSources.IDataSource import IDataSource
result = None


def extract(data_source:str) -> pd.DataFrame:
    file_path = data_source.split('::')[1]
    data_source:IDataSource = DataSourceFactory.createDataSource(data_source)
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

    return data



def load(data:pd.DataFrame, data_destination:str):
    global result
    print('####################################')
    print(data_destination)
    print('####################################')

    file_path = data_destination.split('::')[1]
    data_destination:IDataSource = DataSourceFactory.createDataSource(data_destination)
    data = data_destination.load(data, file_path)
    result= 'Excution Done!'
    # global result
    # source_type = __get_source_type(data_destination)
    # if source_type == 'CSV':
    #     __load_to_csv(data, data_destination)
    #     result = 'Execution Done!'
    # elif source_type == 'SQLITE':
    #     db_destination = data_destination.split('/')[0]
    #     table_name = data_destination.split('/')[1]
    #     __load_to_sqlite(data, db_destination, table_name)
    #     result = 'Execution Done!'
    # elif source_type == 'MSSQL':
    #     __load_to_mssql(data, data_destination)
    #     result = 'Execution Done!'
    # elif source_type == 'HTML':
    #     __load_to_html(data, data_destination)
    #     result = 'Execution Done!'
    # elif source_type == 'JSON':
    #     __load_to_json(data, data_destination)
    #     result = 'Execution Done!'
    # elif source_type == 'XML':
    #     __load_to_xml(data, data_destination)
    #     result = 'Execution Done!'
    # elif source_type == 'EXCEL':
    #     __load_to_excel(data, data_destination)
    #     result = 'Execution Done!'
    # elif source_type == 'CONSOL':
    #     result = data
    #     # print(data)
    # else:
    #     raise Exception(f'Unsupported data destination')
