const electron = require('electron');
const canable = require('./canable');
const usb = require('usb-detection');
const serial = require('serialport');

const app = electron.app;
const BrowserWindow = electron.BrowserWindow;
const CANport = canable.CANPort;
const hand = require('./can-handler');

usb.startMonitoring();
hand.init_connection();

var glob = require("glob");


// @brief: find serial devices and return list of available ports
async function initCanable()
{
    init_connection();
}
//  var devs = await usb.find();
//  console.log(devs);
//  var canableport = -1;
//  // search for the canable in the usb devices currently connected
//  for (var i = 0; i < devs.length; i++)
//  {
//    if (devs[i].deviceName.indexOf('canable') >= 0)
//    {
//      canableport = devs[i].deviceAddress;
//      break;
//    }
//  }
//  //
//  if (canableport > -1)
//  {
//  }
//
//
//  if (ports.length < 1)
//  {
//    return false;
//  }
//
//  return ports;
//}




function init_connection(){

    platform = process.platform;
    var ports = [];

    if (platform.startsWith('win')){

      for (var i = 0; i<256; i++){
        ports.push(`COM${i + 1}`);
      }
    }
    else if(platform.startsWith('linux') || platform.startsWith('cygwin')){
      ports = glob("/dev/tty[A-Za-z]*");
    }
    else if(platform.startsWith('darwin')){
      ports = glob("/dev/tty.usbmodem*");
    }


    else{
      console.log('Unsupported platform');
    }

//    for (var i = 0; i < ports.length; i++){
//      if (ports[i] !== null){
//        port = ports[i];
//      }
//    }

    console.log(ports);
//      console.log(await CANPort.listSerialPorts());
    // let can = new CANPort(port);
    // can.open();
    // can.setBitRate(125000);
    // can.on('data', console.log);
}

function createWindow()
{
  winder = new BrowserWindow(
    {
      width: 800,
      height: 600,
      webPreferences: {
        nodeIntegration: true
      }
    }
  );
  winder.loadFile('index.html');

}

app.on('session-created', initCanable);
app.on('ready', createWindow);
