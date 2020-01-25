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
