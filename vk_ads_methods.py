import requests
import json


with open('resources/credentials.json', 'r') as file:
    access_token = json.load(file)['access_token']

account_id = 1900012938


def get_clients():
    url = 'https://api.vk.com/method/ads.getClients'
    params = {
        "account_id": account_id,
        "access_token": access_token,
        'v': '5.131'
    }
    
    response = requests.get(url, params).json()
    
    # with open('assets/clients.json', 'w') as f:
    #     json.dump(response, f, indent=3)
    return response


def get_campaigns(client_id):
    url = 'https://api.vk.com/method/ads.getCampaigns'
    params = {
        "account_id": account_id,
        "client_id": client_id,
        "access_token": access_token,
        "include_deleted": 1,
        "fields": "ads_count",
        'v': '5.131'
    }

    response = requests.get(url, params).json()

    # with open('assets/campaigns.json', 'w') as f:
    #     json.dump(response, f, indent=3)
    return response


def get_ads(client_id, campaign_ids):
    url = 'https://api.vk.com/method/ads.getAds'
    params = {
        "account_id": account_id,
        "client_id": client_id,
        "campaign_ids": f"[{campaign_ids}]",
        "access_token": access_token,
        "include_deleted": 1,
        "limit": 2000,
        "v": "5.131"
    }

    response = requests.get(url, params).json()

    # with open('assets/ads.json', 'w') as f:
    #     json.dump(response, f, indent=3)
    return response


def get_statistics(ids_type, ids, date_from, date_to):
    url = 'https://api.vk.com/method/ads.getStatistics'
    params = {
        "account_id": account_id,
        "ids_type": ids_type,
        "ids": ids,
        "period": "day",
        "date_from": date_from,
        "date_to": date_to,
        "access_token": access_token,
        "limit": 2000,
        "v": "5.131"
    }

    response = requests.get(url, params).json()

    # with open('assets/statistics.json', 'w') as f:
    #     json.dump(response, f, indent=3)
    return response
