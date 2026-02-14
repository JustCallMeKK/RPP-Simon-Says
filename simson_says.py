from machine import Pin
import utime
import random
import machine

buttonR = Pin(12, Pin.IN, Pin.PULL_UP)
buttonG = Pin(13, Pin.IN, Pin.PULL_UP)
buttonB = Pin(14, Pin.IN, Pin.PULL_UP)
buttonY = Pin(15, Pin.IN, Pin.PULL_UP)

ledR = Pin(11, Pin.OUT)
ledG = Pin(16, Pin.OUT)
ledB = Pin(17, Pin.OUT)
ledY = Pin(10, Pin.OUT)

buzzer = machine.PWM(machine.Pin(0))

ledOrder = []

def playTone(frequency, duration = 0.2, volume = 0.015):
    buzzer.freq(frequency)
    buzzer.duty_u16(int(65535 * volume)) #set duty cylce to 50%
    utime.sleep(duration)
    buzzer.duty_u16(0)

def toggleLED(colour):
    if (colour == 'r'):
        ledR.toggle()
    elif (colour == 'g'):
        ledG.toggle()
    elif (colour == 'b'):
        ledB.toggle()
    elif (colour == 'y'):
        ledY.toggle()

# 
def getInput(playSound = 1):
    userInput = 'none'
    while userInput == 'none':
        if buttonR.value() == 0:
            toggleLED('r')
            while buttonR.value() == 0:
                if (playSound): playTone(440, 0.1)
            toggleLED('r')
            userInput = 'r'
        if buttonG.value() == 0:
            toggleLED('g')
            while buttonG.value() == 0:
                if (playSound): playTone(523, 0.1)
            toggleLED('g')
            userInput = 'g'
        if buttonB.value() == 0:
            toggleLED('b')
            while buttonB.value() == 0:
                if (playSound): playTone(659, 0.1)
            toggleLED('b')
            userInput = 'b'
        if buttonY.value() == 0:
            toggleLED('y')
            while buttonY.value() == 0:
                if (playSound): playTone(783, 0.1)
            toggleLED('y')
            userInput = 'y'
    
    return userInput

def userPlay():
    correct = 1
    for colour in ledOrder:
        if (colour != getInput()):
            correct = 0
            break
    return correct

def playOrder(mult):
    for colour in ledOrder:
        toggleLED(colour)
        if (colour == 'r'):
            playTone(440, 0.3 / mult)
        elif (colour == 'g'):
            playTone(523, 0.3 / mult)
        elif (colour == 'b'):
            playTone(659, 0.3 / mult)
        elif (colour == 'y'):
            playTone(783, 0.3 / mult)
        toggleLED(colour)
        utime.sleep(0.2 / mult)
        
def addColour():
    number = random.randint(0,3)
    if (number == 0):
        ledOrder.append('r')
    elif (number == 1):
        ledOrder.append('g')
    elif (number == 2):
        ledOrder.append('b')
    elif (number == 3):
        ledOrder.append('y')
    
def resetLED():
    ledR.off()
    ledG.off()
    ledB.off()
    ledY.off()
    
def playLoose():
    toggleLED('r')
    playTone(261)
    toggleLED('r')
    utime.sleep(0.1)
    toggleLED('r')
    playTone(261)
    toggleLED('r')
    utime.sleep(0.1)
    toggleLED('r')
    playTone(261)
    toggleLED('r')
    utime.sleep(0.1)
    
def playWelcome(mult):
    toggleLED('r')
    playTone(440, 0.3 / mult)
    toggleLED('g')
    playTone(523, 0.3 / mult)
    toggleLED('b')
    playTone(659, 0.3 / mult)
    toggleLED('y')
    playTone(783, 0.3 / mult)
    resetLED()

def gameLoop(difficulty = 1):
    playWelcome(difficulty)
    levelCounter = 0
    correct = 1
    while True:
        if (correct == 1):
            levelCounter += 1
            print("Difficulty:", difficulty,"Level:", levelCounter)
            addColour()
            utime.sleep(1)
        else:
            resetLED()
            ledOrder.clear()
            playLoose()
            break
        playOrder(difficulty)
        correct = userPlay()
    
resetLED()
while True:
    if (getInput(0) == 'r'):
        gameLoop()
    elif (getInput(0) == 'g'):
        gameLoop(2)
    elif (getInput(0) == 'b'):
        gameLoop(3)
    elif (getInput(0) == 'y'):
        gameLoop(4)
