
#ifndef APP_INCLUDE_DRIVER_HAL_BUTTON_H_
#define APP_INCLUDE_DRIVER_HAL_BUTTON_H_

#include <stdio.h>
#include <c_types.h>
#include <gpio.h>
#include <eagle_soc.h>

#define BUTTON_IO 0

#define ButtonOn() GPIO_OUTPUT_SET(GPIO_ID_PIN(BUTTON_IO), 0)
#define ButtonOff() GPIO_OUTPUT_SET(GPIO_ID_PIN(BUTTON_IO), 1)

void button_gpio_init(void);

#endif