# kemper-version

Finds the installed and latest versions of [Rig Manager](https://www.kemper-amps.com/rig-manager) and [PROFILER OS](https://www.kemper-amps.com/products/profiler/line-up)

```json
{
  "profiler_latest": "8.7.10.38833",
  "profiler_installed": "8.5.6.30271",
  "rigmanager_latest": "3.2.76",
  "rigmanager_installed": "3.2.43"
}
```

## Scenario

You realize that you haven't fired up rig manager in a while and a new update is available. You update, but are met with the error that the current version of rig manager is too new to communicate with the profiler. You have to find a usb-stick and go through the tedious process of manually updating the profiler...

---

### Home Assistant Example

```yaml
sensor:
  - platform: command_line
    name: updates_kemper
    command: >
      ssh -q -o StrictHostKeyChecking=no -i /config/.ssh/id_rsa matte@192.168.1.109 /opt/homebrew/bin/python3 Developer/kemper-version/main.py || \
      echo '{"profiler_latest": "", "profiler_installed": "", "rigmanager_latest": "", "rigmanager_installed": ""}'
    value_template: >
      {{ 'on' if value_json.profiler_installed != value_json.profiler_latest or
      value_json.rigmanager_latest != value_json.rigmanager_installed else 'off' }}
    json_attributes:
      - profiler_latest
      - profiler_installed
      - rigmanager_latest
      - rigmanager_installed
    scan_interval: 86400
```
