from vk_ads_methods import get_clients, get_campaigns, get_ads, get_statistics


account_id = 1900012938
client_id = 1608343119
campaign_id = 1028976655


get_clients()
get_campaigns(client_id=client_id)
get_ads(client_id=client_id, campaign_ids=campaign_id)
get_statistics(ids_type="campaign", ids=campaign_id, date_from="2023-08-01", date_to="2023-08-31")
