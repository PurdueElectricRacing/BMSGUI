cells = {};
temps = {};

function parseMsg(header, data) {
  switch (header)
  {
    case "volt_id":

        var row = data[1];
        var table_access = document.getElementById("cell_info_table").rows[row].cells;    // accesses HTML table
        var volt_reading = (data[3] + data[2] << 8);

        rstring = '';
        rstring.concat('Row ' + row + ': ' + volt_reading + 'V');

        table_access[0].innerHTML = rstring;            // updates value in html table
        break;

    case "temp_msg":
        var row = data[1];
        var single_row_access = document.getElementById("cell_info_table").rows[row].cells;
        var temp_reading = (data[3] + data[2] << 8);

        rstring = '';
        rstring.concat(temp_reading + ' degrees freedomheit');
        single_row_access[1].innerHTML = rstring;
        break;

    case "error_msg":
        var table = document.getElementById('error_msg_table');
        error_msg_names = ['COC', 'DOC', 'Overvolt', 'Undervolt', 'Overtemp', 'Undertemp'];
        for (i=0; i<table.length; i++)
        {
            table.delete_row(i) //Clear all rows b4 repopulation
        }

        for (var byte in data){
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
    var tot_voltage = 0;
    largest = 0;
    smallest = 0;
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

    document.getElementById('cell_delta').innerHTML = largest - smallest;
    document.getElementById('total_voltage').innerHTML = tot_voltage;

    var charge_percent = 1 - (((4.2 - (tot_voltage/21))/10)/.17);   //Calculates battery %
    document.getElementById('charge_percent').innerHTML = charge_percent;

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

