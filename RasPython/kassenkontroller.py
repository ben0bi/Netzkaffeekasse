# You may need to install RPi.GPIO and the picamera module for python3:
#
# sudo apt-get install python{,3}-pip
# sudo pip3 install RPi.GPIO
#
# sudo apt-get install python3-picamera

# Kassenkamera Script
# GPIO SETTING
#
#     3v3 .. 5v
# GPIO  2 .. 5v
# GPIO  3 .. GND
# GPIO  4 .. GPIO 14
#     GND .. GPIO 15
# GPIO 17 .. GPIO 18
# GPIO 27 .. GND
# GPIO 22 .. GPIO 23
#     3v3 .. GPIO 24
# GPIO 10 .. GND
# GPIO  9 .. GPIO 25
# GPIO 11 .. GPIO  8
#     GND .. GPIO  7
#   ID_SD .. ID_SC
# GPIO  5 .. GND
# GPIO 19 .. GPIO 16
# GPIO 26 .. GPIO 20
#     GND .. GPIO 21
# vv USB PORT vv

# GPIO library
import RPi.GPIO as GPIO
# Time libs
from time import sleep
import datetime
# File operation libs
import os
from shutil import copyfile
# Camera lib
from picamera import PiCamera

# the camera
camera = PiCamera()

# start the camera right away so we can take stills everytime we want.
camera.start_preview()
# wait at least 2 seconds to focus and stuff.
sleep(3)
camera.stop_preview()

# The kontrol inputs are two contacts at the corner of the lid of the box.
# They will determine if the box is open or closed.
# # Connect them to 3.3v!
kontrol1 = 24
kontrol2 = 10

# The f inputs are for the Franken (1,2,5)
frGND = 2
f5 = 23
f2 = 18
f1 = 17
# The r inputs are for the Rappen (5,10,20,50)
r5 = 3
r10 = 14
r50 = 4
r20 = 15

GPIO.setmode(GPIO.BCM)

# Setup the open/close controls.
GPIO.setup(kontrol1, GPIO.IN)
GPIO.setup(kontrol2, GPIO.IN)

# Setup the F/R controls.
GPIO.setup(frGND, GPIO.IN)
GPIO.setup(f5, GPIO.IN)
GPIO.setup(f2, GPIO.IN)
GPIO.setup(f1, GPIO.IN)
GPIO.setup(r5, GPIO.IN)
GPIO.setup(r10, GPIO.IN)
GPIO.setup(r20, GPIO.IN)
GPIO.setup(r50, GPIO.IN)

# check if it was open/closed before
oldkontrol1 = 0
oldkontrol2 = 0

# 0 = closed, 1 = full open, 2 = half open
opened = 2

# COIN is the actual coin, TOTAL is everything counted.
COIN = 0.00
TOTAL = 0.00

# get the actual date and time.
def Now():
  return datetime.datetime.now().strftime("%a, %Y-%m-%d %H:%M:%S")

def NowFilename():
  return datetime.datetime.now().strftime("%Y_%m_%d_T%H_%M_%S")

# create a camera image.
def Shoot(filename,text,date):
  name = filename+"_"+date+".jpg"
  camera.capture(name)
  copyfile(name, "/var/www/html/IMAGES/latest.jpg")
  f = open("ACTUALTEXT.nkk","w")
  f.write(text+"\n")
  f.close()
  f = open("ACTUALTIMESTAMP.nkk","w")
  f.write(date+"\n")
  f.close()

# Save the total value.
def SaveTotal(total):
  f = open("TOTAL.nkk","w")
  f.write(str(round(total,2)))
  f.close()

# Load the total value.
def LoadTotal():
  if os.path.isfile("TOTAL.nkk"):
    f = open("TOTAL.nkk", "r")
    q = f.read()
    TOTAL = round(float(q),2)
    f.close()
    print("Loaded Total: "+str(TOTAL))
    return TOTAL
  else:
    print("Total file does not exist yet.")
    return 0.0

# Save a log line.
def Log(text):
  f = open("LOG.nkk","a")
  f.write(text+"\n")
  f.close()
  print(text)

# MAIN
Log(Now()+" --> Kassenkontroller gestartet.")
TOTAL = LoadTotal()

# Main loop  
while True:
  i1 = GPIO.input(kontrol1)
  i2 = GPIO.input(kontrol2)

  fignd = GPIO.input(frGND)
  fi5 = GPIO.input(f5)
  fi2 = GPIO.input(f2)
  fi1 = GPIO.input(f1)
  ri5 = GPIO.input(r5)
  ri10 = GPIO.input(r10)
  ri20 = GPIO.input(r20)
  ri50 = GPIO.input(r50)

# check for one of the two triggers.
  if ((not i1) and (oldkontrol1 == 1)):
    print("1 OPEN")
    oldkontrol1 = 0
    if opened==0 or opened==1:
      print("WARNING> The box is HALF open! [1]")
      opened = 2
  elif (i1 and (oldkontrol1 == 0)):
    print("1 CLOSE")
    oldkontrol1 = 1

  if ((not i2) and (oldkontrol2 == 1)):
    print("2 OPEN")
    oldkontrol2 = 0
    if opened==0 or opened==1:
      print("WARNING> The box is HALF open! [2]")
      opened = 2
  elif (i2 and (oldkontrol2 == 0)):
    print("2 CLOSE")
    oldkontrol2 = 1

# check for completely open or closed box.
  if ((oldkontrol1 == 0) and (oldkontrol2 == 0) and (opened != 1)):
    dt = Now()
    Log("ALERT> "+dt+": THE BOX IS COMPLETELY OPEN !!")
    Shoot("ALERT_IMAGES/OPENED_AT","ALERT> "+dt+" --> THE BOX WAS OPENED!", NowFilename())
    opened = 1

  if ((oldkontrol1 == 1) and (oldkontrol2 == 1)):
    if(opened != 0):
      Log(Now()+" --> The Box is now closed.")
    opened = 0

# Check the F/R inputs.
# on GND, add the coin if there is one.
  if fignd:
    if COIN != 0.0:
      txt=""
      if COIN == 0.05:
        txt=" --> Knauserige 5 Rappen."
      # Set  0.50 coin if so.
      if COIN == 0.07:
        txt=" --> Fifty Cent, Br0!"
        COIN = 0.50
      if COIN == 0.10:
        txt=" --> 10 Rappen. Naja."
      if COIN == 0.20:
        txt=" --> 20 Rappen. Immerhin."
      if COIN == 1.00:
        txt=" --> Ein ganzer Franken."
      if COIN == 2.00:
        txt=" --> Zwei Franken. Erstaunlich!"
      if COIN == 5.00:
        txt=" --> Eine Helvetia. Danke, edler Spender."

      # add total and reset coin.
      TOTAL = round(TOTAL + COIN,2)
      dt = Now()
      # Make an image.
      Shoot("EINWURF_IMAGES/EINWURF_"+str(COIN)+"_Franken",dt+txt,NowFilename())
      Log(dt+txt)
      SaveTotal(TOTAL)
      COIN = 0.0
      Log(dt+" --> TOTAL: "+str(TOTAL))

  if ri5 and (COIN <= 0.05):
    COIN = 0.05
  if ri50 and (COIN <= 0.07):
    # 0.50 is smaller than 0.10 so we set it to 0.07 and later to 0.50
    COIN = 0.07
  if ri10 and (COIN <= 0.10):
    COIN = 0.10
  if ri20 and (COIN <= 0.20):
    COIN = 0.20
  if fi1 and (COIN <= 1.00):
    COIN = 1.00
  if fi2 and (COIN <= 2.00):
    COIN = 2.00
  if fi5 and (COIN <= 5.00):
    COIN = 5.00

  sleep(0.005)

Log(Now()+" --> Kassenkontroller CLOSED!")
camera.close()
