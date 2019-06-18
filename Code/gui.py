
import time
from guizero import *
from gpiozero import PWMOutputDevice
from gpiozero import DigitalOutputDevice
import RPi.GPIO as io
import Adafruit_GPIO.SPI as SPI
import Adafruit_MCP3008
#plt.plot([1, 2, 3, 4])
#///////////////// Define Motor Driver GPIO Pins /////////////////
# Motor A, Left Side GPIO CONSTANTS
PWM_DRIVE_LEFT = 21		# ENA - H-Bridge enable pin
FORWARD_LEFT_PIN = 26	# IN1 - Forward Drive
REVERSE_LEFT_PIN = 19	# IN2 - Reverse Drive
# Motor B, Right Side GPIO CONSTANTS
PWM_DRIVE_RIGHT = 5		# ENB - H-Bridge enable pin
FORWARD_RIGHT_PIN = 13	# IN1 - Forward Drive
REVERSE_RIGHT_PIN = 6	# IN2 - Reverse Drive
driveLeft = PWMOutputDevice(PWM_DRIVE_LEFT, True, 0, 1000)
driveRight = PWMOutputDevice(PWM_DRIVE_RIGHT, True, 0, 1000)
 
forwardLeft = DigitalOutputDevice(FORWARD_LEFT_PIN)
reverseLeft = DigitalOutputDevice(REVERSE_LEFT_PIN)
forwardRight = DigitalOutputDevice(FORWARD_RIGHT_PIN)
reverseRight = DigitalOutputDevice(REVERSE_RIGHT_PIN)
io.setwarnings(False)
SPI_PORT   = 0
SPI_DEVICE = 0
mcp = Adafruit_MCP3008.MCP3008(spi=SPI.SpiDev(SPI_PORT, SPI_DEVICE))

io.setmode(io.BCM)
io.setup(12,io.OUT)
io.setup(4,io.OUT);io.setup(3,io.OUT)
pressed=1
var=1
def Stop():
    slider.value=0
    
def modeChange(): 
    if (mode.value=="Manual"):
        isManual(True)
    else:
        isManual(False)
        Stop()
        
def isManual(Manual):
    stopBut.visible=Manual
    speedLab.visible=Manual
    stopLab.visible=Manual
    slider.visible=Manual
app = App(title="Control",height =300,width=300, layout="grid")
box = Box(app,layout="grid",grid=[0,0])
mode= ButtonGroup(box, options=["Auto", "Manual"], selected="Auto",grid=[0,0],align="bottom",command=modeChange)
####################Manual Components################################
stopBut = PushButton(box, command=Stop, text="Stop", grid=[1,1])
speedLab = Text(box, text="Speed",grid=[2,0])
stopLab = Text(box, text="Stop",grid=[1,0])
slider = Slider(box,end=100,start=-100,grid=[2,1])
micLab=Text(box, text="Mic",grid=[0,3])
####################Auto Components##################################

modeChange()
t=0
while True:
    t+=1
    stopLab.clear()
    micLab.clear()
    v=mcp.read_adc(0)*(9.9/1023)
    v=round(v,2)
    s=mcp.read_adc(1)
    s=round(s,2)   
    stopLab.append(v)
    micLab.append(s)
    #io.output(4,1)

    #if (mode.value=="Manual"):

    #else:
    #######################
    
    
    ########################
    speed=slider.value
    forwardRight.value = (speed>=0)
    reverseRight.value = (speed<0)
    if (t % 5==0):
        print (speed)
    driveRight.value =abs((int(slider.value))/100)
    io.output(12,True)
    #time.sleep(.1)
    io.output(3,False)
    #time.sleep(.1)
    app.update()

