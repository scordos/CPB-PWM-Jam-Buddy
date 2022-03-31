# do-re-mi
import time, pwmio, board, digitalio, math, neopixel
from analogio import AnalogIn
from adafruit_debouncer import Debouncer


# setup speaker for tone playing
tone = pwmio.PWMOut(board.SPEAKER, duty_cycle = 1500, frequency=440, variable_frequency=True)

speaker = digitalio.DigitalInOut(board.SPEAKER_ENABLE)
speaker.switch_to_output()

#Neopixels

pixels_num_of_lights = 10
pixels_pin = board.NEOPIXEL
pixels = neopixel.NeoPixel(pixels_pin, pixels_num_of_lights, brightness = .1, auto_write = True)

# setup buttons

buttonA_input = digitalio.DigitalInOut(board.BUTTON_A)
buttonA_input.switch_to_input(pull=digitalio.Pull.UP)
button_A = Debouncer(buttonA_input)

buttonB_input = digitalio.DigitalInOut(board.BUTTON_B)
buttonB_input.switch_to_input(pull=digitalio.Pull.UP)
button_B = Debouncer(buttonB_input)


# Notes
#From C0 to B8
notes = [16, 17, 18, 19, 21, 22, 23, 25, 26, 28, 29, 31, 33, 35, 37, 39, 41, 44, 46, 49, 52, 55, 58, 62, 65, 69, 73, 78, 82, 87, 93, 98, 104,
110, 117, 123, 131, 139, 147, 156, 165, 175, 185, 196, 208, 220, 233, 247, 262, 277, 294, 311, 330, 349, 370, 392, 415, 440, 466, 494, 523, 554,
587, 622, 659, 698, 740, 784, 831, 880, 932, 988, 1047, 1109, 1175, 1245, 1319, 1397, 1480, 1568, 1661, 1760, 1865, 1976, 2093, 2217, 2349, 2489,
2637, 2794, 2960, 3136, 3322, 3520, 3729, 3951, 4186, 4435, 4699, 4978, 5274, 5588, 5920, 6272, 6645, 7040, 7459, 7902]

root = 57 #440 or A4

#Mode Potentiometer
mode = AnalogIn(board.A6)
songmode = 1
changed = False

#Tempo Potentiometer
tempo = AnalogIn(board.A3)
bpm = 60 + tempo.value / (65520/100)
qNote = 60/bpm

#Note Functions
def play_Qnote(note):
    tone.frequency = notes[int(note)]
    speaker.value = True
    time.sleep(qNote)
    speaker.value = False


def play_28note(note):
    tone.frequency = notes[int(note)]
    speaker.value = True
    time.sleep((qNote/2)-.05)
    speaker.value = False
    time.sleep(.1)
    tone.frequency = notes[int(note)]
    speaker.value = True
    time.sleep((qNote/2)-.05)
    speaker.value = False

#Periferal Functions (Tempo and Mode pots)
def check_tempo():
    global bpm, qNote
    bpm = 60 + tempo.value / (65520/100)  #range of 60-160
    qNote = 60/bpm
    print("BPM: ", bpm)
    print("Quarter Note Duration: ", qNote)

def check_mode(): #Checks Mode Pot position
    global songmode
    if mode.value <= (65520/5):
        songmode = 1
        pixels.fill((100,0,0))
    elif mode.value <= (65520/4)*2:
        songmode = 2
        pixels.fill((255,0,255))
    elif mode.value <= (65520/4)*3:
        songmode = 3
        pixels.fill((0,0,255))
    else:
        songmode = 4
        pixels.fill((0,255,0))
    return songmode

"""def key_change():
    global root
    if button_A.fell:
        root -= 1
        print("Button A Pressed")
    elif button_B.fell:
        root += 1
        print("Button B Pressed")
    print(root)"""

def check_all():
    check_tempo()
    check_mode()

#Songs (One measure each)

def off(): #Mode 1
    time.sleep(qNote*4)
    check_all()

def bluesMelody1(chord):  #Mode 2
    play_28note(chord) #Root
    play_28note(chord+12) #Octave
    play_28note(chord+10) #b7th
    play_28note(chord+7) #5th

    check_all()
    if songmode != 2:
        changed = True


def bluesMelody2(chord): #Mode 3
    play_28note(chord+12) #Root
    play_28note(chord+3) #Root
    play_28note(chord+4) #Root
    play_28note(chord) #Root


    check_all()

def metronome(): #Mode 4
    #play_Qnote(68)
    time.sleep(qNote)
    play_Qnote(68)
    play_Qnote(68)
    play_Qnote(68)
    check_all()

def blues(key, song): #Mode 2 and 3
    four = key + 5
    five = key + 7
    chords = [key, four, five]
    structure = [0,0,0,0,1,1,0,0,2,1,0,1]
    if int(song) == 1:
        for i in structure:
            bluesMelody1(chords[i])

    else:
        for i in structure:
            bluesMelody2(chords[i])

def jukebox(mode):
    if mode == 1:
        off()
    elif mode == 2:
        blues(root, 1)
    elif mode ==3:
        blues(root, 2)
    else:
        metronome()

while True:
    print(songmode)
    jukebox(songmode) #Play song of mode







