Monitor your vpn connection on OSX, and run/quit a set of applications based on the vpn status.

Install requirements
--------------------

```bash
pip install -r requirements.txt
```

Usage
-----

```
Usage:
  vpn-monitor.py --vpn=VPN [--app=APP, --app=APP, ...] [(-q | --quiet)]
  vpn-monitor.py (-h | --help)
  vpn-monitor.py --version

Options:
  --vpn=VPN             Name of VPN.
  --app=APP             Name of APP that should run iff the VPN is connected.
  -h --help             Show this screen.
  -v --version          Show version.
  -q --quiet            Quiet mode.
```
