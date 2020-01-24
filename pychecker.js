var cells = {}

function parseMsg(String header, int data) {
  switch (header)
  {
  case "volt_id":
//    String slave_id = data[0];
    String row = data[1]
    int volt_reading = (data[3] + data[2] << 8)
    cells[row] = volt_reading
    return [row, volt_reading];
  }
  case "temp_msg":
    String slave_id = data[0];
    String site = data[1]
    int temp_reading = (data[3] + data[2] << 8)
    return
  }
  case "ocv_msg":

}

function get_total_voltage() {
    int nom_voltage = 0;
    for (var series_voltage in cells) {
        nom_voltage += series_voltage;
    }

    return nom_voltage;
}


