const pytalk = require('pytalk');
const electron = require('electron');
const app = electron.app;
const BrowserWindow = electron.BrowserWindow;

var tester = pytalk.worker('./python_interface/communication.py');
var test = tester.method('test');

test('infinite loop test', (err) => {
  
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

app.on('ready', createWindow);


// test('this some garbage yo', (err, retgarbage) => 
// {
//   console.log(retgarbage);
// });