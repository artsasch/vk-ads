from methods import get_campaigns, get_ads, get_campaigns_statistics
import requests
import datetime
import json


client_id = 17778548
client_name = 'adv_cabandos_vk'
with open('../resources/adv_tokens.json') as json_file:
    data = json.load(json_file)
access_token = data[client_name]['access_token']

date_to = datetime.date.today()
date_from = str(datetime.date(date_to.year, date_to.month - 2, 1))


campaigns = get_campaigns(client_id=client_id,
                          client_name=client_name,
                          access_token=access_token)

# ads = get_ads(client_id=client_id,
#               client_name=client_name,
#               access_token=access_token)

campaigns_dict = {i['id']: i['name'] for i in campaigns['items']}
campaigns_ids = list(campaigns_dict.keys())
print(campaigns_ids)

# campaigns_statistics = get_campaigns_statistics(date_from=date_from,
#                                                 date_to=str(date_to),
#                                                 campaigns_ids=campaigns_ids,
#                                                 client_name=client_name,
#                                                 access_token=access_token)
