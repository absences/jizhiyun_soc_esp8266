#include "driver/hal.button.h"

#include "osapi.h"
#include "eagle_soc.h"

void ICACHE_FLASH_ATTR

button_gpio_init(void)
{

    PIN_FUNC_SELECT(PERIPHS_IO_MUX_GPIO0_U, FUNC_GPIO0);

    gpio_output_set(0, 0, GPIO_ID_PIN(BUTTON_IO), 0);

    os_printf("GPIO_init_OK!\r\n");
}