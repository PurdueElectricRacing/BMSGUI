headerCellh = ['Voltage (V)', 'Internal Resistance (mOhm)', 'Date']
headerCellv = 12
headerTemph = ['Temperature (\xb0C)', 'Date']
headerTempv = ['Site 0', 'Site 1', 'Site 2']
headerCANh = ['Length', 'Byte0', 'Byte1', 'Byte2', 'Byte3', 'Byte4', 'Byte5', 'Byte6', 'Byte7', 'Date']
headerCANv = ['0x605', '0x606', '0x607', '0x7E0']
labelStates = ['State: disconnect', 'State: idle', 'State: log', 'State: live']
ignoreDec = ['update']

errorDBopen = """Unable to establish a database connection.\n
                This example needs SQLite support. 
                Please read the Qt SQL driver documentation for information how to build it.\n\n
                Click Cancel to exit."""
errorDBexist = """Database already exists"""

portNumber = 1090
DISCONNECT = 0
IDLE = 1
LOG = 2
LIVE = 3
CLOSE = -1

def dec(func):
    def wrapper(*args):
        if (func.__name__ not in ignoreDec) and (func.__name__[0] != '_'):
            print "0 - " + func.__name__
            func(*args)
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