"""vpn-monitor 0.1

Usage:
  vpn-monitor.py --vpn <vpn> --apps <apps>
  vpn-monitor.py (-h | --help)
  vpn-monitor.py --version

Options:
  -h --help     Show this screen.
  --version     Show version.
  --vpn=<vpn>   Name of VPN.
  --apps=<apps> Comma separated list of apps that should run iff the VPN is connected.
"""
import sys
import logging
import logging.config

from time import sleep
from subprocess import check_output

from appscript import app
from docopt import docopt

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

class VpnMonitor(object):
  def __init__(self, vpn_name, app_names):
    self.vpn_name = vpn_name
    self.apps = [(name, app(name)) for name in app_names]

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
    return 'Wi-Fi Power (en1): On' in check_output(['networksetup', '-getairportpower', 'en1'])

  def quit_apps(self):
    for name, cur in self.apps:
      if cur.isrunning():
        logging.info("Quiting app %s", name)
        cur.quit()

  def run_apps(self):
    for name, cur in self.apps:
      if not cur.isrunning():
        logging.info("Starting app %s", name)
        cur.run()
      
if __name__ == '__main__':
    arguments = docopt(__doc__, version='vpn-monitor 0.1')

    vpn_monitor = VpnMonitor(arguments['--vpn'], arguments['--apps'].split(','))
    vpn_monitor.run()
