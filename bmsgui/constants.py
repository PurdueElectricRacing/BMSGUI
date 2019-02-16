headerCellh = ['Voltage (V)', 'Date']
headerCellv = 12    # number of total cells
headerTemph = ['Temperature (\xb0C)', 'Date']
headerTempv = 4     # number of total thermistors
headerModh = ['Value', 'Date']
headerModv = ['State of Charge', 'Pack Voltage', 'Pack Current']
dbModID = ['soc', 'pvol', 'pcur']
headerCANh = ['Length', 'Byte0', 'Byte1', 'Byte2', 'Byte3', 'Byte4', 'Byte5', 'Byte6', 'Byte7', 'Date']
headerCANv = ['0x605', '0x606', '0x607', '0x608', '0x609', '0x60A', '0x60B', '0x60C']   # CAN data to display on GUI
# volt, temp, packv, packi, error, macro, sdc, sdc
labelStates = ['State: disconnect', 'State: idle', 'State: log', 'State: live']
ignoreDec = ['update']

errorDBopen = """Unable to establish a database connection.\n
                This example needs SQLite support. 
                Please read the Qt SQL driver documentation for information how to build it.\n\n
                Click Cancel to exit."""
errorDBexist = """Database already exists"""

slaveNum = 2
cellsPERslave = 6
dataPERmsg = 3
DEBUG = 1
PRINT = 0
DISCONNECT = 0
IDLE = 1
LOG = 2
LIVE = 3
CLOSE = -1

def dec(func):
    def wrapper(*args):
        if (func.__name__ not in ignoreDec) and (func.__name__[0] != '_'):
            global PRINT
            if PRINT:
                print "0 - " + func.__name__
            func(*args)
            if PRINT:
                print "1 - " + func.__name__
        else:
            func(*args)
    return wrapper

def fdec(d):
    def wrapper(cls):
        for attr in cls.__dict__:
            if callable(getattr(cls, attr)):
                setattr(cls, attr, d(getattr(cls, attr)))
        return cls
    return wrapper