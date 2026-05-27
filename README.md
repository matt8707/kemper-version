# kemper-version

Compares installed and latest versions of [Rig Manager](https://www.kemper-amps.com/rig-manager) and PROFILER OS. Installed versions are parsed from the Rig Manager debug log and latest versions are fetched from the Kemper update API using credentials stored in macOS defaults.

Requires Rig Manager to have been launched at least once.

## Scenario

You realize that you haven't fired up rig manager in a while and a new update is available. You update, but are met with the error that the current version of rig manager is too new to communicate with the profiler. You have to find a usb-stick and go through the tedious process of manually updating the profiler... Use this script to automate version checks so you don't fall too far behind.

## Usage

No dependencies.

```sh
python3 main.py
```

## Output

Returns JSON.

```json
{
  "profiler": {
    "installed": "13.0.5.61298",
    "latest": "14.1.2.66277",
    "up_to_date": false
  },
  "rigmanager": {
    "installed": "3.10.13",
    "latest": "4.1.20",
    "up_to_date": false
  }
}
```
