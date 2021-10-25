import xml.etree.ElementTree as xml
import requests as req
import config as user

def api(latest):
    """Return latest version"""
    url = 'https://www.kemper-amps.com/api/update?type=' + latest
    return xml.fromstring(req.get(url, auth=(user.email, user.password)).text)[0].attrib['version']

def find(local):
    """Return installed version"""
    with open(user.debuglog, 'r', encoding='latin-1') as file:
        log = file.read()
    key = log[log.rfind(local):].splitlines()
    file.close()
    return key[1] if local == 'session start' else key[0].split(' ')[1]

print(f'{{"profiler_latest": "{api("KPA2")}", "profiler_installed": "{find("OS=Release:")}", \
"rigmanager_latest": "{api("RIGMANAGER")}", "rigmanager_installed": "{find("session start")}"}}')
