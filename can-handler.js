//const SerialPort = require('serialport')   INCL. in CANPort
let CANPort = require('./index').CANPort;

var can;
var port;
var glob = require("glob")

var known_messages = {'0x605': 'volt_id',
'0x606': 'temp_msg',
'0x608': 'resistance_msg',
'0x609': 'error_msg'
}

function recieve(){
    while(true){
        var message = can.recv();
        var id = message.id();
        var data = message.data();

        if (known_messages.indexOf(id) >= 0){
            return (id, data);

        }
        else{
            console.log('message unknown');
        }
    }
}



function init_connection(){

        platform = process.platform;

        if platform.startsWith('win'){
            ports = ['COM%s' % (i + 1) for i in range(256)];
        }
        else if platform.startsWith('linux') or platform.startsWith('cygwin'){
            ports = glob("/dev/tty[A-Za-z]*")
        }
        else if platform.startsWith('darwin'){
            ports = glob("/dev/tty.*")
        }
        else{
            console.log('Unsupported platform');
        }

        for (var index in ports){
            if (index !== null){
                port = index;
            }
        }


//      console.log(await CANPort.listSerialPorts());
        let can = new CANPort(port);
        can.open();
        can.setBitRate(125000);
        can.on('data', console.log);
}

}
