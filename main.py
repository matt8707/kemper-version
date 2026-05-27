""" kemper-version """

import base64
import json
import os
import subprocess
import sys
import urllib.request
import xml.etree.ElementTree as xml

LOG_PATH = os.path.expanduser("~/Documents/Kemper Amps/RigManager/DebugLog.txt")
API_URL = "https://www.kemper-amps.com/api/update?type={}"
USER_AGENT = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:151.0) Gecko/20100101 Firefox/151.0"

def build_auth_header():
    """ Build Basic auth header from Rig Manager stored credentials. """
    def read(key):
        result = subprocess.run(
            ["defaults", "read", "de.RigManager.Kemper Amps", key],
            capture_output=True, check=True,
        )
        return base64.b64decode(result.stdout).decode()

    credentials = f"{read('LoginName64')}:{read('LoginPassword64')}"
    return base64.b64encode(credentials.encode()).decode()


def get_latest_version(update_type, auth_header):
    """ Return the highest Release version from the Kemper API. """
    req = urllib.request.Request(
        API_URL.format(update_type),
        headers={
            "Authorization": f"Basic {auth_header}",
            "User-Agent": USER_AGENT,
        },
    )

    with urllib.request.urlopen(req, timeout=10) as resp:
        root = xml.fromstring(resp.read())

    def version_tuple(version_str):
        return tuple(map(int, version_str.split(".")))

    releases = []
    for item in root.findall("item"):
        if item.attrib.get("type") == "Release":
            try:
                v = item.attrib["version"]
                version_tuple(v)  # validate
                releases.append(v)
            except (ValueError, KeyError):
                continue

    return max(releases, key=version_tuple, default=None)


def get_installed_versions():
    """ Read both installed versions from the Rig Manager debug log. """
    with open(LOG_PATH, encoding="latin-1") as f:
        log = f.read()

    profiler = None

    old_pos = log.rfind("OS=Release:")
    if old_pos != -1:
        profiler = log[old_pos:].splitlines()[0].split(" ")[1]

    new_pos = log.rfind("opened new KPA with serial")
    if new_pos != -1 and new_pos > old_pos:
        line = log[new_pos:].splitlines()[0]
        profiler = line.rsplit("version ", 1)[1].replace("Release: ", "")

    if not profiler:
        raise ValueError("Could not find profiler version in debug log")

    pos = log.rfind("session start")
    rigmanager = log[pos:].splitlines()[1]

    return profiler, rigmanager


if __name__ == "__main__":
    try:
        prof_installed, rig_installed = get_installed_versions()
    except (FileNotFoundError, IndexError) as e:
        print(f"Error reading local logs. Start Rig Manager and Profiler at least once.\nDetails: {e}")
        sys.exit(1)

    try:
        header = build_auth_header()
        prof_latest = get_latest_version("KPA2", header)
        rig_latest = get_latest_version("RIGMANAGER", header)
    except Exception as e:
        print(f"Error fetching latest versions from Kemper API.\nDetails: {e}")
        sys.exit(1)

    def compare(installed, latest):
        """ Build a structured entry for one component. """
        def to_tuple(v):
            try:
                return tuple(map(int, v.split(".")))
            except (ValueError, AttributeError):
                return ()
        return {
            "installed": installed,
            "latest": latest,
            "up_to_date": to_tuple(installed) >= to_tuple(latest),
        }

    print(json.dumps({
        "profiler": compare(prof_installed, prof_latest),
        "rigmanager": compare(rig_installed, rig_latest),
    }, indent=2))
