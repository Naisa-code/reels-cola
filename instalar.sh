#!/bin/bash
# Una sola vez en el servidor: instala recoger.py y lo añade al cron (min 50 de cada hora). No toca nada más.
set -e
curl -fsSL https://raw.githubusercontent.com/naisa-code/reels-cola/main/recoger.py -o /opt/naisa-publicador/recoger.py
( crontab -l 2>/dev/null | grep -v 'recoger.py'; echo '50 * * * * cd /opt/naisa-publicador && /usr/bin/python3 recoger.py >> recoger.log 2>&1' ) | crontab -
cd /opt/naisa-publicador && python3 recoger.py
echo "--- cron:"; crontab -l | grep naisa-publicador
echo "--- cola (últimas):"; python3 -c "import json;[print(c['publicar'],c['video']) for c in json.load(open('cola.json'))[-14:]]"
