import json
import requests
import os
from itertools import product
from tqdm import tqdm


device = 230
country = "RU"
region = 5
v = "2.0"
lang = "en_US"
channel = "a100900101016"
sn = "20401144071142"
cv = "100778_6.11.0"
appplatform = "android_phone"
devices = list(range(220, 280)) + list(range(400, 450)) + [7995648, 7995649, 7930112, 7930113] #415, 414, 241, 242, 246, 247
countries = ['US', 'RU', 'CH', 'UA']
langs = ['ru_RU']
# APP_TOKEN here
app_token = "RQVBQEJyQktGXip6SltGSlpuQkZgBAAEAAAAAP4CH8dQnFiIyheLSM89EhSmu4GNhYRkCn-4GDK_ws5Tp1rG22kZkrazk94dcxvn_I3Ag7296PaKgR-bLSL7VAqbMLae5Q02CYmW2CC0GAW-nOcdb2mEtQP-LRbqeHZTS2guu3Lm4imbUB2DF9iK0MpMBOKFeDHOiYvH6xGGCpQfrh8apXytVKOdgI9-eq8Tn"


burp0_url = f"https://api-mifit-ru.huami.com:443/market/devices/{device}/app?&page=1&per_page=100&userid=8727068155&user_country={country}&user_region={region}&sn={sn}"
burp0_headers = {"Hm-Privacy-Diagnostics": "false", "Country": country, "Cv": cv, "Appplatform": appplatform, "Appname": "com.huami.midong", "Hm-Privacy-Ceip": "true", "V": v, "Timezone": "Europe/Moscow", "Channel": channel, "Apptoken": app_token, "Lang": lang, "X-Request-Id": "9a29c337-7c0c-4638-bb3a-247e979d5a6d", "User-Agent": "Zepp/6.11.0 (Mi 10 Pro; Android 12; Density/2.75)", "Accept-Encoding": "gzip, deflate"}

print("Updating app database...")
for i, k in tqdm(list(product(devices, countries))):
    for lang in langs:
        device = i
        country = k
        os.makedirs(f"{lang}/apps_{country}_device", exist_ok=True)
        burp0_url = f"https://api-mifit-ru.huami.com:443/market/devices/{device}/app?&page=1&per_page=100&userid=8727068155&user_country={country}&user_region={region}&sn={sn}"
        burp0_headers = {"Hm-Privacy-Diagnostics": "false", "Country": country, "Cv": cv, "Appplatform": appplatform, "Appname": "com.huami.midong", "Hm-Privacy-Ceip": "true", "V": v, "Timezone": "Europe/Moscow", "Channel": channel, "Apptoken": app_token, "Lang": lang, "X-Request-Id": "9a29c337-7c0c-4638-bb3a-247e979d5a6d", "User-Agent": "Zepp/6.11.0 (Mi 10 Pro; Android 12; Density/2.75)", "Accept-Encoding": "gzip, deflate"}
        r = requests.get(burp0_url, headers=burp0_headers)
        j = json.loads(r.text)
        for q in j['data']:
            if q == 'code':
                continue
            q['config'] = json.loads(q['config'])
        if len(j['data']) != 0:
            with open(f"{lang}/apps_{country}_device/{i}.json", 'w') as f:
                json.dump(j, f)
            #print(i, k, len([k['name'] for k in j['data']]), ':', ", ".join([k['name'] for k in j['data']]), '\n')
