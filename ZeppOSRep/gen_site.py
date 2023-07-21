import json


dbfile = "zepprep.json"

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
    <script src="assets/jquery-3.7.0.slim.min.js"></script>
    <script>  
        function ReLoadImages(){
            $('img[data-lazysrc]').each( function(){
                //* set the img src from data-src
                $( this ).attr( 'src', $( this ).attr( 'data-lazysrc' ) );
                }
            );
        }

        document.addEventListener('readystatechange', event => {
            if (event.target.readyState === "interactive") {  //or at "complete" if you want it to execute in the most last state of window.
                ReLoadImages();
            }
        });
    </script>
</body>

</html>"""
spoiler = """<div><a class="btn btn-primary" data-bs-toggle="collapse" aria-expanded="false" aria-controls="collapse-{i}" href="#collapse-{i}" role="button">{watch}</a>
    <div id="collapse-{i}" class="collapse">
"""
app = """<div class="row">
    <div class="col align-items-center"><img data-lazysrc="{img}" width="32" height="32" /></div>
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

# Uncomment this to update apps when generate site
#print("Updating database...")
#os.system('python3 req.py')

apps = {}
dwnlnks = ""
with open(dbfile) as f:
    jrep = json.load(f)
for i, device in enumerate(jrep):
    apps.setdefault(device, spoiler.format(watch=f">>> {device} <<<", i=i) + first_row)
    dapps = [[k['name'], k["download_url"], k["image"], k["version"], k['fetchcntr'], appid] for appid, k in jrep[device].items()]
    for dapp in dapps:
        apps[device] += app.format(img=dapp[2], name=f"{dapp[0]} ({dapp[4]})", ver=dapp[3], qr=f"qr.html?app={device+dapp[-1]}")
        dwnlnks += f"            '{device + dapp[-1]}': '{dapp[1].replace('https', 'zpkd1', 1)}',\n"
dwnlnks += f"            'null': 'null'"

with open("index.html", 'w') as f:
    f.write(head)
    f.write('</div></div>'.join(apps.values()) + '</div></div>')
    f.write(foot)
with open("qr.html", 'w') as f:
    f.write(qr.replace('{apps}', dwnlnks))
