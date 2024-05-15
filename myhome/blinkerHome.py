import pygame
import requests
import time
import threading
import json
import RPi.GPIO as GPIO
import readtempDTH11
import random


from blinker import Device, ButtonWidget, NumberWidget

from blinker.voice_assistant import VoiceAssistant, VAType, DuerLightMode, PowerMessage, ModeMessage, ColorMessage, \
    ColorTempMessage, BrightnessMessage, DataMessage

GPIO.setmode(GPIO.BCM)
sigPort = 18

readtemp = readtempDTH11.Readtemp(sigPort)

num = 0
async def button1_callback(msg):
    global num
    num += 1
    await number1.text("num").value(num).update()

async def button2_callback(msg):
    print("Button2: {0}".format(msg))

def get_temp():
  return tempState.temp
def get_humi():
  return tempState.humidity

async def realtime_func(keys):
    print("realtime func received {0}".format(keys))
    for key in keys:
        if key == "humi":
          await device.sendRtData(key, get_humi)
        elif key == "temp":
           await device.sendRtData(key, get_temp)

async def power_change(message: PowerMessage):
    """ 电源状态改变(适用于灯和插座)
    """

    set_state = message.data["pState"]
    print("change power state to : {0}".format(set_state))

    if set_state == "on":
        pass
    elif set_state == "off":
        pass

    await (await message.power(set_state)).update()


async def mode_change(message: ModeMessage):
    """ 模式改变(适用于灯和插座)
    """

    mode = message.data["mode"]
    print("change mode to {0}".format(mode))

    if mode == AliLightMode.READING:
        pass
    elif mode == AliLightMode.MOVIE:
        pass
    elif mode == AliLightMode.SLEEP:
        pass
    elif mode == AliLightMode.HOLIDAY:
        pass
    elif mode == AliLightMode.MUSIC:
        pass
    elif mode == AliLightMode.COMMON:
        pass

    await (await message.mode(mode)).update()


async def color_change(message: ColorMessage):
    """ 颜色改变(适用于灯)
    支持的颜色：Red红色\Yellow黄色\Blue蓝色\Green绿色\White白色\Black黑色\Cyan青色\Purple紫色\Orange橙色
    """

    color = message.data["col"]
    print("change color to {0}".format(color))
    await (await message.color(color)).update()


async def colorTemp_change(message: ColorTempMessage):
    """色温改变(适用于灯)
    """

    color_temp = message.data["colTemp"]
    print("change color temp to {0}".format(color_temp))
    await (await message.colorTemp(100)).update()


async def brightness_change(message: BrightnessMessage):
    """ 亮度改变(适用于灯)
    """

    if "bright" in message.data:
        brightness = int(message.data["bright"])
    elif "upBright" in message.data:
        brightness = int(message.data["upBright"])
    elif "downBright" in message.data:
        brightness = int(message.data["downBright"])
    else:
        brightness = 50

    print("change brightness to {0}".format(brightness))
    await (await message.brightness(brightness)).update()

async def state_query(message: DataMessage):
    print("query state: {0}".format(message.data))
    #await message.power("on")
    #await message.mode(AliLightMode.HOLIDAY)
    #await message.color("red")
    #await message.brightness(66)

    await message.temp(tempState.temp)
    await message.humi(tempState.humidity)
    await message.update()


device = Device("ec4369c659bc", realtime_func=realtime_func,mi_type=VAType.SENSOR)

voice_assistant = VoiceAssistant(VAType.SENSOR)
voice_assistant.mode_change_callable = mode_change
voice_assistant.colortemp_change_callable = colorTemp_change
voice_assistant.color_change_callable = color_change
voice_assistant.brightness_change_callable = brightness_change
voice_assistant.state_query_callable = state_query
voice_assistant.power_change_callable = power_change

device.addVoiceAssistant(voice_assistant)

button1 = device.addWidget(ButtonWidget('btn-123'))
button2 = device.addWidget(ButtonWidget('btn-abc'))
number1 = device.addWidget(NumberWidget('num-abc'))

button1.func = button1_callback
button2.func = button2_callback

weData = {
  '晴':'qing',
  '阴':'duoyun',
  '多云':'duoyun',
  '阵雨':'zhenyu',
  '大雨':'dayu',
  '中雨':'zhongyu',
  '小雨':'xiaoyu',
  '雷阵雨':'leizhenyu',
  '雷电':'leidian',
  '雪':'xue',
  '雾':'wu'
}

class states():
  def __init__(self,temp,text,humidity):
    #温度
    self.temp=temp
    #天气图标
    self.text=text
    #湿度
    self.humidity=humidity

tempState=states(0,0,0)

def getwether():

  while True:
    url = "https://devapi.heweather.net/v7/weather/now?location=101270101&key=148c121458374402a89c67fcd37e895c"
    r = requests.get(url)
    now=json.loads(r.text)
    #tempState.temp=now['now']['temp']
    tempState.text=now['now']['text']
    #tempState.humidity=now['now']['humidity']
    #每隔2小时获取天气图标
    time.sleep(7200)

def drawui():

  pygame.init() 
  screen = pygame.display.set_mode([800,460])
  pygame.display.set_caption("Xie Wen's Home")

  font = pygame.font.Font(None,60)
  fontMax = pygame.font.Font(None,120)
  fcolor = (203,229,78)
  fgcolor = (250,247,202)
  path = "/home/xiewen/Desktop/myhome/"
  bg_image=pygame.image.load(path+"bg.png").convert_alpha()

  while True:
    for event in pygame.event.get():
      if event.type == pygame.QUIT:
        pygame.quit()
        GPIO.cleanup()

    screen.fill([0, 0, 0])
    screen.blit(bg_image,(0,0))
  
    if tempState.text !=0 :
      temp = font.render(str(tempState.temp)+"°C",True,fcolor)
      screen.blit(temp,(170,25))
      screen.blit(pygame.image.load(path+weData[tempState.text] + ".png").convert_alpha(),(30,110))
      humidity = font.render(str(tempState.humidity) + "%",True,fcolor)
      screen.blit(humidity,(170,80))

    pygame.display.update()

def getRealTemp():

  while True:
    temp, humidity = readtemp.temp()

    if humidity > 0 :
      tempState.humidity = humidity
      tempState.temp = temp
      time.sleep(10)

def threadfun():

  weatherThread=threading.Thread(target=getwether)
  weatherThread.start()

  tempThread=threading.Thread(target=getRealTemp)
  tempThread.start()

  uiThread=threading.Thread(target=drawui)
  uiThread.start()
#Main Begine
def main():

  threadfun()
  device.run()

if __name__=="__main__":
    main()
