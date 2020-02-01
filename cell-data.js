cells = {};
temps = {};
let startTime = new Date();
let prev_volts = 0;
let prev_delta = 0;
let prev_charge = 0;

function parseMsg(header, data) {
  let row = data[1];
  let rstring = '';
  switch (header)
  {
    case "volt_id":

        const table_access = document.getElementById("cell_info_table").rows[row].cells;    // accesses HTML table
        const volt_reading = (data[3] + data[2] << 8);

        rstring.concat('Row ' + row + ': ' + volt_reading + 'V');

        table_access[0].innerHTML = rstring;            // updates value in html table
        break;

    case "temp_msg":
        const single_row_access = document.getElementById("cell_info_table").rows[row].cells;
        const temp_reading = (data[3] + data[2] << 8);

        rstring.concat(temp_reading + ' degrees freedomheit');
        single_row_access[1].innerHTML = rstring;
        get_total_voltage();
        break;

    case "error_msg":
        const table = document.getElementById('error_msg_table');
        let error_msg_names = ['COC', 'DOC', 'Overvolt', 'Undervolt', 'Overtemp', 'Undertemp'];
        for (i=0; i<table.length; i++)
        {
            table.deleteRow(i) //Clear all rows b4 repopulation
        }

        for (const byte in data){
            if(byte == 0 && byte <= 5)
            {
             table.insertRow(error_msg_names[byte]);
            }
        }

        break;

    default:
        return "Message not recognised. Something is really fucked up because we should've already checked for this.";
  }
}

function get_total_voltage()
{
    let delta_update = false;
    let endTime = new Date();
    let timeDiff = endTime - startTime; //in ms
    // strip the ms
    timeDiff /= 60000;
    if(timeDiff >= 10)
    {
        delta_update = true;
        startTime = new Date()
    }
    let tot_voltage = 0;
    let largest = 0;
    let smallest = 0;
    for (var series_voltage in cells)
    {
        tot_voltage += series_voltage;
        if(series_voltage > largest)
        {
            largest = series_voltage;
        }
        if(smallest == 0)
        {
            smallest = series_voltage
        }
        else if (series_voltage < series_voltage)
        {
            smallest = series_voltage;
        }
    }
    const delta = largest-smallest;
    const charge_percent = 1 - (((4.2 - (tot_voltage / 21)) / 10) / .17);   //Calculates battery %

    document.getElementById('cell_delta').innerHTML = delta.toString();
    document.getElementById('total_voltage').innerHTML = tot_voltage.toString();
    document.getElementById('charge_percent').innerHTML = charge_percent.toString();


    if(delta_update)
    {
        const total_delta_span = delta-prev_delta;
        prev_delta = delta;
        document.getElementById('cell_delta_span').innerHTML = total_delta_span.toString();

        const tot_voltage_span = tot_voltage-prev_volts;
        prev_volts = tot_voltage;
        document.getElementById('total_voltage_span').innerHTML = tot_voltage_span.toString();

        const charge_percent_delta = charge_percent-prev_charge;
        prev_charge = charge_percent;
        document.getElementById('charge_percent_delta').innerHTML = charge_percent_delta.toString();
    }

    //Full = 4.2V
    // cutoff @ 2.5V
}


// ERROR MSGS::: ALL ARE ACTIVE LOW
//0: COC
//1: DOC
//2: Overvolt
//3: Undervolt
//4: Overtemp
//5: Undertemp
//6: reserved
//7: reserved

