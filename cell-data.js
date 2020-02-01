cells = {};
temps = {};

function parseMsg(header, data) {
  switch (header)
  {
    case "volt_id":

        let row = data[1];
        const table_access = document.getElementById("cell_info_table").rows[row].cells;    // accesses HTML table
        const volt_reading = (data[3] + data[2] << 8);

        let rstring = '';
        rstring.concat('Row ' + row + ': ' + volt_reading + 'V');

        table_access[0].innerHTML = rstring;            // updates value in html table
        break;

    case "temp_msg":
        row = data[1];
        const single_row_access = document.getElementById("cell_info_table").rows[row].cells;
        const temp_reading = (data[3] + data[2] << 8);

        rstring = '';
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
            if(byte == 0)
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
    document.getElementById('cell_delta').innerHTML = delta.toString();
    document.getElementById('total_voltage').innerHTML = tot_voltage.toString();

    const charge_percent = 1 - (((4.2 - (tot_voltage / 21)) / 10) / .17);   //Calculates battery %
    document.getElementById('charge_percent').innerHTML = charge_percent.toString();

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

