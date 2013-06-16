"""vpn-monitor 0.1

Usage:
  vpn-monitor.py --vpn=VPN --wifi=WIFI [--app=APP, --app=APP, ...] [(-q | --quiet)]
  vpn-monitor.py (-h | --help)
  vpn-monitor.py --version

Options:
  --vpn=VPN             Name of VPN
  --wifi=WIFI           Name of Wifi interface.
  --app=APP             Name of APP that should run iff the VPN is connected
  -h --help             Show this screen
  -v --version          Show version
  -q --quiet            Quiet mode
"""
import sys
import subprocess
import logging
import logging.config

from time import sleep
from subprocess import check_output

from appscript import app
from docopt import docopt

class VpnMonitor(object):
  def __init__(self, vpn_name, wifi_interface, app_names):
    self.vpn_name = vpn_name
    self.apps = [(name, app(name)) for name in app_names]
    self.wifi_interface = wifi_interface

  def run(self):
    try:
      self.main_loop()
    except KeyboardInterrupt:
      self.quit_apps()
    except:
      self.quit_apps()
      raise

  def main_loop(self):
    while True:
      if not self.is_vpn_connected():
        logging.info("VPN %s is disconnected", self.vpn_name)
        self.quit_apps()

        if self.is_wifi_connected():
          logging.info("Connecting to VPN %s ...", self.vpn_name)
          self.vpn().connect()

          while not self.is_vpn_connected():
            sys.stdout.write('.')
            sys.stdout.flush()
            sleep(0.5)
          print ''

          logging.info("Connected to VPN %s", self.vpn_name)
      else:
        self.run_apps()
      
      sleep(0.1)

  def vpn(self):
    return app('System Events').network_preferences.services[self.vpn_name]

  def is_vpn_connected(self):
    return self.vpn().current_configuration.connected()

  def is_wifi_connected(self):
    return ("Wi-Fi Power (%s): On" % self.wifi_interface) in check_output(["networksetup", "-getairportpower", self.wifi_interface])

  def quit_apps(self):
    for name, cur in self.apps:
      if cur.isrunning():
      logging.info("Quiting app %s", name)
      subprocess.call(["killall", "-9", name])

  def run_apps(self):
    for name, cur in self.apps:
      if not cur.isrunning():
        logging.info("Starting app %s", name)
        cur.run()

# Configure logging
DEBUG_FORMAT = "%(asctime)s: %(message)s"
LOG_CONFIG = {
  'version': 1,
  'formatters': {
    'debug': { 'format':DEBUG_FORMAT },
  },
  'handlers': {
    'console': {
      'class': 'logging.StreamHandler',
      'formatter': 'debug',
      'level': logging.DEBUG,
    },
  },
  'root': { 'handlers': ('console', ), 'level': 'DEBUG' }
}
logging.config.dictConfig(LOG_CONFIG)

if __name__ == '__main__':
    arguments = docopt(__doc__, version='vpn-monitor 0.1')
    if arguments['--quiet']:
      logging.disable(logging.INFO)

    vpn_monitor = VpnMonitor(arguments["--vpn"], arguments["--wifi"], arguments["--app"])
    vpn_monitor.run()
