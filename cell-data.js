cells = {}
temps = {}

function parseMsg(header, data) {
  switch (header)
  {
    case "volt_id":

        var row = data[1]
        var table_access = document.getElementById("cell_info_table").rows[row].cells;    // accesses HTML table
        var volt_reading = (data[3] + data[2] << 8)

        rstring = ''
        rstring.concat('Row ' + row + ': ' + volt_reading + 'V');

        table_access[0].innerHTML = rstring;            // updates value in html table
        break;

    case "temp_msg":
        var row = data[1]
        var table_access = document.getElementById("cell_info_table").rows[row].cells;
        var temp_reading = (data[3] + data[2] << 8)

        rstring = ''
        rstring.concat(temp_reading + ' degrees freedomheit');
        table_access[1].innerHTML = rstring;
        break;

    case "error_msg":
        var error_msg_bank = 'Errors: ';
        error_msg_names = ['COC', 'DOC', 'Overvolt', 'Undervolt', 'Overtemp', 'Undertemp']
        for (var bit in data){
            if(bit == 0)
            {
                error_msg_bank.concat(error_msg_names[bit] + '- ';
            }
        }

        document.getElementById('error_msgs').innerHTML = error_msg_bank;
        break;

    default:
        return "Message not recognised. Something is really fucked up because we should've already checked for this.";
  }
}

function get_total_voltage() {
    var nom_voltage = 0;
    for (var series_voltage in cells) {
        nom_voltage += series_voltage;
    }

    return nom_voltage;
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

