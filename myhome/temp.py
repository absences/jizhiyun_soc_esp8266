import pygame
import requests
import time

import threading
import json
import RPi.GPIO as GPIO
import readtempDTH11

GPIO.setmode(GPIO.BCM)
sigPort = 18

weData={
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
 def __init__(self,temp,text,qc,qh,fc):
   #网上温度
  self.temp=temp
  #天气图标
  self.text=text
  #传感器温度
  self.qc=qc
  #湿度
  self.qh=qh
  #机器cpu温度
  self.fc=fc

tempState=states(0,0,0,0,0)

def GetTemp():
 url = "https://devapi.heweather.net/v7/weather/now?location=101270101&key=148c121458374402a89c67fcd37e895c"
 r = requests.get(url)
 now=json.loads(r.text)
 tempState.temp=now['now']['temp']
 tempState.text=now['now']['text']

 global timer
 timer=threading.Timer(7200,GetTemp)
 timer.start()
def GetRealTemp():
 temp, hum = readtemp.temp()
 tempState.qc=temp
 tempState.qh=hum
 filec = open("/sys/class/thermal/thermal_zone0/temp")
 tempState.fc=round(float(filec.read()) / 1000,1)
 filec.close()
 global temper
 temper=threading.Timer(10,GetRealTemp)
 temper.start()

#Main Begine
pygame.init() 
screen = pygame.display.set_mode([800,460])
pygame.display.set_caption("System Info")

font=pygame.font.Font(None,60)
fontMax=pygame.font.Font(None,120)
fcolor=(203,229,78)
fgcolor=(250,247,202)
path="/home/pi/Desktop/myprg/"
bg_image=pygame.image.load(path+"bg.png").convert_alpha()
readtemp = readtempDTH11.Readtemp(sigPort)

GetTemp()
time.sleep(0.5)

GetRealTemp()
while True:
 screen.fill([0, 0, 0])
 screen.blit(bg_image,(0,0))

 ta=time.localtime()
 cymd=time.strftime("%y-%m-%d",ta)
 chms=time.strftime("%H:%M:%S",ta)

 timey=font.render(str(cymd),True,fcolor)
 timeh=fontMax.render(str(chms),True,fgcolor)
 screen.blit(timey,(430,80))
 screen.blit(timeh,(430,150))
 
 if tempState.temp != 0:
   tempt=font.render(str(tempState.qc)+"℃/"+str(tempState.temp)+"℃    CPU:"+ str(tempState.fc) +"℃",True,fcolor)
   screen.blit(tempt,(170,25))
   screen.blit(pygame.image.load(path+weData[tempState.text]+".png").convert_alpha(),(30,110))
   hut=font.render(str(tempState.qh)+"%",True,fcolor)
   screen.blit(hut,(170,80))
   
 
 pygame.display.update()
 time.sleep(1)
 for event in pygame.event.get():
     if event.type == pygame.QUIT:
         GPIO.cleanup()
         
         pygame.quit()
         break
