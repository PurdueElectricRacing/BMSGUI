const pytalk = require('pytalk');
const electron = require('electron');
const app = electron.app;
const BrowserWindow = electron.BrowserWindow;
const http = require('http');

http.createServer().listen(8008, 'localhost');

var worker = pytalk.worker('./python_interface/communication.py');
// var test = worker.method('test');
var run = worker.method('run');



worker.on('datarcv', (err, args) => 
{
  console.log(args);
});


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

// app.on('ready', createWindow);
run((err, ret) => {
  console.log('running');
});

// test('this some garbage yo', (err, retgarbage) => 
// {
//   console.log(retgarbage);
// });