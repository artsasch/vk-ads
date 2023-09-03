import pandas as pd
import sqlalchemy
import requests
import json


with open('../resources/sql_engine.txt', 'r') as file:
    sql_engine = file.read()


def get_campaigns(client_name, access_token):
    if 'mytarget' in client_name:
        url = 'https://ads.vk.com/api/v2/campaigns.json'
    else:
        url = 'https://ads.vk.com/api/v2/ad_plans.json'
    params = {
        'metrics': 'all',
        'limit': 250,
    }
    headers = {
        'Authorization': f'Bearer {access_token}'
    }
    response = requests.get(url, params=params, headers=headers).json()
    # with open(f'assets/{client_name}_campaigns.json', 'w') as f:
    #     json.dump(response, f, indent=3)
    return response


def get_ads(client_name, access_token):
    url = 'https://ads.vk.com/api/v2/banners.json'
    params = {
        'fields': 'id, name',
        'limit': 250,
    }
    headers = {
        'Authorization': f'Bearer {access_token}'
    }
    response = requests.get(url, params=params, headers=headers).json()
    # with open(f'assets/{client_name}_ads.json', 'w') as f:
    #     json.dump(response, f, indent=3)
    return response


def get_campaigns_statistics(date_from, date_to, campaigns_ids, client_name, access_token):
    if 'mytarget' in client_name:
        url = 'https://ads.vk.com/api/v2/statistics/campaigns/day.json'
    else:
        url = 'https://ads.vk.com/api/v2/statistics/ad_plans/day.json'
    params = {
        'date_from': date_from,
        'date_to': str(date_to),
        'metrics': 'base'
    }
    headers = {
        'Authorization': f'Bearer {access_token}'
    }
    response = requests.get(url, params=params, headers=headers).json()
    # with open(f'assets/{client_name}_campaigns_statistics.json', 'w') as f:
    #     json.dump(response, f, indent=3)
    return response


def get_ads_statistics(date_from, date_to, ads_ids, client_name, access_token):
    url = 'https://ads.vk.com/api/v2/statistics/banners/day.json'
    params = {
        'date_from': date_from,
        'date_to': str(date_to),
        'metrics': 'base'
    }
    headers = {
        'Authorization': f'Bearer {access_token}'
    }
    response = requests.get(url, params=params, headers=headers).json()
    # with open(f'assets/{client_name}_ads_statistics.json', 'w') as f:
    #     json.dump(response, f, indent=3)
    return response


def load_to_database(df, table_name):
    engine = sqlalchemy.create_engine(sql_engine)
    inspector = sqlalchemy.inspect(engine)
    if not inspector.has_table(table_name):
        df.head(0).to_sql(table_name, engine, if_exists='replace', index=False)
    df.to_sql(table_name, engine, if_exists='replace', index=False)
    print(f'{table_name} loaded to database')


def convert_to_dataframe(statistics, reference_df, client_name, category):
    table_name = f'{client_name}_{category}_statistics'
    df = pd.json_normalize(statistics['items'], 'rows', 'id')
    df = pd.merge(df, reference_df[['id', 'name']], on='id', how='left')
    df.to_csv(f'assets/{table_name}.csv', index=False)
    df = pd.read_csv(f'assets/{table_name}.csv')
    df.columns = df.columns.str.replace('.', '_', regex=True)
    return df
