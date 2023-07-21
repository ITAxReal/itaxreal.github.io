import json
import requests
from itertools import product
from tqdm import tqdm
from packaging import version


# Request vars
device = 230
country = "RU"
region = 5
v = "2.0"
lang = "en_US"
channel = "a100900101016"
sn = "20401144071142"
cv = "101035_7.7.5"
appplatform = "android_phone"
devices = list(range(220, 280)) + list(range(400, 450)) + [7995648, 7995649, 7930112, 7930113] #415, 414, 241, 242, 246, 247
countries = [('RU', 'ru_RU'), ('US', 'en_US'), ('CH', 'en_US'), ('UA', 'ru_RU')]
# langs = ['ru_RU']
# lang = "ru_RU"
dbfile = 'zepprep.json'

replacings = {
    ('230', '229'): "GTR3-PRO",
    ('226', '227'): "GTR3",
    ('224', '225'): "GTS3",
    ('418', '419'): "T-REX2",
    ('241', '242'): "GTR3-PRO-LE",
    ('246', '247'): "GTS4-Mini",
    ('252',): "Band7-NFC",
    ('253', '254'): "Band7",
    ('414', '415'): "Falcon",
    ('260', '261'): "MiBand7-NFC",
    ('262', '263', '264', '265', '266'): "MiBand7",
    ('7995648', '7995649'): "GTS4",
    ('7930112', '7930113'): "GTR4",
}

# APP_TOKEN here (Could be retrieved from /data/data/com.huami.watch.hmwatchmanager/shared_prefs/hm_id_sdk_android.xml)
app_token = "RQVBQEJyQktGXip6SltGSlpuQkZgBAAEAAAAA6xDRgmGnPFo0nMatkC6eKMFgwxu5Ed0SZvspFWK5sgvsednVYB3RxIXq6fA9YBGhTsc529GNWfeWrlUvDivEPudfpQkqi4MYGxSNWkSYW2BKb5wsppLAa8x4gDkYZLvWRR80XGLImRV3PwgqCG69syndT-udPj8H3u9JyQLwoOUoeJO_uWzcl9uWnGQWKQeU"


base_url = "https://api-mifit-ru.huami.com:443/market/devices/{dev}/app?&page=1&per_page=100&userid=8727068155&user_country={ctr}&user_region={reg}&sn={sn}"
headers = {
    "Hm-Privacy-Diagnostics": "false",
    "Country": country,
    "Cv": cv,
    "Appplatform": appplatform,
    "Appname": "com.huami.midong",
    "Hm-Privacy-Ceip": "true",
    "V": v,
    "Timezone": "Europe/Moscow",
    "Channel": channel,
    "Apptoken": app_token,
    "Lang": lang,
    "X-Request-Id": "9a29c337-7c0c-4638-bb3a-247e979d5a6d",
    "User-Agent": "Zepp/7.7.5 (Mi 10 Pro; Android 12; Density/2.75)",
    "Accept-Encoding": "gzip, deflate"
}

zepprep = {}

print("Updating app database...")
with requests.Session() as sess:
    for device, (country, lang) in tqdm(list(product(devices, countries))):
        devname = next(iter([cdname for cdevs, cdname in replacings.items() if str(device) in cdevs]), None) or f"DEV-{device}"
        zepprep.setdefault(devname, {})
        # for lang in langs:
        # os.makedirs(f"{lang}/apps_{country}_device", exist_ok=True)
        url = base_url.format(dev=device, ctr=country, reg=region, sn=sn)
        headers.update({"Country": country, "Lang": lang})
        r = sess.get(url, headers=headers)
        j = json.loads(r.text)
        for q in j['data']:
            if q == 'code':
                continue
            q['config'] = json.loads(q['config'])
        if len(j['data']) != 0:
            for app in j['data']:
                app['fetchcntr'] = country
                appid = app['appid']
                ver = app['version']
                savedapp = zepprep[devname].get(appid, None)
                if not savedapp:
                    zepprep[devname][appid] = app
                elif version.parse(ver) > version.parse(savedapp['version']):
                    zepprep[devname][appid] = app
                else:
                    continue
        if not len(zepprep[devname]):
            zepprep.pop(devname)
                
            # with open(f"{lang}/apps_{country}_device/{device}.json", 'w') as f:
            #     json.dump(j, f)
        #print(i, k, len([k['name'] for k in j['data']]), ':', ", ".join([k['name'] for k in j['data']]), '\n')

with open(dbfile, 'w') as f:
    json.dump(zepprep, f, indent=4)

print(f"Database saved to {dbfile}")
