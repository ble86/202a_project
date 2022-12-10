/* Includes ---------------------------------------------------------------- */
#include <Mapped_Range_v5_inferencing.h>
#include <ArduinoBLE.h>
#include "fifo.h"

/* Private variables ------------------------------------------------------- */
static const bool debug_nn = false; // Set this to true to see e.g. features generated from the raw signal

FIFO fifo;
// char receive_buff[1024];
int received_samples;

bool validate_retrieve_data(uint8_t *read_buff);
int receive_data();
bool trigger_classification();
void classify();

/**
* @brief      Arduino setup function
*/
void setup()
{
    /* Init serial */
    Serial.begin(921600);
    Serial1.begin(921600);
    // comment out the below line to cancel the wait for USB connection (needed for native USB)
    while (!Serial1);

    received_samples = 0;
    // ei_printf("Hello World\n");
}

/**
* @brief      Get data and run inferencing
*/
void loop()
{
    // ei_printf("Hello World\n");
    received_samples += receive_data();
    ei_printf(" ");
    // delay(100);
    bool received_enough = received_samples > 2048;
    bool trigger = received_enough && trigger_classification();
    if (trigger) {
      ei_printf("Going to trigger classification\n");
      classify();
      // fifo.clear();
      received_samples = 0;
      // delay(1000);
    }
}

bool validate_retrieve_data(uint8_t *read_buff) {
  uint8_t first_sensor = (read_buff[0] & 0xF0) >> 4;
  uint8_t second_sensor = (read_buff[2] & 0xF0) >> 4;
  uint8_t third_sensor = (read_buff[4] & 0xF0) >> 4;
  uint8_t fourth_sensor = (read_buff[6] & 0xF0) >> 4;

  bool is_3456 = (first_sensor == 3) && (second_sensor == 4) && (third_sensor == 5) && (fourth_sensor == 6);
  bool is_4563 = (first_sensor == 4) && (second_sensor == 5) && (third_sensor == 6) && (fourth_sensor == 3);
  bool is_5634 = (first_sensor == 5) && (second_sensor == 6) && (third_sensor == 3) && (fourth_sensor == 4);
  bool is_6345 = (first_sensor == 6) && (second_sensor == 3) && (third_sensor == 4) && (fourth_sensor == 5);

  return is_3456 || is_4563 || is_5634 || is_6345;
}

int receive_data() {
  uint8_t data;
  uint8_t read_bytes = 0;
  uint8_t read_buffer[1024] = {0}; 
  // ei_printf("Starting Receive data\n");
  while(!Serial1.available());

  while(Serial1.available()){
    data = Serial1.read();
    if(data != '\n'){
        read_buffer[read_bytes] = data;
        read_bytes++;
    }
    else{
        break;
    }
  }

  if (read_bytes < 8) {
    // ei_printf("Invalid read size %d\n", read_bytes);
    return 0;
  }

  // ei_printf("Data: ");
  // for(int i = 0; i < 8; i++ ) { 
  //   ei_printf("0x%x ", read_buffer[i]);
  // }
  // ei_printf("\n");


  if (!validate_retrieve_data(read_buffer)) {
    // ei_printf("Invalid alignment\n");
    return 0;
  }

  // while(!Serial1.available());
  // size_t read_bytes = Serial1.readBytesUntil('\n', receive_buff, 1024);
  //  ei_printf("Read bytes %d\n", read_bytes);

  for (int i = 0; i < read_bytes; i += 2) {
    int msb = read_buffer[i];
    int sensor = (msb & 0xF0) >> 4;
    msb = msb & 0x0F;
    int lsb = read_buffer[i + 1];

    int int_data = ((msb << 8) | lsb);
    float float_data = (float) (map(int_data, 0, 4095, 0, 255) - 50);

    // ei_printf("Sensor %d value: %.3f\r\n", sensor, float_data);

    fifo.update(float_data, sensor);
  }

  return read_bytes / 2;
}

bool trigger_classification() {
   float *data = fifo.get();

   const int START_INDEX = 170 * 4;
   const int END_INDEX = 342 * 4;
   const float ENERGY_THRESH = 6500;

   float energy = 0;

   for (int i = START_INDEX; i < END_INDEX; i += 4) {
       float data_val = data[i] - 53;
       energy += (data_val * data_val);
   }

   return energy > ENERGY_THRESH;
}

void classify() {
   // Allocate a buffer here for the values we'll read from the sensor
   float *data = fifo.get();

   // Turn the raw buffer in a signal which we can the classify
   signal_t signal;
   int err = numpy::signal_from_buffer(data, EI_CLASSIFIER_DSP_INPUT_FRAME_SIZE, &signal);
   if (err != 0) {
       ei_printf("ERR:(%d)\r\n", err);
       return;
   }

   // Run the classifier
   ei_impulse_result_t result = { 0 };

   err = run_classifier(&signal, &result, debug_nn);
   if (err != EI_IMPULSE_OK) {
       ei_printf("ERR:(%d)\r\n", err);
       return;
   }
 
   // print the predictions
   ei_printf("Prediction (DSP: %d ms., Classification: %d ms., Anomaly: %d ms.):\r\n",
       result.timing.dsp, result.timing.classification, result.timing.anomaly);
   for (size_t ix = 0; ix < EI_CLASSIFIER_LABEL_COUNT; ix++) {
       ei_printf("%s: %.5f\r\n", result.classification[ix].label, result.classification[ix].value);
   }
}
