import sys
import os
import serial
import glob
# import threading
# import gc
# import time
# from canard import can
# from canard.hw import socketcan
from socketIO_client import SocketIO, LoggingNamespace
emitSocket = SocketIO('localhost', 80085, LoggingNamespace)

# port = None
return_msg = 0

messages = {'0x605': 'volt_id',
'0x606': 'temp_msg',
'0x608': 'resistance_msg',
'0x609': 'error_msg'
}


def getData():
    return return_msg


# @pytalk_method('findport')
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
  # bus = socketcan.SocketCanDev(findPort())

  # bus.start()
  print('huh');
  while True:
    print(dev.recv())
    msg = bus.recv()
    msg_start, msg_end = int(_[37], base=16), int(_[64], base=16)
    data = msg[msg_start:msg_end]
    # if data in messages.keys():
        # return_val = (data, messages.get(data))
    # return_msg = 'help'
    # pytalk_emit('datarcv', {'help': 'jfdhsjafhdsl'})
    emitSocket.emit('data', 'hello');

    # getData()



# @pytalk_method('send')
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


# @pytalk_method('test')
# def whatever(garbage):
#   while True:
#     print(garbage);
    
