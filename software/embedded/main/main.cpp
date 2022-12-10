/*
 * =====================================================================================
 *
 *       Filename:  main.cpp
 *
 *    Description:  
 *
 *        Version:  1.0
 *        Created:  11/12/2022 07:11:01 PM
 *       Revision:  none
 *       Compiler:  gcc
 *
 *         Author:  Benjamin Gillmore (bg), bggillmore@gmail.com
 *        Company:  University of California Los Angeles
 *
 * =====================================================================================
 */


#include <string.h>
#include <stdio.h>
#include <math.h>
#include "sdkconfig.h"
#include "esp_log.h"

#include "freertos/FreeRTOS.h"
#include "freertos/task.h"
#include "freertos/semphr.h"

#include "driver/adc.h"
#include "driver/uart.h"
#include "driver/gpio.h"

#include "Arduino.h"
#include "sdkconfig.h"

#define UART_PORT_NUM UART_NUM_0
#define QUEUE_LEN 512

#define BUF_SIZE (1024)
#include <esp32-hal-timer.h>

#include <Mapped_Range_inferencing.h>
#include <ei_classifier_porting.h>
#include <ei_classifier_porting.cpp>

//#define CONFIG_BT_ENABLED
//#define CONFIG_BLUEDROID_ENABLED
//
//#include "BluetoothSerial.h"
//
//#if !defined(CONFIG_BT_ENABLED) || !defined(CONFIG_BLUEDROID_ENABLED)
//#error Bluetooth is not enabled! Please run `make menuconfig` to and enable it
//#endif

//#include <semphr.h>
//typedef struct ContactMic{

typedef struct ContactMic{
      uint16_t num :4;
      uint16_t val :12;
} contactMic_t;



// Globals
static SemaphoreHandle_t mutex;


const int wdtTimeout = 1000;  //time in ms to trigger the timer
hw_timer_t* timer = NULL;
static TaskHandle_t send_to_classifier_handle;
static TaskHandle_t start_adc_handle;

static QueueHandle_t sensor1_queue;
static QueueHandle_t sensor2_queue;
static QueueHandle_t sensor3_queue;
static QueueHandle_t sensor4_queue;

#define ENERGY_THRESHOLD 	0x100000
#define ENERGY_BASE		0x6E0

#define TIMES              512
#define GET_UNIT(x)        ((x>>3) & 0x1)

#define ADC_RESULT_BYTE     2
#define ADC_CONV_LIMIT_EN   0
#define ADC_CONV_MODE       ADC_CONV_SINGLE_UNIT_1
#define ADC_OUTPUT_TYPE     ADC_DIGI_OUTPUT_FORMAT_TYPE1

static uint16_t adc1_chan_mask = BIT(3) | BIT(4) | BIT(5) | BIT(6);
static adc_channel_t channel[4] = {ADC_CHANNEL_3, ADC_CHANNEL_4, ADC_CHANNEL_5, ADC_CHANNEL_6};
static const char *TAG = "ADC DMA";

static const bool debug_nn = false; // Set this to true to see e.g. features generated from the raw signal

//BluetoothSerial SerialBT;


void send_to_classifier_task(void* n){
    float buffer[QUEUE_LEN*4] = { 0 };
    //printf("%d", sizeof(buffer));
    contactMic_t sensor;
    signal_t signal;
    int err = numpy::signal_from_buffer(buffer, EI_CLASSIFIER_DSP_INPUT_FRAME_SIZE, &signal);
    ei_impulse_result_t result = {};

    while(true){
		vTaskSuspend(NULL);
		for (size_t ix = 0; ix < QUEUE_LEN*4; ix += 4) {
			for(int i = 0; i < 4; i++) {
				switch(i){
					case 0:
						xQueueReceive(sensor1_queue, &sensor, 0); 
						break;
					case 1:
						xQueueReceive(sensor2_queue, &sensor, 0); 
						break;
					case 2:
						xQueueReceive(sensor3_queue, &sensor, 0); 
						break;
					case 3:
						xQueueReceive(sensor4_queue, &sensor, 0); 
						break;
					default:
						break;
				}
			buffer[ix + i] =(float) (map(sensor.val, 0, 4095, 0, 255) - 50); 
		}
        }

	//uart_write_bytes(UART_PORT_NUM, buffer, sizeof(buffer));
	//uart_write_bytes(UART_PORT_NUM, "\r\n", 2);

        // Turn the raw buffer in a signal which we can the classify
        err = numpy::signal_from_buffer(buffer, EI_CLASSIFIER_DSP_INPUT_FRAME_SIZE, &signal);
        if (err != 0) {
		ei_printf("ERR:(%d)\r\n", err);
        }

//	printf("Value: %0.3f\n", buffer[0]);

        // Run the classifier
        err = run_classifier(&signal, &result, debug_nn);

        if (err != EI_IMPULSE_OK) {
		printf("ERR:(%d)\r\n", err);
        }

	//SerialBT.write("Hello World!\n");
        // print the predictions
        printf("a:%.3f b:%.3f c:%.3f d:%.3f e:%.3f f:%.3f s:%.3f\r\n",
		result.classification[0].value, result.classification[1].value,
		result.classification[2].value,	result.classification[3].value,
		result.classification[4].value,	result.classification[5].value,
		result.classification[6].value);
//        printf("Predictions (DSP: %d ms., Classification: %d ms., Anomaly: %d ms.):\r\n",
//		result.timing.dsp, result.timing.classification, result.timing.anomaly);
//        for (size_t ix = 0; ix < EI_CLASSIFIER_LABEL_COUNT; ix++) {
//		printf("%s: %.5f\r\n", result.classification[ix].label, result.classification[ix].value);
//        }
	//vTaskDelay(500);
    }
}


static void continuous_adc_init(uint16_t adc1_chan_mask, adc_channel_t *channel, uint8_t channel_num)
{
	
    adc_digi_init_config_t adc_dma_config = {
        .max_store_buf_size = 1024,
        .conv_num_each_intr = TIMES,
        .adc1_chan_mask = adc1_chan_mask,
    };
    ESP_ERROR_CHECK(adc_digi_initialize(&adc_dma_config));

    adc_digi_configuration_t dig_cfg = {
        .conv_limit_en = ADC_CONV_LIMIT_EN,
        .conv_limit_num = 250,
        .sample_freq_hz = 10 * 1000,
        .conv_mode = ADC_CONV_MODE,
        .format = ADC_OUTPUT_TYPE,
    };

    adc_digi_pattern_config_t adc_pattern[SOC_ADC_PATT_LEN_MAX] = {};
    dig_cfg.pattern_num = channel_num;
    for (int i = 0; i < channel_num; i++) {
        uint8_t unit = GET_UNIT(channel[i]);
        uint8_t ch = channel[i] & 0x7;
        adc_pattern[i].atten = ADC_ATTEN_DB_11;
        adc_pattern[i].channel = ch;
        adc_pattern[i].unit = unit;
        adc_pattern[i].bit_width = SOC_ADC_DIGI_MAX_BITWIDTH;
    }
    dig_cfg.adc_pattern = adc_pattern;
    ESP_ERROR_CHECK(adc_digi_controller_configure(&dig_cfg));
}
void start_adc(void* n){
	esp_err_t ret;
	contactMic_t sensor = {0};
	uint32_t ret_num = 0;
	uint8_t result[TIMES] = {0};
	
	memset(result, 0xcc, TIMES);
	
	continuous_adc_init(adc1_chan_mask, channel, sizeof(channel) / sizeof(adc_channel_t));
	adc_digi_start();
    	long long unsigned int energy1, energy2, energy3, energy4, energy_av;

	energy1 = 0;
	energy2 = 0;
	energy3 = 0;
	energy4 = 0;
	
	while(true){
        	ret = adc_digi_read_bytes(result, TIMES, &ret_num, ADC_MAX_DELAY);
		
		if (ret == ESP_OK || ret == ESP_ERR_INVALID_STATE) {
			for(int i = 0; i < ret_num-2; i+=2){
				sensor.num = (result[i+1]<<8 | result[i]) >> 12;
				sensor.val = (result[i+1]<<8 | result[i]) & 0xFFF;
				switch(sensor.num){
					case 3:
						energy1 += (sensor.val - ENERGY_BASE) * (sensor.val - ENERGY_BASE);
						if (uxQueueSpacesAvailable(sensor1_queue) != 0 )
							xQueueSend(sensor1_queue, &sensor, 0);
						break;
					case 4:
						energy2 += (sensor.val - ENERGY_BASE) * (sensor.val - ENERGY_BASE);
						if (uxQueueSpacesAvailable(sensor2_queue) != 0 )
							xQueueSend(sensor2_queue, &sensor, 0);
						break;
					case 5:
						energy3 += (sensor.val - ENERGY_BASE) * (sensor.val - ENERGY_BASE);
						if (uxQueueSpacesAvailable(sensor3_queue) != 0 )
							xQueueSend(sensor3_queue, &sensor, 0);
						break;
					case 6:
						energy4 += (sensor.val - ENERGY_BASE) * (sensor.val - ENERGY_BASE);
						if (uxQueueSpacesAvailable(sensor4_queue) != 0 )
							xQueueSend(sensor4_queue, &sensor, 0);
						break;
					default:
						printf("Something is broken -> Sensor.num == %d\n", sensor.num);
						break;
				}

				//If queues are full then schedule the classifier
				if( uxQueueSpacesAvailable(sensor1_queue) == 0 &&
					uxQueueSpacesAvailable(sensor2_queue) == 0 &&
					uxQueueSpacesAvailable(sensor3_queue) == 0 &&
					uxQueueSpacesAvailable(sensor4_queue) == 0)
				{
					// Get average energy
					energy_av = (energy1 + energy2 + energy3 + energy4)/4;
					//printf("Average Energy is: 0x%llx\n", energy_av);
					energy1 = 0;
					energy2 = 0;
					energy3 = 0;
					energy4 = 0;
					
					// If average energy is over threshold - classify - otherwise clear queues
					if(energy_av > ENERGY_THRESHOLD)
						vTaskResume(send_to_classifier_handle);
					else{
						xQueueReset(sensor1_queue);
						xQueueReset(sensor2_queue);
						xQueueReset(sensor3_queue);
						xQueueReset(sensor4_queue);
					}
						
				}
			}
			vTaskDelay(15);
		} else if (ret == ESP_ERR_TIMEOUT) {
			ESP_LOGW(TAG, "No data, increase timeout or reduce conv_num_each_intr");
			vTaskDelay(1000);
		}
	}
	adc_digi_stop();
	ret = adc_digi_deinitialize();
	assert(ret == ESP_OK);
}


extern "C" void app_main() {
//void app_main(void){
	printf("--- app_main() begin ---\n");
	
//	SerialBT.begin("ESP32test"); //Bluetooth device name
//	if (SerialBT.available()) {
//	SerialBT.read()
	
	//Set up Queue
	sensor1_queue = xQueueCreate(QUEUE_LEN, 2);
	sensor2_queue = xQueueCreate(QUEUE_LEN, 2);
	sensor3_queue = xQueueCreate(QUEUE_LEN, 2);
	sensor4_queue = xQueueCreate(QUEUE_LEN, 2);

	mutex = xSemaphoreCreateMutex();
	
	/* Configure parameters of an UART driver,
	* communication pins and install the driver */
	uart_config_t uart_config = {
		.baud_rate = 921600,//115200,
		.data_bits = UART_DATA_8_BITS,
		.parity = UART_PARITY_DISABLE,
		.stop_bits = UART_STOP_BITS_1,
		.flow_ctrl = UART_HW_FLOWCTRL_DISABLE,
		.source_clk = UART_SCLK_APB,
	};
	//Install UART driver, and get the queue.
	uart_driver_install(UART_PORT_NUM, BUF_SIZE * 2, BUF_SIZE * 2, 20, NULL, 0);
	uart_param_config(UART_PORT_NUM, &uart_config);

	xTaskCreate(start_adc, "start_adc", 4097, NULL, 6, &start_adc_handle);
	xTaskCreate(send_to_classifier_task, "send_to_classifier", 16384, NULL, 7, &send_to_classifier_handle);
}

