import requests
import json


def get_campaigns(client_id, client_name, access_token):
    url = 'https://ads.vk.com/api/v2/ad_plans.json'
    params = {
        'id': client_id,
        'metrics': 'all'
    }
    headers = {
        'Authorization': f'Bearer {access_token}'
    }
    response = requests.get(url, params=params, headers=headers).json()
    with open(f'assets/{client_name}_campaigns.json', 'w') as f:
        json.dump(response, f, indent=3)
    return response


def get_ads(client_id, client_name, access_token):
    url = 'https://ads.vk.com/api/v2/banners.json'
    params = {
        'id': client_id,
        'metrics': 'all'
    }
    headers = {
        'Authorization': f'Bearer {access_token}'
    }
    response = requests.get(url, params=params, headers=headers).json()
    with open(f'assets/{client_name}_ads.json', 'w') as f:
        json.dump(response, f, indent=3)
    return response


def get_campaigns_statistics(date_from, date_to, campaigns_ids, client_name, access_token):
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
    with open(f'assets/{client_name}_campaigns_statistics.json', 'w') as f:
        json.dump(response, f, indent=3)
    return response
