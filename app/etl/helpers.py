import pandas as pd
import re


def __get_source_type(data_source:str) -> str:
    if data_source == 'CONSOLE':
        return 'CONSOL'
    # elif data_source.split(':')[0]=='video':
    #     print('video  detected')
    #     return 'VIDEO'
    # elif data_source.split(':')[0]=='csv':
    #     print('csv  detected')
    #     return 'CSV'
    # elif data_source.split(':')[0]=='sqllite':
    #     print('SQLITE  detected')
    #     return 'SQLITE'
    # elif data_source.split(':')[0]=='mssql':
    #     print('MSSQL  detected')
    #     return 'MSSQL'
    # elif data_source.split(':')[0]=='html':
    #     print('HTML  detected')
    #     return 'HTML'
    # elif data_source.split(':')[0]=='json':
    #     print('JSON  detected')
    #     return 'JSON'
    # elif data_source.split(':')[0]=='xml':
    #     print('xml detected')
    #     return 'XML'
    # elif data_source.split(':')[0]=='excel':
    #     return 'EXCEL'
    elif re.search(r'.*\.csv(\.zip)?', data_source):   
        return 'CSV'
    elif re.search(r'.*\.db/\w+', data_source):
        return 'SQLITE'
    elif re.search(r'Data Source.*', data_source):
        return 'MSSQL'
    elif re.search(r'.*\.html', data_source):   
        return 'HTML'
    elif re.search(r'.*\.json', data_source):   
        return 'JSON'
    elif re.search(r'.*\.xml', data_source):   
        return 'XML'
    elif re.search(r'.*\.mp4', data_source):   
        return 'VIDEO'     
    elif re.search( r'(.+\.xlsx)| (.+\.xls) | (.+\.xlsm)| (.+\.xlsb)| (.+\.odf)| (.+\.ods)| (.+\.odt)', data_source):   
        return 'EXCEL'

# __get_source_type('video::sx')


def __filter(data:pd.DataFrame, filters:dict) -> pd.DataFrame:
    left = filters['left']
    right = filters['right'] 

    if filters["type"] == 'or' or filters["type"] == 'and':
        left = __filter(data, left)
        right = __filter(data, right)

        if filters["type"] == 'or':
            data = pd.concat([left, right])
        elif filters["type"] == 'and':
            data = pd.merge(left, right)
        data = data[~data.index.duplicated(keep='first')]

    elif filters["type"] == 'like':
        data = data[[True if re.match(right, str(x)) else False for x in data[left]]]
    elif filters["type"] == '>':
        data = data[data[left] > right]
    elif filters["type"] == '>=':
        data = data[data[left] >= right]
    elif filters["type"] == '<':
        data = data[data[left] < right]
    elif filters["type"] == '<=':
        data = data[data[left] <= right]
    elif filters["type"] == '==':
        data = data[data[left] == right]
    elif filters["type"] == '!=':
        data = data[data[left] != right]

    return data



    