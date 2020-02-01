let CANPort = require('./canable').CANPort;
const electron = require('electron');
const canable = require('./canable');
const serial = require('serialport');


let can;
let port;
const glob = require("glob");

const known_messages = {
    '0x605': 'volt_id',
    '0x606': 'temp_msg',
    '0x608': 'resistance_msg',
    '0x609': 'error_msg'
};

usb.startMonitoring();
init_connection();

function init_tables()
{
    const table = document.getElementById('cell_info_table');
    let r = 0, n = 20;
    for (; r <= n; r++) {
        table.insertRow(r);                                 //Init cell voltage & temp table
        let c = 0, m = 2;
        for (; c <= m; c++) {
            table.rows[r].insertCell(c)
        }
    }
}

function receive()
{
  while(1)
  {
      const message = can.recv();
      const id = message.id();
      const data = message.data();  //Is recieved as an array through the canable pkg

    if (known_messages.indexOf(id) >= 0){
        parseMsg(id, data);

        const table = document.getElementById('can_message_bank');
        table.insertRow(0);
        // table.insertRow(error_msg_names[byte]);

        const single_row_access = document.getElementById("cell_info_table").rows[row].cells;

        const i = 0;
        for(let byte in data)
        {
            single_row_access.insertCell(i);
            single_row_access[i].innerHTML = byte;
        }
    }
    else{
        console.log('message unknown');
    }
  }
}

function send_message()
{
    const id = document.getElementById("frame_id").value;
    const msg_data = document.getElementById("message").value;
    const e_id = document.getElementById("extended_id").value;


//    id = "frame_id"
//    id = "length"
//    id = "message"
//    id = "extended_id"
    let msg = can.Message(arbitration_id = id, data = msg_data, is_extended_id = e_id);


    try{
        can.send(msg);
        console.log("Message sent")
    }
    catch {
        console.log("Message NOT sent")
    }
}


async function init_connection() {

    port = null;
    let platform = process.platform;

    if (platform.startsWith('win')) {
        ports = glob("/dev/tty*");
        for (let p in ports) {
            if (p.indexOf('modem') >= 0) {    //Code works 100% on MAC. Untested on windows but should work
                port = p
            }
        }

        //
//        mcu_platform = 0x05e3 //This is a incorrect VID
//
//        port = await usb.find(vid = mcu_platform); //should only be one       //Commented out code won't work unless a VID/ PID for the CANable can be found.
        //console.log(port);
    } else let ports;
    let ports;
    if (platform.startsWith('darwin')) { // Mac
        ports = glob("/dev/tty*");
        for (let p in ports) {
            if (p.indexOf('modem') >= 0) {    //Code works 100% on MAC
                port = p
            }
        }
    } else {
        console.log('Unsupported platform');
    }

    if (port != null) {
        console.log(port);
        console.log(await CANPort.listSerialPorts());
        let can = new CANPort(port);
        can.open();
        can.setBitRate(125000);
        can.on('data', console.log);
        console.log("Success");
    } else {
        console.log("fail");
    }

    init_tables();
    receive();
}

module.exports = {
  init_connection,
};
