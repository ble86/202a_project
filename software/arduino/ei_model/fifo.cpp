#include "fifo.h"

FIFO::FIFO() {
    // for (int i = 0; i < FIFO_SIZE; i++) {
    //     fifo[i] = INITIALIZE_VALUE;
    //     public_fifo[i] = INITIALIZE_VALUE;
    // }
    // fifo_head = 0;
    for (int i = 0; i < FIFO_SIZE; i++) {
        public_fifo[i] = INITIALIZE_VALUE;
    }
    for (int i = 0; i < FIFO_SIZE / 4; i++) {
        sensor1[i] = INITIALIZE_VALUE;
        sensor2[i] = INITIALIZE_VALUE;
        sensor3[i] = INITIALIZE_VALUE;
        sensor4[i] = INITIALIZE_VALUE;
    }
    sensor1_head = 0;
    sensor2_head = 0;
    sensor3_head = 0;
    sensor4_head = 0;
}

void FIFO::update(float new_data, int sensor) {
    // for (int i = 0; i < new_points; ++i) {
    //     fifo[(fifo_head + i) % FIFO_SIZE] = new_data[i];
    // }
    // fifo_head = (fifo_head + new_points) % FIFO_SIZE;
    switch(sensor) {
      case 3:
        sensor1[sensor1_head] = new_data;
        sensor1_head = (sensor1_head + 1) % (FIFO_SIZE / 4);
        break;
      case 4:
        sensor2[sensor2_head] = new_data;
        sensor2_head = (sensor2_head + 1) % (FIFO_SIZE / 4);
        break;
      case 5:
        sensor3[sensor3_head] = new_data;
        sensor3_head = (sensor3_head + 1) % (FIFO_SIZE / 4);
        break;
      case 6:
        sensor4[sensor4_head] = new_data;
        sensor4_head = (sensor4_head + 1) % (FIFO_SIZE / 4);
        break;
      default:
        break;
    }
}

float *FIFO::get() {
    for (int i = 0; i < FIFO_SIZE / 4; ++i) {
      public_fifo[4*i + 0] = sensor1[(sensor1_head + i) % (FIFO_SIZE / 4)];
      public_fifo[4*i + 1] = sensor2[(sensor2_head + i) % (FIFO_SIZE / 4)];
      public_fifo[4*i + 2] = sensor3[(sensor3_head + i) % (FIFO_SIZE / 4)];
      public_fifo[4*i + 3] = sensor4[(sensor4_head + i) % (FIFO_SIZE / 4)];
    }
    // memcpy((void *) public_fifo, (void *)(fifo + fifo_head), (FIFO_SIZE - fifo_head) * sizeof(float));
    // memcpy((void *) (public_fifo + FIFO_SIZE - fifo_head), (void *) fifo, fifo_head * sizeof(float));
    return public_fifo;
}

// void FIFO::clear() {
//     for (int i = 0; i < FIFO_SIZE; i++) {
//         public_fifo[i] = INITIALIZE_VALUE;
//     }
//     fifo_head = 0;
// }