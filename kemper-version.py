import config
import requests
import xml.etree.ElementTree as ET
import json


def api(type):
    url = 'https://www.kemper-amps.com/api/update?type=' + type
    return ET.fromstring(requests.get(url, auth=(config.email, config.password)).text)[0].attrib['version']


def find(str):
    file = open(config.debuglog, 'r'); log = file.read()
    key = log[log.rfind(str):].splitlines(); file.close()
    if str == 'session start':
        return key[1]
    else:
        return key[0].split(' ')[1]


data = json.dumps({
    "profiler_latest": api('KPA2'),
    "profiler_installed": find('OS=Release:'),
    "rigmanager_latest": api('RIGMANAGER'),
    "rigmanager_installed": find('session start')
})

print(data)
