cells = {}
temps = {}

function parseMsg(header, data) {
  switch (header)
  {
    case "volt_id":
        var row = data[1]
        var volt_reading = (data[3] + data[2] << 8)
        cells[row] = volt_reading;

        rstring = ''
        for row in cells:
            rstring.concat('Row ' + row + ': ' + cells[row] + 'V --- ');

        document.getElementById('voltage_readings').innerHTML = rstring;
        break;

    case "temp_msg":
        var row = data[1]
        var temp_reading = (data[3] + data[2] << 8)

        rstring = ''
        for row in temps:
            rstring.concat('Row ' + row + ': ' + temps[row] + 'degrees freedomheit --- ');

        document.getElementById('temp_readings').innerHTML = rstring;
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

