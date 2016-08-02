#!/usr/bin/python2
import sys
import os
import time
import pty
from pyotp import totp

config = {
    "username": '',
    "password": '',
    "google_secret": ""
}

def openvpn_wrapper():
  try:
    ( child_pid, fd ) = pty.fork()
  except OSError as e:
    print str(e)

  if child_pid == 0:
    # print "In Child Process: PID# %s" % os.getpid()
    sys.stdout.flush()
    try:
      os.execlp("openvpn","OpenVPN",'--config', 'client.ovpn')
    except:
      print "Cannot spawn execlp..."
  else:
    if not isinstance(config, dict):
      raise TypeError('config must be dictionary!')
    for entry in config:
      if not config[entry]:
        raise RuntimeError('Missing config data: %s' % entry)
    # print "In Parent Process: PID# %s" % os.getpid()
    print os.read(fd, 1000)
    otp_gen = totp.TOTP(s=config['google_secret'])
    try:
      os.write(fd,config['username']+'\n')
      print os.read(fd, 1000)
      time.sleep(2)
      os.write(fd,config['password']+'\n')
      print os.read(fd, 1000)
      time.sleep(2)
      otp_code = otp_gen.now()
      os.write(fd,str(otp_code)+'\n')
      print os.read(fd, 1000)
      time.sleep(2)
    except KeyError as e:
      raise KeyError("Missing config parameter! %s"%e.message)
    while True:
      print os.read(fd, 10000)


if __name__ == "__main__":
    openvpn_wrapper()