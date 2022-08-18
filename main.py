""" kemper-version """

import json
import xml.etree.ElementTree as xml
import requests
import config

def api(latest):
    """
    Return latest version
    """
    try:
        url = f"https://www.kemper-amps.com/api/update?type={latest}"
        response = requests.get(url, auth=(config.EMAIL, config.PASSWORD))
        xml_path = xml.fromstring(response.text)[0].attrib["version"]
        return xml_path
    except xml.ParseError:
        return "ParseError"


def find(local):
    """
    Return installed version
    """
    try:
        with open(config.DEBUGLOG, "r", encoding="latin-1") as file:
            log = file.read()
            key = log[log.rfind(local):].splitlines()
            file.close()
            if local == "session start":
                return key[1]
            if local == key[0].split(" ")[0]:
                return key[0].split(" ")[1]
            return "Not found"
    except FileNotFoundError:
        return "FileNotFoundError"
    except IndexError:
        return "IndexError"


output = {
    "profiler_latest": api("KPA2"),
    "profiler_installed": find("OS=Release:"),
    "rigmanager_latest": api("RIGMANAGER"),
    "rigmanager_installed": find("session start")
}

data = json.dumps(output, indent=2)

print(data)
