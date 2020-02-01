import {init_connection} from "./can-handler";
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

const glob = require("glob");


// @brief: find serial devices and return list of available ports
async function initCanable()
{
    init_connection();
}

function createWindow()
{
    let winder = new BrowserWindow(
        {
            width: 800,
            height: 600,
            webPreferences: {
                nodeIntegration: true
            }
        }
    );
  winder.loadFile('./layout/production/index.html');

}

app.on('session-created', initCanable);
app.on('ready', createWindow);