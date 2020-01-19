var cells = {}

function parseMsg(String header, int data) {
  switch (header)
  {
    case "volt_id":
        String row = data[1]
        int volt_reading = (data[3] + data[2] << 8)
        cells[row] = volt_reading
        return [row, volt_reading];

    case "temp_msg":
        String site = data[1]
        int temp_reading = (data[3] + data[2] << 8)
        return [site, temp_reading]

    case "error_msg":
        error_msg_bank = []
        error_msg_names = ['COC', 'DOC', 'Overvolt', 'Undervolt', 'Overtemp', 'Undertemp']
        for bit in data:
            if(bit == 0)
            {
                error_msg_bank.push(error_msg_names[bit]);
            }

        return error_msg_bank;

    default:
        return "Message not recognised. Something is really fucked up because we should've already checked for this."
  }

function get_total_voltage() {
    int nom_voltage = 0;
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