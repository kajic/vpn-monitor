from time import sleep
from subprocess import check_output

from appscript import app

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
      vpn = app('System Events').network_preferences.services[VPN]
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
      
VPN = 'IPredator'
APPS = ['Transmission', 'uTorrent']

vpn_monitor = VpnMonitor(VPN, APPS)
vpn_monitor.run()
