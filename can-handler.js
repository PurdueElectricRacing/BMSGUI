//const SerialPort = require('serialport')   INCL. in CANPort
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

function recieve()
{
  while(true)
  {
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

        mcu_platform = 0x05e3 //This is the vendor ID for the CANable.

        port = await usb.find(vid = mcu_platform); //should only be one
        //console.log(port);
    }
    else if(platform.startsWith('darwin')){ // Mac
      port = glob("/dev/tty.usbmodem*"); //only should be one.
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
