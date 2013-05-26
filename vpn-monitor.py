"""vpn-monitor 0.1

Usage:
  vpn-monitor.py --vpn <vpn> --apps <apps>
  vpn-monitor.py (-h | --help)
  vpn-monitor.py --version

Options:
  -h --help     Show this screen.
  --version     Show version.
  --vpn=<vpn>   Name of vpn
  --apps=<apps> Name of apps that may run iff the vpn is running.
"""

from time import sleep
from subprocess import check_output

from appscript import app
from docopt import docopt

class VpnMonitor(object):
  def __init__(self, vpn, apps):
    self.vpn = vpn
    self.apps = apps

  def run(self):
    try:
      self.main_loop()
    except KeyboardInterrupt:
      self.quit_apps()
      raise
    except:
      self.quit_apps()
      raise

  def main_loop(self):
    while True:
      vpn = app('System Events').network_preferences.services[self.vpn]
      vpn_connected = vpn.current_configuration.connected()

      if not vpn_connected:
        self.quit_apps()

        if self.is_wifi_connected():
          vpn.connect()
          sleep(30)
      else:
        self.run_apps()
      
      sleep(0.1)

  def is_wifi_connected(self):
    return 'Wi-Fi Power (en1): On' in check_output(['networksetup', '-getairportpower', 'en1'])

  def quit_apps(self):
    for name in self.apps:
      cur = app(name)
      if cur.isrunning():
        cur.quit()

  def run_apps(self):
    for name in self.apps:
      cur = app(name)
      if not cur.isrunning():
        cur.run()
      
if __name__ == '__main__':
    arguments = docopt(__doc__, version='vpn-monitor 0.1')

    vpn_monitor = VpnMonitor(arguments['--vpn'], arguments['--apps'].split(','))
    vpn_monitor.run()
