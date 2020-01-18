import sys
import os
# import serial
import glob
import threading
import gc
import time
from canard import can
from canard.hw import socketcan

port = None
return_msg = ''

messages = {'0x605': 'volt_id',
'temp_msg': '0x606',
'ocv_msg': '0x607',
'resistance_msg': '0x608',
'error_msg': '0x609'
}


@pytalk_method('getdata')
def getData(self):
    return return_msg


@pytalk_method('findport')
def findPort(self):
    if sys.platform.startswith('win'):
      ports = ['COM%s' % (i + 1) for i in range(256)]
    elif sys.platform.startswith('linux') or sys.platform.startswith('cygwin'):
      ports = glob.glob('/dev/tty[A-Za-z]*')
    elif sys.platform.startswith('darwin'):
      ports = glob.glob('/dev/tty.*')
    else:
      raise EnvironmentError('Unsupported platform')

    for index in ports:
      if index is not None:
        self.port = index


@pytalk_method('run')
def run(self):

  # dev = socketcan.SocketCanDev("can0")
  bus = socketcan.SocketCanDev(findPort(self))

  bus.start()

  while True:
    # print(dev.recv())
    msg = bus.recv()
    msg_start, msg_end = int(_[37], base=16), int(_[64], base=16)
    data = msg[msg_start:msg_end]
    if data in messages.keys():
        self.return_val = (data, messages.get(data))



@pytalk_method('send')
def send(self, msg_data):
    bus = socketcan.SocketCanDev(findPort(self))
    # bus = can.interface.Bus()

    msg = can.Message(arbitration_id=0xc0ffee,
                      data=[0, 25, 0, 1, 3, 1, 4, 1],    #example
                      is_extended_id=True)

    try:
        bus.send(msg)
        print("Message sent")
    except can.CanError:
        print("Message NOT sent")


