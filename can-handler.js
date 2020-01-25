let CANPort = require('./canable').CANPort;
const electron = require('electron');
const canable = require('./canable');
const usb = require('usb-detection');
const serial = require('serialport');


var can;
var port;
var glob = require("glob");

var known_messages = {'0x605': 'volt_id',
'0x606': 'temp_msg',
'0x608': 'resistance_msg',
'0x609': 'error_msg'
};

usb.startMonitoring();
hand.init_connection();

function init_tables()
{
    var table = document.getElementById('cell_info_table');
    for (var r = 0, n = 20; r <= n; r++) {
        table.insertRow(r);                                 //Init cell voltage & temp table
        for (var c = 0, m = 2; c <= m; c++) {
            table.rows[r].insertCell(c)
        }
    }
}

function recieve()
{
  while(true)
  {
    var message = can.recv();
    var id = message.id();
    var data = message.data();

    if (known_messages.indexOf(id) >= 0){
        parseMsg(id, data);
    }
    else{
        console.log('message unknown');
    }
  }
}

function send(header, msg_data){
    msg = can.Message(arbitration_id=header, data= msg_data);

//    msg = CANPort.Message(arbitration_id=msg_id, data= msg_data)

    try{
        bus.send(msg);
        console.log("Message sent")
    }
    catch can.CanError{
        console.log("Message NOT sent")
    }
}


function init_connection(){

    port = null;
    platform = process.platform;

    if (platform.startsWith('win')){
        ports = glob("/dev/tty*");
        for(p : ports){
            if(p.indexOf('modem') >= 0){    //Code works 100% on MAC. Untested on windows but should work
                port = p
            }
        }

        //
//        mcu_platform = 0x05e3 //This is a incorrect VID
//
//        port = await usb.find(vid = mcu_platform); //should only be one       //Commented out code won't work unless a VID/ PID for the CANable can be found.
        //console.log(port);


    }
    else if(platform.startsWith('darwin')){ // Mac
        ports = glob("/dev/tty*");
        for(p : ports){
            if(p.indexOf('modem') >= 0){    //Code works 100% on MAC
                port = p
            }
        }
    }
    else{
        console.log('Unsupported platform');
    }

    if(port != null)
    {
        console.log(port);
        console.log(await CANPort.listSerialPorts());
        let can = new CANPort(port);
        can.open();
        can.setBitRate(125000);
        can.on('data', console.log);
        console.log("Success");
    }
    else{
        console.log("fail");
    }
}

module.exports = {
  init_connection,
};
