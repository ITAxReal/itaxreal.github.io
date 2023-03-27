import base64
import os
import re
import json
import sys
from packaging import version

head = """<!DOCTYPE html>
<html>

<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, shrink-to-fit=no">
    <title>Home - ZeppOS Apps</title>
    <link rel="stylesheet" href="assets/bootstrap/css/bootstrap.min.css">
    <link rel="stylesheet" href="https://fonts.googleapis.com/css?family=Catamaran:100,200,300,400,500,600,700,800,900&amp;display=swap">
    <link rel="stylesheet" href="https://fonts.googleapis.com/css?family=Lato:100,100i,300,300i,400,400i,700,700i,900,900i&amp;display=swap">
</head>

<body>
    <nav class="navbar navbar-dark navbar-expand-lg fixed-top bg-dark navbar-custom">
        <div class="container"><a class="navbar-brand" href="#">ZeppOS Apps [4PDA]</a></div>
    </nav>
    <header class="text-center text-white masthead">
        <div class="masthead-content">
            <div class="container">
                <h2 class="masthead-subheading mb-0"><strong>Репозиторий приложений для смарт-часов на ZeppOS</strong></h2>
            </div>
        </div>
    </header>
    <div class="container">
<div class="container">
    <div class="row">
        <div class="col">
            <h1>-</h1>
        </div>
    </div>
</div>
        <h1>Как устанавливать приложения:</h1>
        <div><a class="btn btn-primary" data-bs-toggle="collapse" aria-expanded="false" aria-controls="collapse-2281337" href="#collapse-2281337" role="button">&gt; Показать видео &lt;</a>
            <div class="collapse" id="collapse-2281337"><iframe allowfullscreen="" frameborder="0" width="270" height="585" src="assets/Videos/install.mp4"></iframe></div>
        </div>
    </div>
<div class="container">
    <div class="row">
        <div class="col">
            <h1>-</h1>
        </div>
    </div>
</div>
    <div class="container">
        <h1>Список приложений (можно ставить приложения других моделей часов):</h1>
        """

foot = """
<div class="container">
    <div class="row">
        <div class="col">
            <h1>-</h1>
        </div>
    </div>
</div>
    <div class="container">
        <h1>Установка циферблата по прямой ссылке:</h1>
        <div class="row">
            <div class="col"><input id="wf_link" class="form-control" type="text" /></div>
            <div class="col"><button id="wf_install" class="btn btn-primary" type="button" onclick="wf_inst();">WatchFace</button></div>
        </div>
    </div>
<div class="container">
    <div class="row">
        <div class="col">
            <h1>-</h1>
        </div>
    </div>
</div>
    <script>
        function wf_inst() {
            var link = document.getElementById('wf_link').value;
            link = btoa(link.replace("http://", "watchface://").replace("https://", "watchface://")).replaceAll('/', '-').replaceAll('+', '*').replaceAll('=', '_');
            window.location = "qr.html?app=" + link;
        }
    </script>
    <footer class="py-5 bg-black">
        <div class="container">
            <p class="text-center text-white m-0 small">Copyright&nbsp;© ITAxReal [4PDA] 2022</p>
        </div>
    </footer>
    <script src="assets/bootstrap/js/bootstrap.min.js"></script>
</body>

</html>"""
spoiler = """<div><a class="btn btn-primary" data-bs-toggle="collapse" aria-expanded="false" aria-controls="collapse-{i}" href="#collapse-{i}" role="button">{watch}</a>
    <div id="collapse-{i}" class="collapse">
"""
app = """<div class="row">
    <div class="col align-items-center"><img src="{img}" width="32" height="32" /></div>
    <div class="col">
        <p>{name}</p>
    </div>
    <div class="col">
        <p>{ver}</p>
    </div>
    <div class="col"><a href="{qr}">Install</a></div>
</div>
"""
first_row = """<div class="row">
    <div class="col">
        <p>Image</p>
    </div>
    <div class="col">
        <p>Name</p>
    </div>
    <div class="col">
        <p>Version</p>
    </div>
    <div class="col">
        <p>Install</p>
    </div>
</div>
"""

# Uncomment this to update apps when generate site
#print("Updating database...")
#os.system('python3 req.py')
#print("Done\n")

replacings = {
    ('230', '229'): "[GTR3-PRO]",
    ('226', '227'): "[GTR3]",
    ('224', '225'): "[GTS3]",
    ('418', '419'): "[T-REX2]",
    ('241', '242'): "[GTR3-PRO-LE]",
    ('246', '247'): "[GTS4-Mini]",
    ('252',): "[Band7-NFC]",
    ('253', '254'): "[Band7]",
    ('414', '415'): "[Falcon]",
    ('260', '261'): "[MiBand7-NFC]",
    ('262', '263', '264', '265', '266'): "[MiBand7]",
    ('7995648', '7995649'): "[GTS4]",
    ('7930112', '7930113'): "[GTR4]",
}

ru = {}
content = ""
paths = {'RU': None, 'US': None}
for i in os.walk('./'):
    if i[0].endswith('device'):
        country = re.findall("apps_(\w+)_device", i[0])[0]
        paths[country] = i

for country, i in paths.items():
    for file in i[2]:
        if len(sys.argv) == 2:
            if not sys.argv[1] in file:
                continue
        with open(f"{i[0]}/{file}") as f:
            j = json.load(f)
        fname = file.replace('.json', '')
        names = [[k['name'], k["download_url"], k["image"], k["version"]] for k in j['data']]
        for name, url, image, ver in names:
            ffound = False
            for qq, ww in replacings.items():
                if ffound:
                    break
                for ee in qq:
                    if fname == ee:
                        name = ww + ' ' + name
                        ffound = True
                        break
            # if '230' in file or '229' in file:
            #     name = "[GTR3-PRO] " + name
            # elif '226' in file or '227' in file:
            #     name = "[GTR3] " + name
            # elif '224' in file or '225' in file:
            #     name = "[GTS3] " + name
            # elif '418' in file or '419' in file:
            #     name = "[T-REX2] " + name
            # else:
            #     name = "{DEV-" + file[:3] + "} " + name
            if not ffound:
                name = "{DEV-" + fname + "} " + name
            if name not in ru:
                ru[name] = [name, url, image, ver, country]
            elif version.parse(ver) > version.parse(ru[name][3]):
                ru[name] = [name, url, image, ver, country]
apps = {}
for ii, i in enumerate(sorted(ru.values())):
    #print(i[0])
    device, name = i[0].split(' ', 1)
    name = f"{name} ({i[-1]})"
    apps.setdefault(device, spoiler.format(watch=f">>> {device} <<<", i=ii) + first_row)
    #if not os.path.exists(f"site/assets/img/app/{ii + 1}.png"):
    os.system(f"wget {i[2]} -O site/assets/img/app/{ii + 1}.png")
    apps[device] += app.format(img=f"assets/img/app/{ii + 1}.png", name=name, ver=i[3], qr=f"qr.html?app={ii + 1}")
with open("site/index.html", 'w') as f:
    f.write(head)
    f.write('</div></div>'.join(apps.values()) + '</div></div>')
    f.write(foot)


qr = """<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>Install QR</title>
</head>
<body>
    <h1>Ваш QR-Code для установки:</h1><br>
    <script src="assets/qrcode.min.js"></script>

    <div id="qrcode"></div>
    <script type="text/javascript">
        const params = new URLSearchParams(window.location.search);
        var app = '0';
        if (params.has('app')) {
            app = params.get('app');
        }
        var d = {
            '0': 'Error in qr.html: app not found',
{apps}
        };
        if (app in d){
            new QRCode(document.getElementById("qrcode"), d[app]);
        }else{
            new QRCode(document.getElementById("qrcode"), atob(app.replaceAll('_', '=').replaceAll('-', '/').replaceAll('*', '+')));
        }
    </script>
</body>
</html>"""

apps = ""
for ii, i in enumerate(sorted(ru.values())):
    if ii == len(ru.values()) - 1:
        apps += f"            '{ii + 1}': '{i[1].replace('https', 'zpkd1', 1)}'"
    else:
        apps += f"            '{ii + 1}': '{i[1].replace('https', 'zpkd1', 1)}',\n"

with open("site/qr.html", 'w') as f:
    f.write(qr.replace('{apps}', apps))
