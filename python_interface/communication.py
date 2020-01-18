import sys
import os
# import serial
import glob
import threading
import gc
import time
from canard import can
from canard.hw import socketcan
import pytalk


port = None
return_msg = ''

messages = {'0x605': 'volt_id',
'0x606': 'temp_msg',
'0x607': 'ocv_msg',
'0x608': 'resistance_msg',
'0x609': 'error_msg'
}


@pytalk_emit('datarcv', 'getdata')
def getData():
    return return_msg


@pytalk_method('findport')
def findPort():
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
        port = index


@pytalk_method('run')
def run():

  # dev = socketcan.SocketCanDev("can0")
  bus = socketcan.SocketCanDev(findPort())

  bus.start()

  while True:
    # print(dev.recv())
    msg = bus.recv()
    msg_start, msg_end = int(_[37], base=16), int(_[64], base=16)
    data = msg[msg_start:msg_end]
    if data in messages.keys():
        return_val = (data, messages.get(data))
        getData()



@pytalk_method('send')
def send(msg_id, msg_data):
    bus = socketcan.SocketCanDev(findPort())
    # bus = can.interface.Bus()

    msg = can.Message(arbitration_id=msg_id,
                      data= msg_data,    #example
                             )

    try:
        bus.send(msg)
        print("Message sent")
    except can.CanError:
        print("Message NOT sent")


