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

    platform = process.platform;
    var found = false;
    if (platform.startsWith('win')){

//      for (var i = 0; i<256; i++){
//        ports.push(`COM${i + 1}`);
//      }
        mcu_platform = '1155' //This is the vendor ID for the STM chip on the CANable. AKA this says that the device plugged in has 'a' STM chip. If a query with this doesn't find anything, there is likely a proprietary VID for the CANable that I can't find at this time. PID will also work by search.
        var devs = await usb.find(vid = mcu_platform);
        console.log(devs);
        // search for the canable in the usb devices currently connected
        for (var i = 0; i < devs.length; i++)
        {
            found = true;
            port = devs[i];
        }

        if(!found){
            return false;
        }
    }
    else if(platform.startsWith('darwin')){
      port = glob("/dev/tty.usbmodem*"); //only should be one.
    }
    //  else if(platform.startsWith('linux') || platform.startsWith('cygwin')){
//      ports = glob("/dev/tty[A-Za-z]*");
//    }
    else{
      console.log('Unsupported platform. (Get a Mac)');
    }

//    for (var i = 0; i < ports.length; i++){
//      if (ports[i] !== null){
//        port = ports[i];
//      }
//    }

    console.log(port);
    console.log(await CANPort.listSerialPorts());
    let can = new CANPort(port);
    can.open();
    can.setBitRate(125000);
    can.on('data', console.log);
    console.log("Success");
}

module.exports = {
  init_connection,
};
