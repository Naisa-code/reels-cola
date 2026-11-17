#!/usr/bin/env python3
# Naisa · recoge del repo público naisa-code/reels-cola los reels nuevos y los mete en la cola del publicador.
# Lo lanza el cron cada hora (min 50). No publica nada: eso lo hace publicar.py a su hora.
import json, os, shutil, time, urllib.request
BASE = '/opt/naisa-publicador'
RAW = 'https://raw.githubusercontent.com/naisa-code/reels-cola/main/'
def baja(ruta, destino=None):
    with urllib.request.urlopen(RAW + ruta + '?t=%d' % time.time(), timeout=120) as r:
        datos = r.read()
    if destino:
        tmp = destino + '.part'; open(tmp, 'wb').write(datos); os.replace(tmp, destino)
    return datos
nuevos = json.loads(baja('cola.json'))
p = os.path.join(BASE, 'cola.json'); cola = json.load(open(p))
ya = {c.get('archivo') for c in cola}
from datetime import datetime
from zoneinfo import ZoneInfo
ahora = datetime.now(ZoneInfo('Europe/Madrid')).strftime('%Y-%m-%d %H:%M')
añadidos = []
for e in nuevos:
    if e['archivo'] in ya or e['publicar'] < ahora: continue
    destino = os.path.join(BASE, 'videos', e['archivo'])
    if not os.path.exists(destino): baja('videos/' + e['archivo'], destino)
    if os.path.getsize(destino) < 100000: print('vídeo raro', e['archivo']); continue
    añadidos.append({k: e[k] for k in ('video', 'publicar', 'archivo', 'caption', 'primer_comentario')})
if añadidos:
    shutil.copy(p, p + '.bak-' + time.strftime('%Y%m%d%H%M%S'))
    cola += añadidos; tmp = p + '.part'
    json.dump(cola, open(tmp, 'w'), ensure_ascii=False, indent=1); os.replace(tmp, p)
for a in añadidos: print(time.strftime('%F %T'), 'en cola', a['publicar'], a['video'])
