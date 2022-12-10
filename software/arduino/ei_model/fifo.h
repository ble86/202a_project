#ifndef FIFO_H
#define FIFO_H

#include <cstring>

#define FIFO_SIZE 2048
#define INITIALIZE_VALUE 0

class FIFO {
    private:
        float public_fifo[FIFO_SIZE];
        float sensor1 [FIFO_SIZE / 4];
        float sensor2 [FIFO_SIZE / 4];
        float sensor3 [FIFO_SIZE / 4];
        float sensor4 [FIFO_SIZE / 4];

        int sensor1_head;
        int sensor2_head;
        int sensor3_head;
        int sensor4_head;
    public:
        FIFO();
        void update(float new_data, int sensor);
        float *get();
        // void clear();
};

#endif