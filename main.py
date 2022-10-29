""" kemper-version """

import os
import json
import xml.etree.ElementTree as xml
import base64
import subprocess
import requests

path = os.path.expanduser("~/Documents/Kemper Amps/RigManager/DebugLog.txt")


def auth(key):
    """ Read Rig Manager credentials """
    defaults = ["defaults", "read", "de.RigManager.Kemper Amps", key]
    shell = subprocess.run(defaults, stdout=subprocess.PIPE, check=True).stdout
    return base64.b64decode(shell).decode("utf-8")


def api(latest):
    """ Return latest version """
    url = f"https://www.kemper-amps.com/api/update?type={latest}"
    response = requests.get(
        url, auth=(auth("LoginName64"), auth("LoginPassword64")), timeout=10)
    return xml.fromstring(response.text)[0].attrib["version"]


def find(local):
    """ Return installed version """
    with open(path, "r", encoding="latin-1") as file:
        log = file.read()
        key = log[log.rfind(local):].splitlines()
        file.close()
        if local == "session start":
            return key[1]
        return key[0].split(" ")[1]


if __name__ == "__main__":
    try:
        output = {
            "profiler_latest": api("KPA2"),
            "profiler_installed": find("OS=Release:"),
            "rigmanager_latest": api("RIGMANAGER"),
            "rigmanager_installed": find("session start")
        }

        data = json.dumps(output, indent=2)

        print(data)

    except Exception as e:
        print("Start Rig Manager and Profiler at least once\nError:", e)
