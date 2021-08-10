# kemper-version

https://www.kemper-amps.com/products/profiler/line-up
https://www.kemper-amps.com/rig-manager

This project finds the installed versions from local logs, checks if updates are available through an undocumented api and outputs json.


```json
{
  "profiler_latest": "8.5.8.30570",
  "profiler_installed": "8.5.6.30271",
  "rigmanager_latest": "3.2.43",
  "rigmanager_installed": "3.2.43"
}
```

***Scenario***
You realize that you haven't fired up rig manager in a while and a new update is available. You update it, but when you try to update your profiler you're met with an error. You have to find a usb-stick and go through the tedious process of manually updating the profiler, because the current version of rig manager is too new to communicate with the profiler...

---

***Home Assistant Example***

```yaml
sensor:
  - platform: command_line
    name: kemper_version
    command: >
      ssh -o StrictHostKeyChecking=no -i /config/.ssh/id_rsa matte@192.168.1.8 '/usr/local/bin/python3 /Users/matte/kemper-version/kemper-version.py'
    value_template: >
      {{ value_json.profiler_installed == value_json.profiler_latest and 
      value_json.rigmanager_latest == value_json.rigmanager_installed }}
    json_attributes:
      - profiler_latest
      - profiler_installed
      - rigmanager_latest
      - rigmanager_installed
    scan_interval: 86400
```

![example](example.png)
