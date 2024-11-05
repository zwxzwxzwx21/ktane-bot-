import copy
import os
#from vosk import Model, KaldiRecognizer
import pyaudio
import pyttsx3
import json
#import speech_recognition as sr
import pyautogui
import time
import numpy as np
from matplotlib import pyplot as plt
import cv2
import os
import cv2
import numpy as np
import pyautogui
import time

global parallel_port
parallel_port = False

def distance_to_colors(pixel):
    white = np.array([255, 255, 255])
    black = np.array([0, 0, 0])
    distance_to_white = np.linalg.norm(pixel - white)
    distance_to_black = np.linalg.norm(pixel - black)
    return distance_to_white, distance_to_black


def check_wdgets(x, y):
    global parallel_port

    check_array = ''


    # having 2 lookup tables for the savety, could use the second one for speed but its not worth the risk of it not
    # working when big battery and 2 batteries barely differ

    widgets_LUT = \
        {
            (255, 255, 135): 1,
            (255, 255, 166): 1,
            (151, 153, 143): 2,
            (130, 135, 136): 2,
            (156, 162, 165): 2,
            (36, 13, 16): "label",
            (43, 26, 29): "label",
            (77, 27, 28): "label",
            (39, 15, 16): "label",
            (78, 82, 81): "port plate",  # works on every position
            (78, 81, 81): "port plate",

        }
    # this one checks for batteries, battery

    # this one checks for labels and port plates

    numb_of_batteries = 0
    labels = []
    for i in range(5):
        dot_x, dot_y = 168 + i * 230, 79

        # Zczytaj piksel z ekranu w odpowiedniej pozycji
        screen_pixel_rgb = pyautogui.pixel(x + dot_x, y + dot_y)
        # print(f'Loop {i} | Pixel at ({dot_x}, {dot_y}):', screen_pixel_rgb)
        label_LUT = \
            {
                "0110101011001110101101101": "FRK",
                "0001101101000010110101101": 'A',
                "0000101100000010110101101": 'A',
                '0000101101000010110101101': 'A'
            }

        try:
            # Sprawdź wartość w `labels_LUT`
            labels_value = widgets_LUT[screen_pixel_rgb]

            # Zwiększ licznik baterii, jeśli etykieta to liczba
            if isinstance(labels_value, int):
                numb_of_batteries += labels_value

            # Warunek, jeśli etykieta to "label"
            if labels_value == "label":
                #print("label")

                # Sprawdzenie pikseli w odpowiedniej pozycji

                xx, yy = 2, 25
                #print(pyautogui.pixel(645 + i * 230 + xx, 34 + yy))

                # Jeśli piksel jest biały
                if pyautogui.pixel(645 + i * 230 + xx, 34 + yy) == (255, 255, 255):
                    # Kontynuacja rozpoznawania obrazu

                    check_array = ''
                    for j in range(5):
                        for k in range(5):
                            dot_x, dot_y = 3 + k * 4, 6 + j * 8
                            screen_pixel_rgb = pyautogui.pixel(745 + i * 230 + dot_x, 34 + dot_y)
                            # print(dot_x, dot_y, screen_pixel_rgb)

                            # Oblicz odległości od kolorów
                            distance_to_white, distance_to_black = distance_to_colors(np.array(screen_pixel_rgb))
                            closer_color = "white" if distance_to_white < distance_to_black else "black"

                            check_array += '0' if closer_color == "white" else '1'

                    #print(check_array)
                    if check_array in label_LUT:
                        if label_LUT[check_array] == "FRK":
                            labels.append("FRK")
                            #print("LIT FRK")
                        if label_LUT[check_array] == "A":

                            #print('pixel', pyautogui.pixel(725 + i * 230 + 1, 34 + 6))
                            if pyautogui.pixel(725 + i * 230 + 1, 34 + 6) == (210, 206, 191):
                                pass
                            else:
                                labels.append("CAR")
                                #print("car label")

            elif labels_value == "port plate" and parallel_port == False:
                #print("port plate")

                xx, yy = 80, 26

                #print(pyautogui.pixel(585 + i * 230 + xx, 20 + yy))
                if pyautogui.pixel(585 + i * 230 + xx, 20 + yy) == (255, 150, 217) or pyautogui.pixel(
                        585 + i * 230 + xx, 20 + yy) == (255, 150, 218):
                    parallel_port = True
                    #print("parallel port found")
                    break

        except KeyError:
            print(f"{check_array} not in LUT")

    #print(f'Number of batteries: {numb_of_batteries}')
    return labels,numb_of_batteries

def take_and_display_screenshot(serial,x, y, width, height):
    #screenshot = pyautogui.screenshot(region=(x, y, width, height))
    serial = serial
    #screenshot_np = np.array(screenshot)
    #my_image = cv2.cvtColor(screenshot_np, cv2.COLOR_RGB2BGR)
    check_array = ''
    number_LUT = {
        '001100011100010010111111100001': 'A',
        '111110100011111110100001111100': 'B',
        '011101100001100000100001011110': 'C',
        '011101100001100000100001011100': 'C',
        '111110100001100001100011111100': 'D',
        '111111100000111110100000111111': 'E',
        '111111100000111110100000100000': 'F',
        '011101100001100111100001011110': 'G',
        '011101100001100111100001011100': 'G',
        '100011100011111111100011100011': 'H',
        '011110001100001100001100011110': 'I',
        '011110001000001000001000011110': 'I',
        '000011000011000011100010011100': 'J',
        '000011000011000011100011011100': 'J',
        '100010101100111000100110100011': 'K',
        '100010101100111000100100100011': 'K',
        '100000100000100000100000111111': 'L',
        '110011110111101111100011100011': 'M',
        '110011111011101111100111100011': 'N',
        '111110100001111110100000100000': 'P',
        '111110100001111110100100100011': 'R',
        '011110100001100001100011011100': 'Q',
        '011110100010001110100011101110': 'S',
        '011111100011001110100011101110': 'S',
        '111111101001001000001000011110': 'T',
        '111111101101001100001100011110': 'T',
        '100011100011100011100011011100': 'U',
        '100001100011010010011100001100': 'V',
        '100001100001101111110110010010': 'W',
        '110111010110001100010110110111': 'X',
        '111110100110001000010011111111': 'Z',
        '111110100110001100010011111111': 'Z',

        '011110100011101001100011011100': '0',

        '001000111000001000001000011110': '1',
        '011110100011000110011011111111': "2",
        '011110100011001110100011011110': "3",
        '000100011100100100000100001111': '4',
        '000100011100100100000110001111': '4',
        '111110100000110011100011011100': '5',
        '011110100000100011100001011110': '6',
        '111111100010000100001000001000': '7',
        '011110100011011110100001011110': '8',
        '011110100011100011000011011100': "9"
    }
    # only number here, made on 3rd pos
    N_LUT = {

        '011110100011101001100011011100': '0',
        '001000111000001000001000011110': '1',
        '011110100011000110011011111111': "2",
        '011110100011001110100011011110': '3',
        '000100011100100100000110001111': '4',
        '111110100000110011100001011100': "5",
        '111110100000110011100011011100': '5',
        '011110100000100011100001011110': '6',
        '111111100010000100001000001000': '7',
        '011110100011011110100001011110': '8',
        '011110100011100011000011011100': '9',
        '011110100001100011000011011100': '9'
    }
    # ONLY ON 6 POS HERE
    N_LUT2 = {

        '011110100011101001110001011100': '0',
        '011110100011101001110011011100': '0',
        '001100111100001100001100011110': '1',
        '011110100011000110011011111111': '2',
        '011110100011001110100001011110': '3',
        '000110011110100110000110001111': '4',
        '111111100000110011100001011100': '5',
        '011110100000100011100001011110': '6',
        '111111100010000100001000001000': '7',
        '011110100011011110100001011110': '8',
        '011110100001110011000011011100': '9'

    }

    for j in range(5):
        for i in range(6):
            dot_x, dot_y = 4 + i * 4, 2 + j * 8
            #my_image[dot_x, dot_y] = (0, 0, 255)
            screen_pixet_rgb = pyautogui.pixel(x + dot_x, y + dot_y)
            screen_pixet_rgb = pyautogui.pixel(x + dot_x, y + dot_y)

            distance_to_white, distance_to_black = distance_to_colors(np.array(screen_pixet_rgb))
            closer_color = "white" if distance_to_white < distance_to_black else "black"
            if closer_color == "white":
                check_array += '0'
            else:
                check_array += '1'

    try:
        if x != 1825:
            if x != 1915:
                serial += number_LUT[check_array]
            else:
                serial +=N_LUT2[check_array]
        else:
            serial +=N_LUT[check_array]
    except KeyError:
        print(check_array, 'not in LUT')


    return serial
# can check for second and third leter in labels because __K is only for FRK and _A_ is only for CAR, but i think it is
# better to ccheck for 3rd pos only and then just check one pixel to determine if the second position is A or L if third one is R.
# i think doing it just like serial number is good, just use less pixels to save time


# to do
# widgets image recognition: we can now detect how many widgets are there and based on that we can determine
# the position we will be checking numbers using lookup table, for example, if we have 5 widgets, we check position 1651
# and then add 30 pixels each time we take a screenshot and compare it with pictures in the folder, then we can
# just extract signs from file name and use those, (if this turns out to kinda fail because comapring images will
# be fucked due to images being too long in height, just make them shorter and set 6 pixels to check for Q sign instead)
# TRY  TO KEEP IMAGE RECOGNITION SMALL, CHECK PIXELS OVER IMAGES, IT TAKES MUCH LESS TIME!
# ideas for modules to not forget and have them in one place:
# button:
# button is rather simple, one pixel for color and you can make something like this: check one pixel for word detonate
# because its the longest, then check another pixel for some shorter word, or any word, just check the pixel right so
# its definitely covered only by one of the remainign words and that way you can use image regocnition from 2-5 times rather
# than using it 5, saving time.stripe is simply just check one pixel and then for timer i think the best idea is
# to simply make 7 pixel checks for each sign in clock and just use LUT
# keys: optimizing image recognition might be hard, id honeslty just take entire pictures and fuck it, it wont save like more than a second anyway
# rest should be trivial
# simon says:
# idk how to check strikes, ig use the twitch thing for it, but you should not be striking at all so idk if there is a pointlol.
#make checks every 0.2 seconds on 4 pixels and when they turn different color, indicating flashing, just go for it
# i guess later would be better to have less checks cuz the module is now more normalized, and you can wait specified amount
# of time after a button press like: you make one press, and then you make a check exactly one second later when another button should be at its peak flash color
# take screen and go with it, keep in mind that image rec might be delayed!!!!!!!!!
# maze:
# you can optimize it by checking only selected green circles, but the rest should be really easy, you have start pos and ending pos, you even have
# scrript that can solve maze so its not hard lol just do it my boi
# memory:
# minor pixel checks to save some time, and optimized button presses for some more time save, the faster the better
# .

# IMPORTANT NOTES, PREVENTION OF POTENTIAL ERRORS: ############################################
# if you are doing button, make some check that would indicate if you have seconds left or minutes, for example you can just
# run your own times and try to sync it up which would be good idea, or something worse, you can check if there are numbers higher than 5 in
# first position in seconds and maybe check if the first number of minutes is higher than 1, cuz i think there are no bombs that give you
# 20 minutes, so it should be 1 or 0 always.

# for 5 widgets (only x varies)
# pos of 6th serial number : 1801 + 26 | 61 + 45
# pos of 5th serial number : 1771
# pos of 4th serial number : 1741
# pos of 3th serial number : 1711
# pos of 2th serial number : 1681
# pos of 1th serial number : 1651 spaced 30px
# for 7 widgets, start at 1879
# for 6 widgets, start at 1765
# for 4 widgets, start at 1535
# fro 3 widgets, start at 1420

#IF PIXELS ARE OFF, ZOOM BY ONE
def check_pixel(x,y):
    a = pyautogui.pixel(x, y)
    print(a)
    return a

serial = ''
batteries = -1 # nothing is checked yet
while True:
    import win32api
    import win32con
    import time
    import pygetwindow as gw
    import keyboard
    import winsound
    import threading # to use multiple winsounds
    window = gw.getWindowsWithTitle("Keep Talking and Nobody Explodes")


    if keyboard.is_pressed(']'):
        winsound.PlaySound("SystemHand", winsound.SND_ASYNC)
        time.sleep(0.1)
        winsound.PlaySound("SystemHand", winsound.SND_ASYNC)
        time.sleep(0.1)
        winsound.PlaySound("SystemHand", winsound.SND_ASYNC)
        time.sleep(0.1)
        winsound.PlaySound("SystemExit", winsound.SND_ALIAS)

        break
    if window:
        window[0].activate()
        time.sleep(1)
        pyautogui.click(1200, 1000)


    #win32api.SetCursorPos((1200, 1000))
    # Click at the position
    #win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, 0, 0)
    #win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, 0, 0)
    #loop for serial number
    if len(serial) != 6:
        for i in range(6):
            y = 61
            if i == 0:
                x = 1765
            elif i == 1:
                x = 1795
            elif i == 2:
                x = 1825
            elif i == 3:
                x = 1855
            elif i == 4:
                x = 1885
            elif i == 5:
                x = 1915
            width, height = 176, 45
            serial = take_and_display_screenshot(serial,x, y, width, height)
    #FLAG for widgets
    if batteries == -1:
        labels, batteries = check_wdgets(600, 0)
        print(f"serial number: {serial} | batteries: {batteries} | labels: {labels} | parallel port {parallel_port}")
    #loop to check 6 pixels for position of the modules
    module_screenshot = pyautogui.screenshot(region=(800,240,1300,600))
    module_screenshot_np = np.array(module_screenshot)
    xx,yy = 150,15 # by how much shift pixels to check more or less the same pos (its normalized anyway, just has to be on the light to make things easier)
    test_image = cv2.cvtColor(module_screenshot_np, cv2.COLOR_BGR2RGB)
    #lut for colors that indicate we have a module
    modules_LUT = [(33, 31, 28),(45, 41, 36),(0, 1, 0),(35, 29, 25),(22, 22, 20),(141, 130, 114),
                   (33, 30, 26),(45, 42, 36),(35, 31, 26),(21, 21, 20),
                   (33, 30, 28),(22, 21, 20),(31, 28, 26),(37, 33, 30),(21, 21, 19),(139, 128, 113),(31, 28, 25)
                   ]

    # accesing modules on demand:
    # have a tuble that will have things stored in ("module name",x pos, y pos,bool which would tell if front or back side).
    module_array_front = []
    module_array_back = []
    #these 2 will be filled with exact name of module and its pos, could do that in upper arrays but idc
    modules_in_front = []
    modules_in_back = []
    front_side = 1 # our bool
    is_on_flipped = False # bool that keeps track of all the 180 rotations
    # VALUES HERE MIGHT BE USEFULL; FOR ACCESIING MODULES LATER ON
    for loop in range(2):
        if loop > 0:
            front_side = 0

        for x in range(3):
            for y in range(2):
                test_image[yy+y*550,xx+x*550] = (0,0,255)
                print(pyautogui.pixel(800+x*550+xx,yy+ 240+y*550))
                if pyautogui.pixel(800+x*550+xx,yy+ 240+y*550) in modules_LUT:

                    #print(f"we have module at ")

                    tuple = ("X module",x,y)
                    if front_side == 1:
                        module_array_front.append(tuple)
                    else:
                        module_array_back.append(tuple)
                else: print(f' not in table {pyautogui.pixel(800+x*550+xx,yy+ 240+y*550)}')
        if front_side == 1:
            pyautogui.dragTo(700,None,0.12,button="right")
            pyautogui.click(button='right')
            time.sleep(0.1)
            pyautogui.click(1200,1000,button='left')
            is_on_flipped = True
        time.sleep(2.5)

    print(module_array_back,"back \n", module_array_front, "front")
    # this one is what pixel color is what module

    type_of_module_LUT = \
        {
            (18, 24, 39) : "password",
            (165, 150, 132) : 'sequence',
            (24, 70, 90) : "maze",
            (43, 49, 67) : "simon",
            (221, 208, 188) : "keypads",
            (92, 89, 84): "memory",
        }
    type_of_module_LUT2 = \
    {
        (67, 66, 79) : "sequence",
        (87, 91, 102) : "morse",
        (40, 36, 44) : "whos on first",
        (99, 110, 137): "wires",
    }
    # if not in any then its button
    pixel_x,pixel_y=670,560 # those are the values to change for pixels checks, they wont be needed
    # later so dw changing as much as needed for testing purposes
    for module in module_array_back: # back because we are on the back
        # module is ("name",x,y)

        print(module)
        pyautogui.click(650+module[1]*550,400+module[2]*550)
        #image to show what im clicking at more or less
        '''press_position = pyautogui.screenshot(region=(650+module[1]*550, 400+module[2]*550, 50, 50))
        press_position = np.array(press_position)
        press_position = cv2.cvtColor(press_position, cv2.COLOR_BGR2RGB)
        cv2.imshow("test",press_position)
        cv2.waitKey(0)'''
        time.sleep(0.5)
        single_module_image = pyautogui.screenshot(region=(800, 240, 1300, 1200))
        single_module_image_np = np.array(single_module_image)
        single_module_image_with_pixels = cv2.cvtColor(single_module_image_np, cv2.COLOR_BGR2RGB)
        single_module_image_with_pixels[pixel_y,pixel_x] = (0, 0, 255)

        print("pixel of module: " ,pyautogui.pixel(pixel_x+800,240+pixel_y))
        if pyautogui.pixel(pixel_x+800,240+pixel_y) in type_of_module_LUT:
            print(type_of_module_LUT[pyautogui.pixel(pixel_x+800,240+pixel_y)], ' module')
        cv2.imshow("test", single_module_image_with_pixels)
        cv2.waitKey(0)
        pyautogui.click(button = "right")
        time.sleep(0.5)

    pyautogui.dragTo(700, None, 0.12, button="right")
    pyautogui.click(button='right')
    time.sleep(0.1)
    pyautogui.click(1200, 1000, button='left')
    is_on_flipped = False
    time.sleep(1)
    #checking modules on other side
    for module in module_array_front:
        print(module)
        pyautogui.click(650 + module[1] * 550, 400 + module[2] * 550)
        time.sleep(0.5)
        single_module_image = pyautogui.screenshot(region=(800, 240, 1300, 1200))
        single_module_image_np = np.array(single_module_image)
        single_module_image_with_pixels = cv2.cvtColor(single_module_image_np, cv2.COLOR_BGR2RGB)
        single_module_image_with_pixels[pixel_y, pixel_x] = (0, 0, 255)

        if pyautogui.pixel(pixel_x + 800, 240 + pixel_y) in type_of_module_LUT:
            print(type_of_module_LUT[pyautogui.pixel(pixel_x + 800, 240 + pixel_y)], ' module')
        print("pixel of module: ", pyautogui.pixel(pixel_x + 800, 240 + pixel_y))
        cv2.imshow("test", single_module_image_with_pixels)
        cv2.waitKey(0)
        pyautogui.click(button="right")
        time.sleep(0.5)
    print(f"printing ciapka at {module[1]*550}, {module[2]*550}")


    #single_module_image_with_pixels[yy + y , xx + x ] = (0, 0, 255)


    #cv2.imshow("test", test_image)
    cv2.waitKey(0)
    time.sleep(999)
'''
speed_up = 225 # speed and slowed down voice for bot to read faster or slower if needed
slow_down = 175

positive_answers = ['yes','s','this','us','ps','as','vince']
#potential bugs n todo:
#uhh i think when serial is not long enough it kinda fucks it over unsure tho
#not really a bug but sth that can be changed, on password gamemode i use double brackets because i tought there was a bug, you can remove one of the brackets but you would need to
#remove the [0] part  from rowX[0][_] and it should make stuff slightly cleaner, and also you wont really have to work on arrays inside of arrays, wont really mean that uch
# but to be fair could be changed later to make the code cleaner or so
#another thing, could be fixed already but idk, when bot wont understand 'yes' or 'wrong' it could go to say_('module') line which is really bad because it loses all progress
# if the error is still there FUCKING FIX IT
# make the bot read passwords faster - DONE
# connect numbers and colors in wires so you say number+  colors, should save several seconds of time cuz bot thinks a lot
#
# GAMES TO REPLICATE
#region
###IMPLEMENTED
#BUTTON - WORKS 100% NO ERRORS FOUND
#PASSWORD - WORKS 100% NO ERRORS FOUND
#WIRES - HAVENT HAD AN ERROR RELATED TO SERIAL NUMBER, NEED TO TESTCASE THAT!!!
#COMPLICATED (COMPLICATED WIRES) - PROB NEXT ONE, REALLY EASY ^^^
#SEQUENCE (WIRE SEQUENCE) - NEED TO TALK SLOWLY, LAST PUZZLE NOT REALLY DOABLE WHEN BOT TAKES OVER 30 SECONDS TO THINK XD
#SIMON SAYS - PISS EASY JUST ASK FOR COLORS STRIKES N SHIT, AND CHECK FOR VOWELS
#MEMORY - JUST SAY 2 THINGS, MAIN NUMBER AND WHAT YOURE PRESSING LIKE 'PRESSING 2' AND YOU SHOULD BE DONE, GL WITH THE BOT RECOGNIZING IT EVERY TIME CORRECTLY THO XD
#MORSE - LEARN HOW TO READ RETSDFASDFDASAFDSSDFA
#KEYPADS - WELL TOU GONNA DO STH LIKE A SIGN THAT LOOKS LIKE A  C JUST IS A C AND BOT WILL GET IT YE???
#KNOBS - SEEMS HARD
###UNIMPLEMENTED
#MAZE - FUCKING HELL NAH
#FIRST - FOR EMPTY SAY EMPTY, I THINK THE BEST THING IS TO USE SOME FUCKED UP PRONOUNCE TO WORK THIS OUT (THEIR , THERE = THERE, DEER = THEIR XD, TRY USING NUMBERS TOO, HONESLT YIT SEEMS THE WORST!!!!!!!!!!)

#endregion
#code below changes the voice from polish to english
#region
print("Available microphones:")
for index, name in enumerate(sr.Microphone.list_microphone_names()):
    print(f"Microphone with index {index}: {name}")

engine = pyttsx3.init()
engine.setProperty('read',210)
voices = engine.getProperty('voices')
for voice in voices:
    if "zira" in voice.id.lower():  # Use the ID for Microsoft Zira (English)
         engine.setProperty('voice', voice.id)
#endregion
info_dict = {} #this one stores values | CEREAL = SERIAL IDCCCCC

debug = True
#model = Model('A:\\ktane bot\\vosk-model-en-us-0.22')
#recognizer = KaldiRecognizer(model, 16000)
recognizer = sr.Recognizer()
p = pyaudio.PyAudio()
stream = p.open(format=pyaudio.paInt16, channels=1, rate=16000, input=True,frames_per_buffer=8192)
stream.start_stream()



mode = 'test'
numbers = {'zero': 0, 'one': 1, 'two': 2, 'three': 3, 'four': 4, 'five': 5, 'six': 6, 'seven': 7, 'eight': 8, 'nine': 9,
           'for': 4, 'aids': 8, 'aid': 8, 'tree': 3, 'free': 3, 'wow':1,'too':2,'poor':4}

def remove_the(text):
    a = text.replace('the ','')
    #a = text.replace('the','')
    return a

def convert_json(json_text):
    text = json.loads(json_text)
    return text['text']

def say_(text):
    engine = pyttsx3.init()
    engine.say(text)
    engine.runAndWait()



def ask_for(key):
    conf = False
    while True:
        if conf == False:
            say_(f'{key} waiting')
            res = listening()
            resp = res.replace('the','')
            response = resp.replace(' ','')
            if response in numbers:
                response = numbers[response]
            print(f"{key}, {response}, correct?")


            return response

            conf = True #makes the bot remember the batteries if it wont understand 'yes' as an answer, you dont have to say it again

def wait_():
    while True:
        response = listening()
        response = remove_the(response)
        if len(response):
            return response
        else: continue
def ask_for_advanced(key):
    #ports
    # for ports its cereal = serial, RCA (stereo),DVI,parallel,ps,rj
    if key == 'edgework':
        lights = []
        port_return = []
        say_('parallel port?')
        answer_ = listening()
        answer = remove_the(answer_)
        print(answer)
        if answer == 'no' or answer == 'none' or answer =='non':
            port_return = []
        elif answer in positive_answers:
            port_return = ['parallel']
            print(port_return)
        say_('lit car?')
        answer_ = listening()
        answer = remove_the(answer_)
        print(answer)
        if answer == 'no' or answer == 'none' or answer =='non':
            pass
        elif answer in positive_answers:
            light = ('car','yes')
            lights.append(light)
            print(lights)
        say_('lit frk?')
        answer_ = listening()
        answer = remove_the(answer_)
        print(answer)
        if answer == 'no' or answer == 'none' or answer == 'non':
            pass
        elif answer in positive_answers:
            light = ('frk', 'yes')
            lights.append(light)
            print(lights)



        return lights,port_return


    elif key == 'serial':
        list_ = []
        while True:

            say_(f'{key}')
            answer = listening()

            if answer:
                clean_answer = answer.replace('the', '')
                print(clean_answer,'answer')
                indicator = ''
                group = clean_answer.split()  # group ofwords from answer
                print(group)
                try:
                    for i in range(6):
                        if group[i] not in numbers:
                            indicator += group[i][0]
                        else:
                            indicator += str(numbers[group[i]])
                except IndexError:
                    ask_for_advanced(key)

                serial = (indicator)
                if len(serial) == 6:
                    say_(f"{' '.join(indicator)}")
                else: continue
                print(f"{key}, {serial}, correct?")

                confirm = wait_()

                if confirm == 'no':
                    print(serial)
                    #say_(f'{key} ')
                    list_ = []

                elif confirm == key:
                    print(serial)
                    return ask_for_advanced(key)

                elif confirm in positive_answers:
                    print(list_)
                    return serial
                    break

        return serial
def edgework():

    say_('edgework')
    lights_list =[]
    answer = listening()
    port_to_return = ''
    answer = remove_the(answer)
    answer = answer.split(' ')
    if len(answer) == 4:
        if answer[3] in numbers:
            batteries = numbers[answer[3]]
        else:
            edgework()
        for answer_number in range(3):
            if answer[answer_number] in positive_answers:
                if answer_number == 0:
                    port_to_return = 'parallel'
                elif answer_number == 1:
                    light = ('car','yes')
                    lights_list.append(light)
                elif answer_number == 2:
                    light = ('frk','yes')
                    lights_list.append(light)


    else:
        edgework()
    if batteries == None: batteries = 2
    return port_to_return, lights_list, batteries
def password(rows_done,r1,r2,r3,r4,r5):
    row1 = r1
    row2 = r2
    row3 = r3
    row4 = r4
    row5 = r5
    password_LUT = ['about','after','again','below','could','every', 'first', 'found', 'great', 'house',
'large', 'learn', 'never', 'other', 'place',
'plant', 'point', 'right', 'small', 'sound',
'spell', 'still', 'study', 'their', 'there',
'these', 'thing', 'think', 'three', 'water',
'where', 'which', 'world', 'would', 'write']

    if rows_done == 'one':
        say_('password')
        letters = wait_()
        letters_replaced = letters.replace('the ', '')
        letters_replaced = letters.replace('why', 'y')
        letters_replaced = letters.replace('you', 'u')
        letters_replaced = letters.replace('eye', 'i')
        letters_replaced = letters.replace('new', 'u')
        letters_replaced = letters.replace('see', 'c')
        letters_replaced = letters.replace('sea', 'c')
        letters_group = letters_replaced.split(' ')
        try:
            row_one = [letters_group[0][0],letters_group[1][0],letters_group[2][0],letters_group[3][0],letters_group[4][0],letters_group[5][0]]
        except IndexError:
            print(rows_done, 'wrong')
            password('one',r1,r2,r3,r4,r5)
        row1 = row_one
        engine.setProperty('rate', speed_up)

        say_(f'{letters_group[0][0]} {letters_group[1][0]} {letters_group[2][0]} {letters_group[3][0]} {letters_group[4][0]} {letters_group[5][0]}, correct?')
        print(f'{letters_group[0][0]} {letters_group[1][0]} {letters_group[2][0]} {letters_group[3][0]} {letters_group[4][0]} {letters_group[5][0]}, correct?')

        engine.setProperty('rate', 200)
        answer_ = wait_()
        answer = remove_the(answer_)
        print(answer)
        if answer in positive_answers:

            print(row1)
            rows_done = 'two'

        elif answer == 'wrong':
            r1 = []
            password('one',r1,r2,r3,r4,r5)
        else: r1 = [];password('one',r1,r2,r3,r4,r5)
    if rows_done == 'two':
        say_('row two')
        letters = wait_()
        letters_replaced = letters.replace('the ', '')
        letters_replaced = letters.replace('why', 'y')
        letters_replaced = letters.replace('you', 'u')
        letters_replaced = letters.replace('eye', 'i')
        letters_replaced = letters.replace('new', 'u')
        letters_replaced = letters.replace('see', 'c')
        letters_replaced = letters.replace('sea', 'c')
        letters_group = letters_replaced.split(' ')
        try:
            row_two = [letters_group[0][0],letters_group[1][0],letters_group[2][0],letters_group[3][0],letters_group[4][0],letters_group[5][0]]
        except IndexError:
            print(rows_done, 'wrong')
            print('function : two',r1,r2,r3,r4,r5)
            password('two',r1,r2,r3,r4,r5)
        row2 = row_two
        say_(f'{letters_group[0][0]} {letters_group[1][0]} {letters_group[2][0]} {letters_group[3][0]} {letters_group[4][0]} {letters_group[5][0]}, correct?')
        print(f'{letters_group[0][0]} {letters_group[1][0]} {letters_group[2][0]} {letters_group[3][0]} {letters_group[4][0]} {letters_group[5][0]}, correct?')
        answer_ = wait_()
        answer = remove_the(answer_)
        print(answer)
        if answer in positive_answers:
            solutions = 0
            solution_array = []
            for i in range(6):
                for j in range(6):
                    #print(row1, row2)
                    word = row1[i] + row2[j]
                    for table in password_LUT:
                        if word == table[:2]:
                            solutions += 1
                            solution_array.append(table)
            if solutions == 1:
                say_(f'{solution_array}')
                print(solution_array)
                return
            else: print(solution_array)
            print(row2)
            rows_done = 'three'

        elif answer == 'wrong':
            r2 = []
            password('two',row1,row2,row3,row4,row5) # apparently used to be wrong but i dont give a fuck, prob still wrong xd, applies to others
        else: r2 = [];password('two',r1,r2,r3,r4,r5)
    if rows_done == 'three':
        say_('row three')
        letters = wait_()
        letters_replaced = letters.replace('the ', '')
        letters_replaced = letters.replace('why', 'y')
        letters_replaced = letters.replace('you', 'u')
        letters_replaced = letters.replace('eye', 'i')
        letters_replaced = letters.replace('new', 'u')
        letters_replaced = letters.replace('see', 'c')
        letters_replaced = letters.replace('sea', 'c')
        letters_group = letters_replaced.split(' ')
        try:
            row_three =[letters_group[0][0],letters_group[1][0],letters_group[2][0],letters_group[3][0],letters_group[4][0],letters_group[5][0]]
        except IndexError:
            print(rows_done, 'wrong')
            password('three',r1,r2,r3,r4,r5)
        row3 = row_three
        engine.setProperty('rate',speed_up)
        say_(f'{letters_group[0][0]} {letters_group[1][0]} {letters_group[2][0]} {letters_group[3][0]} {letters_group[4][0]} {letters_group[5][0]}, correct?')
        print(f'{letters_group[0][0]} {letters_group[1][0]} {letters_group[2][0]} {letters_group[3][0]} {letters_group[4][0]} {letters_group[5][0]}, correct?')
        engine.setProperty('rate', 200)
        answer_ = wait_()
        answer = remove_the(answer_)
        print(answer)
        if answer in positive_answers:
            solutions = 0
            solution_array = []
            for i in range(6):
                for j in range(6):
                    for k in range(6):
                        #print(row1,row2,row3)
                        word = row1[i] + row2[j] + row3[k]
                        for table in password_LUT:
                            if word == table[:3]:
                                solutions += 1
                                solution_array.append(table)
            if solutions == 1:
                say_(f'{solution_array}')
                print(solution_array)
                return
            else:
                print(solution_array)
            print(row3)
            rows_done = 'four'

        elif answer == 'wrong':
            r3 = [];password('three',row1,row2,row3,row4,row5)
        else: r3 = [];password('three',row1,row2,row3,row4,row5)
    if rows_done == 'four':
        say_('row four')
        letters = wait_()
        letters_replaced = letters.replace('the ', '')
        letters_replaced = letters.replace('why', 'y')
        letters_replaced = letters.replace('you', 'u')
        letters_replaced = letters.replace('eye', 'i')
        letters_replaced = letters.replace('new', 'u')
        letters_replaced = letters.replace('see', 'c')
        letters_replaced = letters.replace('sea', 'c')
        letters_group = letters_replaced.split(' ')
        try:
            row_four = [letters_group[0][0],letters_group[1][0],letters_group[2][0],letters_group[3][0],letters_group[4][0],letters_group[5][0]]
        except IndexError:
            print(rows_done, 'wrong')
            password('four',r1,r2,r3,r4,r5)
        row4 = row_four
        engine.setProperty('rate', speed_up)
        say_(f'{letters_group[0][0]} {letters_group[1][0]} {letters_group[2][0]} {letters_group[3][0]} {letters_group[4][0]} {letters_group[5][0]}, correct?')
        print(f'{letters_group[0][0]} {letters_group[1][0]} {letters_group[2][0]} {letters_group[3][0]} {letters_group[4][0]} {letters_group[5][0]}, correct?')
        engine.setProperty('rate', 200)
        answer_ = wait_()
        answer = remove_the(answer_)
        print(answer)
        if answer in positive_answers:
            solutions = 0
            solution_array = []
            for i in range(6):
                for j in range(6):
                    for k in range(6):
                        for l in range(6):
                            #print(row1, row2, row3,row4)
                            word = row1[i] + row2[j] + row3[k] + row4[l]
                            for table in password_LUT:
                                if word == table[:4]:
                                    solutions += 1
                                    solution_array.append(table)
            if solutions == 1:
                say_(f'{solution_array}')
                print(solution_array)
                return
            else:
                print(solution_array)
            print(row4)
            rows_done = 'five'

        elif answer == 'wrong':
            r4 = [];password('four',r1,r2,r3,r4,r5)
        else: r4= [];password('four',r1,r2,r3,r4,r5)
    if rows_done == 'five':
        say_('row five')
        letters = wait_()
        letters_replaced = letters.replace('the ', '')
        letters_replaced = letters.replace('why', 'y')
        letters_replaced = letters.replace('you', 'u')
        letters_replaced = letters.replace('eye', 'i')
        letters_replaced = letters.replace('new', 'u')
        letters_replaced = letters.replace('see', 'c')
        letters_replaced = letters.replace('sea', 'c')
        letters_group = letters_replaced.split(' ')
        try:
            row_five = [letters_group[0][0], letters_group[1][0], letters_group[2][0],letters_group[3][0], letters_group[4][0], letters_group[5][0]]
        except IndexError:
            print(rows_done,'wrong')
            password('five',r1,r2,r3,r4,r5)
        row5 = row_five
        engine.setProperty('rate', speed_up)
        say_(f'{letters_group[0][0]} {letters_group[1][0]} {letters_group[2][0]} {letters_group[3][0]} {letters_group[4][0]} {letters_group[5][0]}, correct?')
        print(f'{letters_group[0][0]} {letters_group[1][0]} {letters_group[2][0]} {letters_group[3][0]} {letters_group[4][0]} {letters_group[5][0]}, correct?')
        engine.setProperty('rate', 200)
        answer_ = wait_()
        answer = remove_the(answer_)
        print(answer)
        if answer in positive_answers:
            print(r1,r2,r3,r4,r5)
            for i in range(6):
                for j in range(6):
                    for k in range(6):
                        for l in range(6):
                            for m in range(6):
                                if debug:
                                    print(i,j,k,l,m)
                                    if len(row5) < 6: say_('error')
                                    print(row1[i] , row2[j] , row3[k] , row4[l] , row5[m])
                                    print(row5)
                                    print(row4)
                                word = row1[i] + row2[j] + row3[k] + row4[l] + row5[m]
                                if word in password_LUT:
                                    say_(word)
                                    return
        elif answer == 'wrong':
            r5 = []
            password('five',r1,r2,r3,r4,r5)
        else:
            r5 = []
            password('five', r1, r2, r3, r4, r5)

def wires(wires_done,wire_numb):
    # funciton takes argument to skip past first part if you fuck up colors
    wire_number = wire_numb
    engine.setProperty('rate', 235)
    if wires_done == False:
        say_('wires numbers')

        wire_number_pre = wait_()
        if wire_number_pre in numbers:
            wire_number = numbers[wire_number_pre]
    say_('colors')
    colors = wait_()
    colors_replaced2 = colors.replace('the ', '')
    colors_replaced = colors_replaced2.replace('read', 'red')
    colors_group = colors_replaced.split(' ')
    if len(colors_group) != wire_number:
        print(colors_group, wire_number)
        say_('wrong colors')
        wires(True,wire_number)


    answer_ = 'yes'
    answer = remove_the(answer_)
    if answer in positive_answers:
        if wire_number == 3:
            if 'red' not in colors_group:
                say_('cut second')
                return
            elif colors_group[-1] == 'white':
                say_('cut last')
            elif colors_group.count('blue') > 1:
                say_('cut last blue')
            else: say_('cut last')
        elif wire_number == 4:
            for i in range(1,7):
                if serial[-i].isdigit():
                    last_int = int(serial[-i]);
                    break

            if last_int % 2 == 1 and colors_group.count('red')>1: say_('cut last red')
            elif colors_group.count('red') == 0 and colors_group[-1] == 'yellow': say_('cut first')
            elif colors_group.count('blue') == 1: say_('cut first')
            elif colors_group.count('yellow') > 1: say_('cut last')
            else: say_('cut second')
        elif wire_number == 5:
            for i in range(1, 7):
                print(serial)
                print(serial[-i])
                if serial[-i].isdigit():
                    print('is digit')
                    last_int = int(serial[-i]);
                    break
            if last_int % 2 == 1 and colors_group[-1] =='black': say_('cut fourth')
            elif colors_group.count('red') == 1 and colors_group.count('yellow') > 1: say_('cut first')
            elif colors_group.count('black') == 0: say_('cut second')
            else: say_('cut first')
        elif wire_number == 6:
            for i in range(1, 7):
                if serial[-i].isdigit():
                    last_int = int(serial[-i]);
                    break
            if last_int % 2 == 1 and colors_group.count('yellow') == 0: say_('cut third')
            elif colors_group.count('yellow') == 1 and colors_group.count('white') > 1: say_('cut fourth')
            elif colors_group.count('red') == 0: say_('cut last')
            else: say_('cut fourth')
    elif answer == 'wrong':
        wires(True,wire_number)
    else:
        wires(True,wire_number)
    engine.setProperty('rate',200)
    return
#password('one',[],[],[],[],[])
#5:["h" ,"v" ,"z" ,"c" ,"g","t"] 3:["z" ,"g" ,"f" ,"k" ,"l", "a"],4:["h" ,"v" ,"z" ,"c" ,"g","t"] 1: ["a", "o", "p", "y", "t", "u"],2:["z", "l", "u" ,"o", "a", "h"]
def complicated():
    say_('complicated')
    # idea basically separete wired by next and make bot just say, cut,skip...
    wires = wait_()
    wires_replaced2 = wires.replace('the ', '')
    wires_replaced3 = wires_replaced2.replace('read', 'red')
    wires_replaced4 = wires_replaced2.replace('lead', 'lit')
    wires_replaced = wires_replaced4.replace('start', 'star')
    wires_group = wires_replaced.split(' ')
    wire_desc = []
    things_to_do = [] # this one is read at the end quikly to save time
    is_even = False
    for signs in serial:
        try:
            # int(signs)
            last_int = int(signs)
        except ValueError:
            continue
    if last_int % 2 == 0:
        is_even = True
    for words in wires_group:
        print(wires_group)
        if words == 'next':
            print(wire_desc)
            if 'lit' in wire_desc:
                if 'red' not in wire_desc and 'blue' not in wire_desc and 'star' not in wire_desc:
                    print('LIT | NOT red | NOT blue | NOT star')
                    things_to_do.append('skip') # right D
                elif 'blue' in wire_desc and 'parallel' in port and 'red' not in wire_desc and 'star' not in wire_desc:
                    print('LIT | NOT red | blue | NOT star',f' ports: {port}','cut')
                    things_to_do.append('cut')# right P
                elif 'red' not in wire_desc and 'blue' not in wire_desc and 'star' in wire_desc and batteries > 1:
                    print('LIT | NOT red | NOT  blue | star', f' batteries: {batteries}','cut')
                    things_to_do.append('cut')# bottom B
                elif 'red' in wire_desc and 'blue' not in wire_desc  and batteries > 1:
                    print('LIT | red | NOT  blue ', f' batteries: {batteries}','cut')
                    things_to_do.append('cut') # star does not matter here, making it 2 | right down B
                elif 'blue' in wire_desc and 'parallel' in port and 'red' not in wire_desc and 'star' in wire_desc:
                    print('LIT | NOT red | blue | star', f' ports: {port}','cut')
                    things_to_do.append('cut') # left down P
                elif 'red' in wire_desc and 'blue' in wire_desc and is_even == True and 'star' not in wire_desc:
                    print('LIT | red | blue | NOT star', f' is even?: {is_even}','cut')
                    things_to_do.append('cut') # middle right S
                elif 'star' in wire_desc and 'red' in wire_desc and 'blue' in wire_desc:
                    print('LIT | red | blue | star')
                    things_to_do.append('skip') # middle D
                else:
                    things_to_do.append('skip')
            else:
                if 'blue' not in wire_desc and 'red' not in wire_desc and 'star' not in wire_desc:
                    print('NOT LIT | NOT red | NOT blue | NOT star','cut')
                    things_to_do.append('cut') # upper C
                elif 'blue' in wire_desc and 'star' not in wire_desc and 'red' not in wire_desc and is_even == True:
                    print('NOT LIT | NOT red | blue | NOT star', f'is even?: {is_even}'),'cut'
                    things_to_do.append('cut') # upper right S
                elif 'blue' in wire_desc and 'star' not in wire_desc and 'red' in wire_desc and is_even == True:
                    print('NOT LIT | red | blue | NOT star', f'is even?: {is_even}','cut')
                    things_to_do.append('cut') # middle S
                elif 'blue' not in wire_desc and 'star' not in wire_desc and 'red' in wire_desc and is_even == True:
                    print('NOT LIT | red | NOT blue | star', f'is even?: {is_even}','cut')
                    things_to_do.append('cut') # upper left S
                elif 'blue' in wire_desc and 'star' in wire_desc and 'red' in wire_desc and 'parallel' in port:
                    print('NOT LIT | red | blue | star', f'port: {port}','cut')
                    things_to_do.append('cut') # middle left P
                elif 'red' not in wire_desc and 'blue' in wire_desc and 'star' in wire_desc:
                    print('NOT LIT | NOT red | blue | star')
                    things_to_do.append('skip') # bottom left D
                elif 'red' not in wire_desc and 'blue' not in wire_desc and 'star' in wire_desc:
                    print('NOT LIT | NOT red | NOT blue | star','cut')
                    things_to_do.append('cut') # middle left C
                elif 'red' in wire_desc and 'blue' not in wire_desc and 'star' in wire_desc:
                    print('NOT LIT | red | NOT blue | star','cut')
                    things_to_do.append('cut') # upper left C
                else:
                    things_to_do.append('skip')
            wire_desc = []
        else:
            wire_desc.append(words)
    for instruction in things_to_do:
        engine.setProperty('rate',240)
        say_(instruction)
        engine.setProperty('rate',200)

def sequence(str,red_count,blue_count,black_count):
    engine.setProperty('rate',220)
    say_('sequence')

    black = black_count
    red = red_count
    blue = blue_count
    first_level = wait_()
    first_level = remove_the(first_level)
    first_level = first_level.replace('see','c')
    first_level = first_level.replace('sea','c')
    first_level = first_level.replace('ct','c')
    first_level = first_level.replace('eight','c')
    first_level = first_level.replace('bee','b')
    first_level = first_level.replace('blow','blue')
    first_level = first_level.replace('baten','b')
    first_level = first_level.replace('rather','red')
    first_level = first_level.replace('be','b')
    first_level = first_level.replace('read','red')
    first_level = first_level.replace('block','black')
    if first_level == 'module':
        return
    level1 = first_level.split(' ')
    wire = []
    what_to_do = []
    print(level1 , f' red {red}, blue {blue}, black {black}')
    for word in level1:
        word = word.replace('see', 'c')
        word = word.replace('sea', 'c')
        word = word.replace('ct', 'c')
        word = word.replace('eight', 'c')
        word = word.replace('bee', 'b')
        word = word.replace('bat', 'b')
        word = word.replace('mix', 'next')
        word = word.replace('ban', 'b')
        word = word.replace('blow', 'blue')
        word = word.replace('baten', 'b')
        word = word.replace('rather', 'red')
        word = word.replace('be', 'b')
        word = word.replace('read', 'red')
        word = word.replace('block', 'black')
        if word == 'next':
            print('wire',wire)
            if 'red' in wire:
                red += 1
                print('red',red,f'wire: {wire}')
                if red == 1:
                    if 'c' in wire:
                        what_to_do.append('cut')
                    else:
                        what_to_do.append('skip')
                elif red == 2:
                    if 'b' in wire:
                        what_to_do.append('cut')
                    else:
                        what_to_do.append('skip')
                elif red == 3:
                    if 'a' in wire:
                        what_to_do.append('cut')
                    else:
                        what_to_do.append('skip')
                elif red == 4:
                    if 'c' in wire or 'a' in wire:
                        what_to_do.append('cut')
                    else:
                        what_to_do.append('skip')
                elif red == 5:
                    if 'b' in wire:
                        what_to_do.append('cut')
                    else:
                        what_to_do.append('skip')
                elif red == 6:
                    if 'c' in wire or 'a' in wire:
                        what_to_do.append('cut')
                    else:
                        what_to_do.append('skip')
                elif red == 7:
                    what_to_do.append('cut')
                elif red == 8:
                    if 'b' in wire or 'a' in wire:
                        what_to_do.append('cut')
                    else:
                        what_to_do.append('skip')
                elif red == 9:
                    if 'b' in wire:
                        what_to_do.append('cut')
                    else:
                        what_to_do.append('skip')
            elif 'blue' in wire:
                blue += 1
                print('blue',blue,f'wire: {wire}')
                if blue == 1:
                    if 'b' in wire:
                        what_to_do.append('cut')
                    else:
                        what_to_do.append('skip')
                elif blue == 2:
                    if 'a' in wire or 'c' in wire:
                        what_to_do.append('cut')
                    else:
                        what_to_do.append('skip')
                elif blue == 3:
                    if 'b' in wire:
                        what_to_do.append('cut')
                    else:
                        what_to_do.append('skip')
                elif blue == 4:
                    if 'a' in wire:
                        what_to_do.append('cut')
                    else:
                        what_to_do.append('skip')
                elif blue == 5:
                    if 'b' in wire:
                        what_to_do.append('cut')
                    else:
                        what_to_do.append('skip')
                elif blue == 6:
                    if 'c' in wire or 'b' in wire:
                        what_to_do.append('cut')
                    else:
                        what_to_do.append('skip')
                elif blue == 7:
                    if 'c' in wire:
                        what_to_do.append('cut')
                    else:
                        what_to_do.append('skip')
                elif blue == 8:
                    if 'c' in wire or 'a' in wire:
                        what_to_do.append('cut')
                    else:
                        what_to_do.append('skip')
                elif blue == 9:
                    if 'a' in wire:
                        what_to_do.append('cut')
                    else:
                        what_to_do.append('skip')
            elif 'black' in wire:

                black += 1
                print('adding black',black,f'wire: {wire}')
                if black == 1:
                    what_to_do.append('cut')
                elif black == 2:
                    if 'a' in wire or 'c' in wire:
                        what_to_do.append('cut')
                    else:
                        what_to_do.append('skip')
                elif black == 3:
                    if 'b' in wire:
                        what_to_do.append('cut')
                    else:
                        what_to_do.append('skip')
                elif black == 4:
                    if 'a' in wire or 'c' in wire:
                        what_to_do.append('cut')
                    else:
                        what_to_do.append('skip')
                elif black == 5:
                    if 'b' in wire:
                        what_to_do.append('cut')
                    else:
                        what_to_do.append('skip')
                elif black == 6:
                    if 'c' in wire or 'b' in wire:
                        what_to_do.append('cut')
                    else:
                        what_to_do.append('skip')
                elif black == 7:
                    if 'b' in wire or 'a' in wire:
                        what_to_do.append('cut')
                    else:
                        what_to_do.append('skip')
                elif black == 8:
                    if 'c' in wire:
                        what_to_do.append('cut')
                    else:
                        what_to_do.append('skip')
                elif black == 9:
                    if 'c' in wire:
                        what_to_do.append('cut')
                    else:
                        what_to_do.append('skip')
            wire = []
        elif word == 'done':

            return
        else:
            wire.append(word)
    huj = ''
    for words in what_to_do:
        huj += words + ' '
    print('huj test', huj)
    engine.setProperty('rate', 240)
    say_(huj)

    engine.setProperty('rate', 200)
    sequence('',red,blue,black)
def simon_says(color_array,loop,strike):
    colors = color_array
    engine.setProperty('rate', speed_up)
    has_vowel = False
    vowels = ['a', 'e', 'i', 'o', 'u']
    for sign in serial:
        if sign in vowels:
            has_vowel = True
            break
    print(has_vowel, 'serial has vowel or not ')
    strikes = strike
    if loop == 0:
        say_('colors, strikes')
        strikes = 0
        answ = wait_()
        answe = remove_the(answ)
        if answe in numbers:
            answer = numbers[answe]
        if answe == 'module':
            return
        try:
            strikes = int(answer)
        except ValueError:
            simon_says(colors,0)
    say_('color')
    flashing = wait_()
    flashing = remove_the(flashing)
    flashing = flashing.replace('read','red')
    if flashing == 'done' or flashing =='don' or flashing == 'dawn':return
    print(flashing)
    if has_vowel:
        if strikes == 0:
            if flashing == 'red':
                colors.append('blue')
            elif flashing == 'blue':
                colors.append('red')
            elif flashing == 'green':
                colors.append('yellow')
            elif flashing == 'yellow':
                colors.append('green')
        elif strikes == 1:
            if flashing == 'red':
                colors.append('yellow')
            elif flashing == 'blue':
                colors.append('green')
            elif flashing == 'green':
                colors.append('blue')
            elif flashing == 'yellow':
                colors.append('red')
        elif strikes == 2:
            if flashing == 'red':
                colors.append('green')
            elif flashing == 'blue':
                colors.append('red')
            elif flashing == 'green':
                colors.append('yellow')
            elif flashing == 'yellow':
                colors.append('blue')
    else:
        if strikes == 0:
            if flashing == 'red':
                colors.append('blue')
            elif flashing == 'blue':
                colors.append('yellow')
            elif flashing == 'green':
                colors.append('green')
            elif flashing == 'yellow':
                colors.append('red')
        elif strikes == 1:
            if flashing == 'red':
                colors.append('yellow')
            elif flashing == 'blue':
                colors.append('blue')
            elif flashing == 'green':
                colors.append('yellow')
            elif flashing == 'yellow':
                colors.append('green')
        elif strikes == 2:
            if flashing == 'red':
                colors.append('yellow')
            elif flashing == 'blue':
                colors.append('green')
            elif flashing == 'green':
                colors.append('blue')
            elif flashing == 'yellow':
                colors.append('red')
    huj = ''
    for words in colors:
        huj += words + ' '
    print('huj test', huj)
    engine.setProperty('rate', 240)
    say_(huj)

    engine.setProperty('rate', 200)

    simon_says(colors,1,strikes)

def memory():
    engine.setProperty('rate', speed_up)
    say_('memory')
    stage1 = '' # main number | seems to be useless xd
    number1 = '' #number on button
    position1 = '' #position of button (first second third fourth)
    stage2 = ''
    number2 = ''
    position2 = ''
    stage3 = ''
    number3 = ''
    position3 = ''
    stage4 = ''
    number4 = ''
    position4 = ''
    stage5 = ''
    number5 = ''
    position5 = ''
    say_('step 1')
    level1 = wait_()
    level1 = remove_the(level1)
    print(level1)
    if level1 == 'module':
        return
    if level1 in numbers:
        level1 = numbers[level1]
        if level1 == 1:
            say_('second position')
            number1 = wait_()
            number1 = remove_the(number1)
            if number1 in numbers:
                number1 = numbers[number1]
            position1 = '2'

        elif level1 == 2:
            say_('second position')
            number1 = wait_()
            number1 = remove_the(number1)
            if number1 in numbers:
                number1 = numbers[number1]
            position1 = '2'

        elif level1 == 3:
            say_('third position')
            number1 = wait_()
            number1 = remove_the(number1)
            if number1 in numbers:
                number1 = numbers[number1]
            position1 = '3'

        elif level1 == 4:
            say_('fourth position')
            number1 = wait_()
            number1 = remove_the(number1)
            if number1 in numbers:
                number1 = numbers[number1]
            position1 = '4'

    say_('step 2')
    level2 = wait_()
    level2 = remove_the(level2)
    if level2 in numbers:
        level2 = numbers[level2]

        if level2 == 1:
            say_('press 4')
            number2 = '4'
            position = wait_()
            position = remove_the(position)
            if position in numbers:
                position2 = numbers[position]

        elif level2 == 2:
            say_(f' press {position1} position')
            number2 = wait_()
            number2 = remove_the(number2)
            if number2 in numbers:
                number2 = numbers[number2]
            position2 = position1

        elif level2 == 3:
            say_('first position')
            number2 = wait_()
            number2 = remove_the(number2)
            if number2 in numbers:
                number2 = numbers[number2]
            position2 = '1'

        elif level2 == 4:
            say_(f' press {position1} position')
            number2 = wait_()
            number2 = remove_the(number2)
            if number2 in numbers:
                number2 = numbers[number2]
            position2 = position1

    say_('step 3')
    level3 = wait_()
    level3 = remove_the(level3)
    if level3 in numbers:
        level3 = numbers[level3]

        if level3 == 1:
            say_(f'press {number2}')
            number3 = number2
            position = wait_()
            position = remove_the(position)
            if position in numbers:
                position3 = numbers[position]

        elif level3 == 2:
            say_(f'press {number1}')
            number3 = number1
            position = wait_()
            position = remove_the(position)
            if position in numbers:
                position3 = numbers[position]

        elif level3 == 3:
            say_('third position')
            number3 = wait_()
            number3 = remove_the(number3)
            if number3 in numbers:
                number3 = numbers[number3]
            position3 = '3'

        elif level3 == 4:
            say_(f' press 4')
            number3 = '4'
            position = wait_()
            position = remove_the(position)
            if position in numbers:
                position3 = numbers[position]

    say_('step 4')
    level4 = wait_()
    level4 = remove_the(level4)
    if level4 in numbers:
        level4 = numbers[level4]

        if level4 == 1:
            say_(f'press {position1} position')
            number4 = wait_()
            number4 = remove_the(number4)
            if number4 in numbers:
                number4 = numbers[number4]
            position4 = position1

        elif level4 == 2:
            say_(f'first position')
            number4 = wait_()
            number4 = remove_the(number4)
            if number4 in numbers:
                number4 = numbers[number4]
            position4 = '1'

        elif level4 == 3:
            say_(f'press {position2} position')
            number4 = wait_()
            number4 = remove_the(number4)
            if number4 in numbers:
                number4 = numbers[number4]
            position4 = position2

        elif level4 == 4:
            say_(f'press {position2} position')
            number4 = wait_()
            number4 = remove_the(number4)
            if number4 in numbers:
                number4 = numbers[number4]
            position4 = position2

    say_('step 5')
    level5 = wait_()
    level5 = remove_the(level5)
    if level5 in numbers:
        level5 = numbers[level5]
        if level5 == 1:

            say_(f'press {number1}')
        elif level5 == 2:

            say_(f'press {number2}')
        elif level5 == 3:

            say_(f'press {number4}')
        elif level5 == 4:

            say_(f'press {number3}')

def morse():
    morse_LUT = {
        'shell' : 505,
        'halls' : 515,
        'slick' : 522,
        'trick' : 532,
        'boxes' : 535,
        'leaks' : 542,
        'strobe': 545,
        'bistro': 552,
        'flick' : 555,
        'bombs' : 565,
        'break' : 572,
        'brick' : 575,
        'steak' : 582,
        'sting' : 592,
        'vector': 595,
        'beats' : 600
    }
    morse_LUT2 = ['shell','halls','slick','trick','boxes','leaks','strobe','bistro','flick','bombs','break','brick','steak','sting','vector','beats']
    morse_decode_LUT = {
        '.-' : 'a',
        '-...' : 'b',
        '-.-.' : 'c',
        '-..' : 'd',
        '.' : 'e',
        '..-.': 'f',
        '--.': 'g',
        '....':'h',
        '..':'i',
        '.---':'j',
        '-.-':'k',
        '.-..':'l',
        '--':'m',
        '-.':'n',
        '---':'o',
        '.--.':'p',
        '--.-':'q',
        '.-.':'r',
        '...':'s',
        '-':'t',
        '..-':'u',
        '...-':'v',
        '.--':'w',
        '-..-':'x',
        '-.--':'y',
        '--..':'z'
    }
    #idea do it like password but all at once, so no optimization here really cuz bot is 2 slow
    morse_code = wait_()
    morse_code = remove_the(morse_code)

    morse_code = morse_code.replace('light','line')
    morse_code = morse_code.replace('lime','line')
    morse_code = morse_code.replace('lie','line')
    morse_code = morse_code.replace('like','line')
    morse_code = morse_code.replace('ninth','line')
    morse_code = morse_code.replace('that','dot')
    morse_code = morse_code.replace('net','next')
    morse_code = morse_code.replace('he','')
    morse_code = morse_code.replace('thought','dot')
    morse_code = morse_code.replace("don't",'dot')
    morse_code = morse_code.replace("do",'dot')
    morse_code = morse_code.replace("got",'dot')
    morse_code = morse_code.split(' ')
    if morse_code == 'module':
        return
    one_sign = []
    solution = ''

    numb_of_signs = 0
    for sign in morse_code:
        possible_sols = []
        if sign == 'next' or sign == 'mixed':
            temp_word = ''
            for signs in one_sign:
                print(f'current sign {sign}', f' one sign: {one_sign}',f'current signs {signs}')
                if signs == 'dot':
                    print('adding a dot')
                    temp_word += '.'
                elif signs == 'line':
                    print('adding a line')
                    temp_word += '-'
                else:
                    print('UH OH NOT GOOOD ')
            print(f'temp word before changing to a sign: {temp_word}')
            if temp_word in morse_decode_LUT:

                temp_word = morse_decode_LUT[temp_word]
                print(f'current temp word: {temp_word}')

            solution += temp_word
            numb_of_signs += 1
            for morse_codes in morse_LUT2:
                if solution == morse_codes[:numb_of_signs]:
                    possible_sols.append(morse_codes)
            if len(possible_sols) == 1:
                say_(possible_sols);return
            print(f' current solution {solution}')
            one_sign = []
        else:
            if sign == 'module':return
            one_sign.append(sign)
            print('appending one sign', one_sign)
    print(f'solution : {solution}')
    try:
        say_(morse_LUT[solution])
    except KeyError:
        morse()

def keypads():
    engine.setProperty('rate',speed_up)
    say_('keypads')
    keypad1 = ['o','triangle','gamma','lightning','rocket','hello','c']
    keypad2 = ['monster','o','c','spring','star','hello','questionmark']
    keypad3 = ['copyright','bob','spring','octopus','line','gamma','star']
    keypad4 = ['six','paragraph','table','rocket','questionmark','face']
    keypad5 = ['trident','face','table','c','paragraph','three','star']
    keypad6 = ['six','monster','puzzle','something','trident','devil','omega']
    signs = wait_()

    signs = remove_the(signs)
    if signs == 'module': return
    signs = signs.replace('sea','c')
    signs = signs.replace('bulb','bob')
    signs = signs.replace('or ','')
    signs = signs.replace('the ','')
    signs = signs.replace('see','c')
    signs = signs.replace('tree','three')
    signs = signs.replace('free','three')
    signs = signs.replace('tea','three')
    signs = signs.replace('start','star')
    signs = signs.replace('debbie','devil')
    signs = signs.replace('grandma','gamma')
    signs = signs.replace('gum','gamma')
    signs = signs.replace('oh','o')
    signs = signs.replace('all','o')
    signs = signs.replace('gunma','gamma')
    signs = signs.replace('government','gamma')
    signs = signs.replace('spraying','spring')
    signs = signs.replace('string','spring')
    signs = signs.replace('?','questionmark')
    signs = signs.split(' ')
    print(signs)
    kp1 = 0
    kp2 = 0
    kp3 = 0
    kp4 = 0
    kp5 = 0
    kp6 = 0
    k_array1 = []
    k_array2 = []
    k_array3 = []
    k_array4 = []
    k_array5 = []
    k_array6 = []
    for sign in signs:
        print(sign)
        if sign in keypad1:
            k_array1.append(sign)
            kp1+=1
            print('kp1 + 1', kp1)
        if sign in keypad2:
            k_array2.append(sign)
            kp2+=1
            print('kp2 + 1', kp2)
        if sign in keypad3:
            k_array3.append(sign)
            kp3+=1
            print('kp3 + 1', kp3)
        if sign in keypad4:
            k_array4.append(sign)
            kp4+=1
            print('kp4 + 1', kp4)
        if sign in keypad5:
            k_array5.append(sign)
            kp5+=1
            print('kp5 + 1', kp5)
        if sign in keypad6:
            k_array6.append(sign)
            kp6+=1
            print('kp6 + 1', kp6)
    print(kp1, kp2, kp3, kp4, kp5, kp6)
    print(k_array1, k_array2, k_array3,k_array4, k_array5, k_array6)
    if kp1 == 4:
        print(f'entire array{keypad1} and what you said {k_array1}')
        for keys in keypad1[:]:
            print(f'current key {keys}')
            if keys not in k_array1:
                keypad1.remove(keys)
                print(f'removing {keys}, current array {keypad1}')
        print(keypad1, 'keypad1')
        say_(f'{keypad1[0]} {keypad1[1]} {keypad1[2]} {keypad1[3]} ')
    elif kp2 == 4:
        print(f'entire array{keypad2} and what you said {k_array2}')
        for keys in keypad2[:]:
            print(f'current key {keys}')
            if keys not in k_array2:
                keypad2.remove(keys)
                print(f'removing {keys}, current array {keypad2}')
        print(keypad2, 'keypad2')
        say_(f'{keypad2[0]} {keypad2[1]} {keypad2[2]} {keypad2[3]}  ')
    elif kp3 == 4:
        print(f'entire array{keypad3} and what you said {k_array3}')
        for keys in keypad3[:]:
            print(f'current key {keys}')
            if keys not in k_array3:
                keypad3.remove(keys)
                print(f'removing {keys}, current array {keypad3}')
        print(keypad3, 'keypad3')
        say_(f'{keypad3[0]} {keypad3[1]} {keypad3[2]} {keypad3[3]} ')
    elif kp4 == 4:
        print(f'entire array{keypad4} and what you said {k_array4}')
        for keys in keypad4[:]:
            print(f'current key {keys}')
            if keys not in k_array4:
                keypad4.remove(keys)
                print(f'removing {keys}, current array {keypad4}')
        print(keypad4, 'keypad4')
        say_(f'{keypad4[0]} {keypad4[1]} {keypad4[2]} {keypad4[3]}  ')
    elif kp5 == 4:
        print(f'entire array {keypad5} and what you said {k_array5}')
        for keys in keypad5[:]:  # Iterate over a copy of the list
            print(f'current key {keys}')
            if keys not in k_array5:
                keypad5.remove(keys)
                print(f'removing {keys}, current array {keypad5}')
        print(keypad5, 'keypad5')
        say_(f'{keypad5[0]} {keypad5[1]} {keypad5[2]} {keypad5[3]}')

    elif kp6 == 4:
        print(f'entire array{keypad6} and what you said {k_array6}')
        for keys in keypad6[:]:
            print(f'current key {keys}')
            if keys not in k_array6:
                keypad6.remove(keys)
                print(f'removing {keys}, current array {keypad6}')
        print(keypad6, 'keypad6')
        say_(f'{keypad6[0]} {keypad6[1]} {keypad6[2]} {keypad6[3]}  ')

    return

def knobs():
    say_('knobs')

    answer = wait_()
    answer = remove_the(answer)

    if answer == 'module':
        return
    answer = answer.replace('too','two')
    answer = answer.replace('to','two')
    answer = answer.replace('free','three')
    answer = answer.replace('tree','three')
    answer = answer.replace('ate','eight')
    answer = answer.replace('aids','eight')
    answer = answer.replace('aid','eight')
    answer = answer.replace('for','four')
    answer = answer.replace('wow','one')
    answer = answer.replace('you','u')
    #answer = answer.split(' ')
    print(answer, 'knobs answer')
    if answer == 'one' or answer == 'zero':
        say_('left')
    elif answer == 'three':
        say_('down')
    elif answer == 'four':
        say_('up')
    elif answer == 'five':
        say_('down')
    elif answer == 'u':
        say_('right')
    return

def first():
    say_('first')
    #comments on left indicate of sth was changed or not to make the bot actually be able to understand differences
    #idea: in some tougher one, say the number so its like, 3 led = led not lead, just need to remember when to use what
    #because idk if really wanna use numbers before every one of them, that can happen because i need to read only 6 things total
    # but you  feel me right>

    #region
    top_left = ['two you are'] , #ur
    top_right = ['five first','four okay','one see'] # first, okay, c
    mid_left = ['three yes','seven nothing','three lead','seven they are'] # yes, nothing, led, they are
    mid_right = ['five blank','four read','three read','three you', 'four your','five you are','deer'] # blank,read,red,you,your,you're,their
    bot_left = ['empty','double read','double lead','six they are'] # literally blank, reed,leed,they're
    bot_right = ['display','says','no','lead','hold on','six you are','there','see','double see']
    answer = wait_()
    print(answer,'1')
    answer = remove_the(answer)
    print(answer,'2')
    answer = answer.replace('too','two')
    answer = answer.replace('sayss','says')
    answer = answer.replace('sas','says')
    answer = answer.replace('sas','says')
    answer = answer.replace('blog','blank')
    answer = answer.replace('to','two')
    answer = answer.replace('say','says')
    answer = answer.replace('for','four')
    answer = answer.replace('for','four')
    answer = answer.replace('red','read')
    answer = answer.replace('free','three')
    answer = answer.replace('tree','three')
    answer = answer.replace('wow','one')
    #endregion
    print(answer)
    print(type(answer))
    if answer == 'module':
        return
    elif answer in top_left:
        say_('top left')
    elif answer in top_right:
        say_('top right')
    elif answer in mid_left:
        say_('middle left')
    elif answer in mid_right:
        say_('middle right')
    elif answer in bot_left:
        say_('bottom left')
    elif answer in bot_right:
        say_('bottom right')
    else:
        first()
    key_word = wait_()
    print(key_word,'1')
    key_word=remove_the(key_word)
    print(key_word,'2')
    #key_word = key_word.replace('u','you')
    key_word = key_word.replace('for', 'four')
    key_word = key_word.replace('day','they')
    key_word = key_word.replace('three you','you')
    key_word = key_word.replace('view','you')
    key_word = key_word.replace('our','are')
    key_word = key_word.replace('day','are')
    key_word = key_word.replace('seeks','six')
    key_word = key_word.replace('four your','your')
    key_word = key_word.replace('four you','your')
    key_word = key_word.replace('four you','your')
    key_word = key_word.replace('what questionmark',"what?")
    key_word = key_word.replace('questionmark',"what?")
    key_word = key_word.replace('questionmark',"what?")
    key_word = key_word.replace('two you',"ur")
    key_word = key_word.replace('wow',"one")
    key_word = key_word.replace('to',"too")
    key_word = key_word.replace('sas',"says")
    key_word = key_word.replace('sayss',"says")
    key_word = key_word.replace('one you',"u")
    key_word = key_word.replace('five hello',"uh huh")
    key_word = key_word.replace('four hello',"uh uh")
    key_word = key_word.replace('three hello',"uhhh")
    key_word = key_word.replace('two you are',"ur")
    key_word = key_word.replace('five you',"you're")
    print(key_word,'3')
    engine.setProperty('rate',200)
    if key_word == 'blank':
        say_('wait, right, okay, middle, blank')
    elif key_word == 'done':
        say_('sure, 5 uh huh, next, what questionmark, your, 2 ur, you apostrophy are, hold, like, 3 you, 1 u, 6 you are, 4 uh uh, done')
    elif key_word == 'first':
        say_('left, 4 okay, yes, middle, no, right, nothing, 4 uhhh, waiot, ready, blank, what, press, first')
    elif key_word == 'hold':
        say_('6 you are, 1 u, done, 4 uh uh, 3 you, 2 ur, sure, what questionmark, you apostrophy are, next, hold')
    elif key_word == 'left':
        say('right,left')
    elif key_word == 'like':
        say_('you apostrophy are, next, 1 u, 2 ur, hold, done, 4 uh uh, what questionmark, 5 uh huh, 3 you, like')
    elif key_word == 'middle':
        say_('blank, ready, 4 okay, what, nothing, press, no , wait, left, middle')
    elif key_word == 'next':
        say_('what questionmark, 5 uh huh, 4 uh uh, 4 your, hold, sure, next')
    elif key_word == 'no':
        say_('blank, 4 uhhh, wait, first, what, ready, right, yes, nothing, left, press, okay,no')
    elif key_word == "nothing":
        say_('4 uhhh, right, 4 okay, middle, yes, blank, no, press, left, what, wait, first, nothing')
    elif key_word == 'okay':
        say_('middle, no, first, yes, 4 uhhh, nothing, wait, 4 okay')
    elif key_word == 'press':
        say_('right, middle, yes, ready, press')
    elif key_word == 'ready':
        say_('yes, 4 okay, what, middle, left, press, right, blank, ready')
    elif key_word == 'right':
        say_('yes, nothing, ready, press, no, wait, what, right')
    elif key_word == 'sure':
        say_('6 you are, done, like, you apostrophy are, 3 you, hold, 5 uh huh, 2 ur, sure')
    elif key_word == 'u':
        say_('5 uh huh, sure, next, what questionmark, you apostrophy are, 2 ur, 4 uh uh, done, 1 u')
    elif key_word == 'uh huh':
        say_('5 uh huh')
    elif key_word == 'uh uh':
        say_('2 ur, 1 u, 6 you are, you apostrophy are, next, 4 uh uh')
    elif key_word == 'uhhh':
        say_('ready, nothing, left, what, 4 okay, yes, right, no, press, blank, 4 uhhh')
    elif key_word == 'ur':
        say_('done, 1 u, 2 ur')
    elif key_word == 'wait':
        say_('4 uhhh, no, blank, 4 okay, yes, left, first, press, what, wait')
    elif key_word == 'what':
        say_('4 uhhh, what')
    elif key_word == 'what?':
        say_('3 you, hold, you apostrophy are, 4 your, 1 u, done, 4 uh uh, like, 6 you are, 5 uh huh, 2 ur, next, what questionmark')
    elif key_word == 'yes':
        say_('4 okay, right, 4 uhhh, middle, first, what, press, ready, nothing, yes')
    elif key_word == 'you are':
        say_('4 your, next, like, 5 uh huh, what questionmark, done, 4 uh uh, hold, 3 you, 1 u , you apostrophy are, sure, 2 ur, 6 you are')
    elif key_word == 'you':
        say_('sure, 6 you are, 4 your, you apostrophy are, next, 5 uh huh, 2 ur, hold, what questionmark, 3 you')
    elif key_word == 'your':
        say_('4 uh uh, 6 you are, 5 uh huh, 4 your')
    elif key_word == "you're":
        say_('3 you, you apostrophy are')
    else: first()
    print('returning ')

    engine.setProperty('rate',200)
    return
def maze_reverse(maze_map,current_number,goal_position,array_of_path_pos):
    while current_number > 0:
        current_number -= 1
        print(f' inside while loop checking for {current_number}')
        if goal_position[0] + 2 < 13:
            if maze_map[goal_position[1]][goal_position[0] + 2] == str(current_number): # right
                print(f'current number found at {goal_position[0] + 2}, {goal_position[1]}')
                goal_position = (goal_position[0] + 2, goal_position[1])
                array_of_path_pos.append(goal_position)
        if goal_position[0] - 2 > 0:
            if maze_map[goal_position[1]][goal_position[0] - 2] == str(current_number): # left
                print(f'current number found at {goal_position[0] - 2}, {goal_position[1]}')
                goal_position = (goal_position[0] - 2, goal_position[1])
                array_of_path_pos.append(goal_position)
        if goal_position[1] - 2 > 0:
            if maze_map[goal_position[1] - 2][goal_position[0]] == str(current_number): # up
                print(f'current number found at {goal_position[0]}, {goal_position[1] - 2}')
                goal_position = (goal_position[0], goal_position[1] - 2)
                array_of_path_pos.append(goal_position)
        if goal_position[1] + 2 < 13:
            if maze_map[goal_position[1] + 2][goal_position[0]] == str(current_number): # down
                print(f'current number found at {goal_position[0]}, {goal_position[1] + 2}')
                goal_position = (goal_position[0], goal_position[1] + 2)
                array_of_path_pos.append(goal_position)

    else:
        array_of_path_pos.reverse()
        print(array_of_path_pos,'123')
        return array_of_path_pos

def maze_solver(maze_map,starting_pos,goal_position,loop_array,current_number):
    #path = []
    loop_finished = False
    finish_found = False
    #loop array is an arrat that has number positions
    #current number is  number of loops in floodfill search
    print(current_number,loop_array,goal_position,'cur number and loop array and goal pos')
    #maze_map[start_pos[1]][start_pos[0]] = current_num
    array_of_pos = []
    if goal_position not in loop_array:
        # temp array to avoid overwriting and fuckery idkkkk
        current_number += 1
        for numbers in loop_array:
            print('numbers variable', numbers)
            if maze_map[numbers[1]][numbers[0] + 1] != '■':  # right

                if maze_map[numbers[1]][numbers[0] + 2] == 'P':
                    print('right move is free')
                    maze_map[numbers[1]][numbers[0] + 2] = str(current_number)
                    pos = (numbers[0]+2, numbers[1])
                    print('appending position', pos )
                    array_of_pos.append(pos) # return as loopm array
                if maze_map[numbers[1]][numbers[0] + 2] == 'F':
                    print('finish found')
                    print(f'calling function with current number {current_number} and array = {[goal_position]}')
                    path = maze_reverse(maze_map,current_number,goal_position,[goal_position])
                    finish_found = True
            if maze_map[numbers[1]][numbers[0] - 1] != '■':  # left
                if maze_map[numbers[1]][numbers[0] - 2] == 'P':
                    print('left move is free')
                    maze_map[numbers[1]][numbers[0] - 2] = str(current_number)
                    pos = (numbers[0] - 2, numbers[1])
                    print('appending position', pos)
                    array_of_pos.append(pos)  # return as loopm arra\
                if maze_map[numbers[1]][numbers[0] - 2] == 'F':
                    print('finish found')
                    print(f'calling function with current number {current_number} and array = {[goal_position]}')
                    path = maze_reverse(maze_map,current_number,goal_position,[goal_position])
                    finish_found = True
            if maze_map[numbers[1] - 1][numbers[0]] != '■':  # up
                if maze_map[numbers[1] - 2][numbers[0]] == 'P':
                    print('up move is free')
                    maze_map[numbers[1] - 2][numbers[0]] = str(current_number)
                    pos = (numbers[0], numbers[1] - 2)
                    print('appending position', pos)
                    array_of_pos.append(pos)  # return as loopm array
                if maze_map[numbers[1] - 2][numbers[0]] == 'F':
                    print('finish found')
                    print(f'calling function with current number {current_number} and array = {[goal_position]}')
                    path = maze_reverse(maze_map,current_number,goal_position,[goal_position])
                    finish_found = True
            if maze_map[numbers[1] + 1][numbers[0]] != '■':  # down
                if maze_map[numbers[1] + 2][numbers[0]] == 'P':
                    print('down move is free')
                    maze_map[numbers[1] + 2][numbers[0]] = str(current_number)
                    pos = (numbers[0], numbers[1] + 2)
                    print('appending position', pos)
                    array_of_pos.append(pos)  # return as loopm array
                if maze_map[numbers[1] + 2][numbers[0]] == 'F':
                    print('finish found')
                    print(f'calling function with current number {current_number} and array = {[goal_position]}')
                    path = maze_reverse(maze_map,current_number,goal_position,[goal_position])
                    finish_found = True
        for positions in array_of_pos:
            maze_map[positions[1]][positions[0]] = str(current_number)
        for row in maze_map:
            print(' '.join(row))
        print('-----------------------------------------')
    else:
        print('done')
        loop_finished = True
    print(current_number, array_of_pos, 'cur number and loop array before calling fucntion')
    moves_to_do = []

    #try:
    if finish_found:
        print(' finish found ')
        if len(path)>0:
            print('path', path)
            for i in range(len(path)):
                try:
                    if path[i][0]+2 == path[i+1][0]:
                        moves_to_do.append('right')
                    if path[i][0]-2 == path[i+1][0]:
                        moves_to_do.append('left')
                    if path[i][1]-2 == path[i+1][1]:
                        moves_to_do.append('up')
                    if path[i][1]+2 == path[i+1][1]:
                        moves_to_do.append('down')
                except:
                    break
        print(moves_to_do,' moves to do')
        string_moves = ''
        for move in moves_to_do:
            engine.setProperty('rate', 225)
            say_(move)
            string_moves += move


        return
    
    if current_number <37 and loop_finished == False:
        maze_solver(maze_map,starting_pos,goal_position,array_of_pos,current_number)


def maze():
    # cry for help will not save my tarnished soul
    # idea is like, if you will be maze 6 and check both dead ends, just return to starting position and choose different direction
    # notes 2, here i think the best idea is, to black out all the places that are not goal and are dead ends, so when you take a bad
    # turn at maze 9 , and you check both dead ends, with no checkpoint behind that, returning to start is fine AS LONG AS you will just block
    #everything you have explored FROM THE CHECKPOINT, so you will not block what is an actuall path
    #circle positions (0 index, (x,y))
    say_('maze, position')
    position = wait_()
    position = remove_the(position)
    position = position.replace('you know','zero')
    position = position.replace("i've", 'five')
    position = position.replace('you know', 'zero')
    position = position.replace('for', 'four')
    position = position.replace('or', 'four')
    position = position.replace('boo', 'two')
    position = position.replace("i've", 'five')
    position = position.replace("fouren", 'four')
    position = position.replace('to', 'two')
    position = position.replace('b', 'three')
    position = position.replace('who', 'two')
    position = position.replace('too', 'two')
    position = position.replace('be', 'three')
    position = position.replace('free', 'three')
    position = position.replace('twoo', 'two')
    if position == 'module': return
    circle_pos = ()
    position = position.split(' ')
    print('circle positions',position)
    for word in position:
        if word in numbers:
            circle_pos += (numbers[word],)
    #MAPS
    #region
    maze_map1 = [
        ['■', '■', '■', '■', '■', '■', '■', '■', '■', '■', '■', '■', '■'],
        ['■', 'P', ' ', 'P', ' ', 'P', '■', 'P', ' ', 'P', ' ', 'P', '■'],
        ['■', ' ', '■', '■', '■', ' ', '■', ' ', '■', '■', '■', '■', '■'],
        ['■', 'P', '■', 'P', ' ', 'P', '■', 'P', ' ', 'P', ' ', 'P', '■'],
        ['■', ' ', '■', ' ', '■', '■', '■', '■', '■', '■', '■', ' ', '■'],
        ['■', 'P', '■', 'P', ' ', 'P', '■', 'P', ' ', 'P', ' ', 'P', '■'],
        ['■', ' ', '■', '■', '■', ' ', '■', ' ', '■', '■', '■', ' ', '■'],
        ['■', 'P', '■', 'P', ' ', 'P', ' ', 'P', '■', 'P', ' ', 'P', '■'],
        ['■', ' ', '■', '■', '■', '■', '■', '■', '■', '■', '■', ' ', '■'],
        ['■', 'P', ' ', 'P', ' ', 'P', '■', 'P', ' ', 'P', '■', 'P', '■'],
        ['■', ' ', '■', '■', '■', ' ', '■', ' ', '■', '■', '■', ' ', '■'],
        ['■', 'P', ' ', 'P', '■', 'P', ' ', 'P', '■', 'P', ' ', 'P', '■'],
        ['■', '■', '■', '■', '■', '■', '■', '■', '■', '■', '■', '■', '■']
    ]
    maze_map2 = [
        ['■', '■', '■', '■', '■', '■', '■', '■', '■', '■', '■', '■', '■'],
        ['■', 'P', ' ', 'P', ' ', 'P', '■', 'P', ' ', 'P', ' ', 'P', '■'],
        ['■', '■', '■', ' ', '■', '■', '■', ' ', '■', ' ', '■', '■', '■'],
        ['■', 'P', ' ', 'P', '■', 'P', ' ', 'P', '■', 'P', ' ', 'P', '■'],
        ['■', ' ', '■', '■', '■', ' ', '■', '■', '■', '■', '■', ' ', '■'],
        ['■', 'P', '■', 'P', ' ', 'P', '■', 'P', ' ', 'P', ' ', 'P', '■'],
        ['■', ' ', '■', ' ', '■', '■', '■', ' ', '■', '■', '■', ' ', '■'],
        ['■', 'P', ' ', 'P', '■', 'P', ' ', 'P', '■', 'P', '■', 'P', '■'],
        ['■', ' ', '■', '■', '■', ' ', '■', '■', '■', ' ', '■', ' ', '■'],
        ['■', 'P', '■', 'P', '■', 'P', '■', 'P', ' ', 'P', '■', 'P', '■'],
        ['■', ' ', '■', ' ', '■', ' ', '■', ' ', '■', '■', '■', '■', '■'],
        ['■', 'P', '■', 'P', ' ', 'P', '■', 'P', ' ', 'P', ' ', 'P', '■'],
        ['■', '■', '■', '■', '■', '■', '■', '■', '■', '■', '■', '■', '■']
    ]
    maze_map3 = [
        ['■', '■', '■', '■', '■', '■', '■', '■', '■', '■', '■', '■', '■'],
        ['■', 'P', ' ', 'P', ' ', 'P', '■', 'P', '■', 'P', ' ', 'P', '■'],
        ['■', ' ', '■', '■', '■', ' ', '■', ' ', '■', ' ', '■', ' ', '■'],
        ['■', 'P', '■', 'P', '■', 'P', '■', 'P', ' ', 'P', '■', 'P', '■'],
        ['■', '■', '■', ' ', '■', ' ', '■', '■', '■', '■', '■', ' ', '■'],
        ['■', 'P', ' ', 'P', '■', 'P', '■', 'P', ' ', 'P', '■', 'P', '■'],
        ['■', ' ', '■', ' ', '■', ' ', '■', ' ', '■', ' ', '■', ' ', '■'],
        ['■', 'P', '■', 'P', '■', 'P', '■', 'P', '■', 'P', '■', 'P', '■'],
        ['■', ' ', '■', ' ', '■', ' ', '■', ' ', '■', ' ', '■', ' ', '■'],
        ['■', 'P', '■', 'P', ' ', 'P', '■', 'P', '■', 'P', '■', 'P', '■'],
        ['■', ' ', '■', '■', '■', '■', '■', ' ', '■', ' ', '■', ' ', '■'],
        ['■', 'P', ' ', 'P', ' ', 'P', ' ', 'P', '■', 'P', ' ', 'P', '■'],
        ['■', '■', '■', '■', '■', '■', '■', '■', '■', '■', '■', '■', '■']
    ]
    maze_map4 = [
        ['■', '■', '■', '■', '■', '■', '■', '■', '■', '■', '■', '■', '■'],
        ['■', 'P', ' ', 'P', '■', 'P', ' ', 'P', ' ', 'P', ' ', 'P', '■'],
        ['■', ' ', '■', ' ', '■', '■', '■', '■', '■', '■', '■', ' ', '■'],
        ['■', 'P', '■', 'P', '■', 'P', ' ', 'P', ' ', 'P', ' ', 'P', '■'],
        ['■', ' ', '■', ' ', '■', ' ', '■', '■', '■', '■', '■', ' ', '■'],
        ['■', 'P', '■', 'P', ' ', 'P', '■', 'P', ' ', 'P', '■', 'P', '■'],
        ['■', ' ', '■', '■', '■', '■', '■', ' ', '■', '■', '■', ' ', '■'],
        ['■', 'P', '■', 'P', ' ', 'P', ' ', 'P', ' ', 'P', ' ', 'P', '■'],
        ['■', ' ', '■', '■', '■', '■', '■', '■', '■', '■', '■', ' ', '■'],
        ['■', 'P', ' ', 'P', ' ', 'P', ' ', 'P', ' ', 'P', '■', 'P', '■'],
        ['■', ' ', '■', '■', '■', '■', '■', '■', '■', ' ', '■', ' ', '■'],
        ['■', 'P', ' ', 'P', ' ', 'P', '■', 'P', ' ', 'P', '■', 'P', '■'],
        ['■', '■', '■', '■', '■', '■', '■', '■', '■', '■', '■', '■', '■']
    ]
    maze_map5 = [
        ['■', '■', '■', '■', '■', '■', '■', '■', '■', '■', '■', '■', '■'],
        ['■', 'P', ' ', 'P', ' ', 'P', ' ', 'P', ' ', 'P', ' ', 'P', '■'],
        ['■', '■', '■', '■', '■', '■', '■', '■', '■', ' ', '■', ' ', '■'],
        ['■', 'P', ' ', 'P', ' ', 'P', ' ', 'P', ' ', 'P', '■', 'P', '■'],
        ['■', ' ', '■', '■', '■', '■', '■', ' ', '■', '■', '■', '■', '■'],
        ['■', 'P', ' ', 'P', '■', 'P', ' ', 'P', '■', 'P', ' ', 'P', '■'],
        ['■', ' ', '■', ' ', '■', '■', '■', '■', '■', ' ', '■', ' ', '■'],
        ['■', 'P', '■', 'P', ' ', 'P', ' ', 'P', '■', 'P', '■', 'P', '■'],
        ['■', ' ', '■', '■', '■', '■', '■', ' ', '■', '■', '■', ' ', '■'],
        ['■', 'P', '■', 'P', ' ', 'P', ' ', 'P', ' ', 'P', '■', 'P', '■'],
        ['■', ' ', '■', ' ', '■', '■', '■', '■', '■', '■', '■', ' ', '■'],
        ['■', 'P', '■', 'P', ' ', 'P', ' ', 'P', ' ', 'P', ' ', 'P', '■'],
        ['■', '■', '■', '■', '■', '■', '■', '■', '■', '■', '■', '■', '■']
    ]
    maze_map6 = [
        ['■', '■', '■', '■', '■', '■', '■', '■', '■', '■', '■', '■', '■'],
        ['■', 'P', '■', 'P', ' ', 'P', '■', 'P', ' ', 'P', ' ', 'P', '■'],
        ['■', ' ', '■', ' ', '■', ' ', '■', '■', '■', ' ', '■', ' ', '■'],
        ['■', 'P', '■', 'P', '■', 'P', '■', 'P', ' ', 'P', '■', 'P', '■'],
        ['■', ' ', '■', ' ', '■', ' ', '■', ' ', '■', '■', '■', ' ', '■'],
        ['■', 'P', ' ', 'P', '■', 'P', '■', 'P', '■', 'P', ' ', 'P', '■'],
        ['■', ' ', '■', '■', '■', '■', '■', ' ', '■', ' ', '■', '■', '■'],
        ['■', 'P', ' ', 'P', '■', 'P', ' ', 'P', '■', 'P', '■', 'P', '■'],
        ['■', '■', '■', ' ', '■', ' ', '■', ' ', '■', ' ', '■', ' ', '■'],
        ['■', 'P', ' ', 'P', '■', 'P', '■', 'P', '■', 'P', ' ', 'P', '■'],
        ['■', ' ', '■', '■', '■', '■', '■', ' ', '■', '■', '■', ' ', '■'],
        ['■', 'P', ' ', 'P', ' ', 'P', ' ', 'P', '■', 'P', ' ', 'P', '■'],
        ['■', '■', '■', '■', '■', '■', '■', '■', '■', '■', '■', '■', '■']
    ]  # podwojne rozwidlenie ale read idea
    maze_map7 = [
        ['■', '■', '■', '■', '■', '■', '■', '■', '■', '■', '■', '■', '■'],
        ['■', 'P', ' ', 'P', ' ', 'P', ' ', 'P', '■', 'P', ' ', 'P', '■'],
        ['■', ' ', '■', '■', '■', '■', '■', ' ', '■', ' ', '■', ' ', '■'],
        ['■', 'P', '■', 'P', ' ', 'P', '■', 'P', ' ', 'P', '■', 'P', '■'],
        ['■', ' ', '■', ' ', '■', '■', '■', '■', '■', '■', '■', ' ', '■'],
        ['■', 'P', ' ', 'P', '■', 'P', ' ', 'P', '■', 'P', ' ', 'P', '■'],
        ['■', '■', '■', '■', '■', ' ', '■', '■', '■', ' ', '■', '■', '■'],
        ['■', 'P', ' ', 'P', '■', 'P', ' ', 'P', ' ', 'P', '■', 'P', '■'],
        ['■', ' ', '■', ' ', '■', ' ', '■', '■', '■', '■', '■', ' ', '■'],
        ['■', 'P', '■', 'P', '■', 'P', ' ', 'P', ' ', 'P', '■', 'P', '■'],
        ['■', ' ', '■', '■', '■', '■', '■', '■', '■', ' ', '■', ' ', '■'],
        ['■', 'P', ' ', 'P', ' ', 'P', ' ', 'P', ' ', 'P', ' ', 'P', '■'],
        ['■', '■', '■', '■', '■', '■', '■', '■', '■', '■', '■', '■', '■']
    ]
    maze_map8 = [
        ['■', '■', '■', '■', '■', '■', '■', '■', '■', '■', '■', '■', '■'],
        ['■', 'P', '■', 'P', ' ', 'P', ' ', 'P', '■', 'P', ' ', 'P', '■'],
        ['■', ' ', '■', ' ', '■', '■', '■', ' ', '■', ' ', '■', ' ', '■'],
        ['■', 'P', ' ', 'P', ' ', 'P', '■', 'P', ' ', 'P', '■', 'P', '■'],
        ['■', ' ', '■', '■', '■', '■', '■', '■', '■', '■', '■', ' ', '■'],
        ['■', 'P', '■', 'P', ' ', 'P', ' ', 'P', ' ', 'P', '■', 'P', '■'],
        ['■', ' ', '■', ' ', '■', '■', '■', '■', '■', ' ', '■', ' ', '■'],
        ['■', 'P', '■', 'P', ' ', 'P', '■', 'P', ' ', 'P', ' ', 'P', '■'],
        ['■', ' ', '■', '■', '■', ' ', '■', '■', '■', '■', '■', '■', '■'],
        ['■', 'P', '■', 'P', '■', 'P', ' ', 'P', ' ', 'P', ' ', 'P', '■'],
        ['■', ' ', '■', ' ', '■', '■', '■', '■', '■', '■', '■', '■', '■'],
        ['■', 'P', ' ', 'P', ' ', 'P', ' ', 'P', ' ', 'P', ' ', 'P', '■'],
        ['■', '■', '■', '■', '■', '■', '■', '■', '■', '■', '■', '■', '■']
    ]
    maze_map9 = [
        ['■', '■', '■', '■', '■', '■', '■', '■', '■', '■', '■', '■', '■'],
        ['■', 'P', '■', 'P', ' ', 'P', ' ', 'P', ' ', 'P', ' ', 'P', '■'],
        ['■', ' ', '■', ' ', '■', '■', '■', '■', '■', ' ', '■', ' ', '■'],
        ['■', 'P', '■', 'P', '■', 'P', ' ', 'P', '■', 'P', '■', 'P', '■'],
        ['■', ' ', '■', ' ', '■', ' ', '■', '■', '■', ' ', '■', ' ', '■'],
        ['■', 'P', ' ', 'P', ' ', 'P', '■', 'P', ' ', 'P', '■', 'P', '■'],
        ['■', ' ', '■', '■', '■', '■', '■', ' ', '■', '■', '■', ' ', '■'],
        ['■', 'P', '■', 'P', '■', 'P', ' ', 'P', '■', 'P', ' ', 'P', '■'],
        ['■', ' ', '■', ' ', '■', ' ', '■', '■', '■', '■', '■', ' ', '■'],
        ['■', 'P', '■', 'P', '■', 'P', '■', 'P', ' ', 'P', '■', 'P', '■'],
        ['■', ' ', '■', ' ', '■', ' ', '■', ' ', '■', ' ', '■', '■', '■'],
        ['■', 'P', ' ', 'P', '■', 'P', ' ', 'P', '■', 'P', ' ', 'P', '■'],
        ['■', '■', '■', '■', '■', '■', '■', '■', '■', '■', '■', '■', '■']
    ]  # check notes 2
    #endregion
    print(circle_pos,'position fo circles')
    maze1 = [(0,1),(5,2),(0,1,),(5,2,)]
    maze2 = [(1,3),(4,1),(1,3,),(4,1,)]
    maze3 = [(3,3),(5,3),(3,3,),(5,3,)]
    maze4 = [(0,0),(0,3),(0,0,),(0,3,)]
    maze5 = [(4,2),(3,5),(4,2,),(3,5,)]
    maze6 = [(4,0),(2,4),(4,0,),(2,4,)]
    maze7 = [(1,0),(1,5),(1,0,),(1,5,)]
    maze8 = [(3,0),(2,3),(3,0,),(2,3,)]
    maze9 = [(2,1),(0,4),(2,1,),(0,4,)]
    # my pos * 2 + 1 = new pos
    say_('start position')
    starting_pos = wait_()
    starting_pos = remove_the(starting_pos)
    starting_pos = starting_pos.replace('you know','zero')
    starting_pos = starting_pos.replace('for', 'four')
    starting_pos = starting_pos.replace('or', 'four')
    starting_pos = starting_pos.replace('boo', 'two')
    starting_pos = starting_pos.replace("i've", 'five')
    starting_pos = starting_pos.replace("fouren", 'four')
    starting_pos = starting_pos.replace('to', 'two')
    starting_pos = starting_pos.replace('b', 'three')
    starting_pos = starting_pos.replace('who', 'two')
    starting_pos = starting_pos.replace('too', 'two')
    starting_pos = starting_pos.replace('be', 'three')
    starting_pos = starting_pos.replace('free', 'three')
    starting_pos = starting_pos.replace('twoo', 'two')
    starting_pos = starting_pos.split(' ')
    print(starting_pos,'starting pos variable')
    start_pos = ()
    for word in starting_pos:
        if word in numbers:
            start_pos += (numbers[word]*2+1,)
    print('start pos ', start_pos)
    if circle_pos in maze1:
        print('maze 1')
        maze_map1[start_pos[1]][start_pos[0]] = '0'
        map_number = copy.deepcopy(maze_map1)

    elif circle_pos in maze2:
        print('maze 2')
        maze_map2[start_pos[1]][start_pos[0]] = '0'
        map_number = copy.deepcopy(maze_map2)

    elif circle_pos in maze3:
        print('maze 3')
        maze_map3[start_pos[1]][start_pos[0]] = '0'
        map_number = copy.deepcopy(maze_map3)

    elif circle_pos in maze4:
        print('maze 4')
        maze_map4[start_pos[1]][start_pos[0]] = '0'
        map_number = copy.deepcopy(maze_map4)

    elif circle_pos in maze5:
        print('maze 5')
        maze_map5[start_pos[1]][start_pos[0]] = '0'
        map_number = copy.deepcopy(maze_map5)

    elif circle_pos in maze6:
        print('maze 6')
        maze_map6[start_pos[1]][start_pos[0]] = '0'
        map_number = copy.deepcopy(maze_map6)

    elif circle_pos in maze7:
        print('maze 7')
        maze_map7[start_pos[1]][start_pos[0]] = '0'
        map_number = copy.deepcopy(maze_map7)

    elif circle_pos in maze8:
        print('maze 8')
        maze_map8[start_pos[1]][start_pos[0]] = '0'
        map_number = copy.deepcopy(maze_map8)

    elif circle_pos in maze9:
        print('maze 9')
        maze_map9[start_pos[1]][start_pos[0]] = '0'
        map_number = copy.deepcopy(maze_map9)




    say_('end position')
    goal = wait_()
    goal = remove_the(goal)
    goal = goal.replace('you know', 'zero')
    goal = goal.replace('we', 'three')
    goal = goal.replace("i've", 'five')
    goal = goal.replace("fouren", 'four')
    goal = goal.replace('for', 'four')
    goal = goal.replace('or', 'four')
    goal = goal.replace('b', 'four')
    goal = goal.replace('boo', 'two')
    goal = goal.replace('to', 'two')
    goal = goal.replace('who', 'two')
    goal = goal.replace('too', 'two')
    goal = goal.replace('euro', 'zero')
    goal = goal.replace('pre', 'three')
    goal = goal.replace('be', 'three')
    goal = goal.replace('free', 'three')
    goal = goal.replace('twoo', 'two')
    goal = goal.split(' ')

    print(goal, 'goal variable (answer)')
    goal_pos = ()

    for word in goal:
        if word in numbers:
            goal_pos += (numbers[word]*2+1,)

    maze_map1[goal_pos[1]][goal_pos[0]] = 'F'
    maze_map2[goal_pos[1]][goal_pos[0]] = 'F'
    maze_map3[goal_pos[1]][goal_pos[0]] = 'F'
    maze_map4[goal_pos[1]][goal_pos[0]] = 'F'
    maze_map5[goal_pos[1]][goal_pos[0]] = 'F'
    maze_map6[goal_pos[1]][goal_pos[0]] = 'F'
    maze_map7[goal_pos[1]][goal_pos[0]] = 'F'
    maze_map8[goal_pos[1]][goal_pos[0]] = 'F'
    maze_map9[goal_pos[1]][goal_pos[0]] = 'F'
    map_number[goal_pos[1]][goal_pos[0]] = 'F'
    
    maze_solver(map_number,start_pos,goal_pos,[start_pos],0)
    # start_pos = (pos[0],pos[1])
    ## god help me
    # 4 check and then 4 more, make a variable that keeps track of newest number and make a check that if position of those newest numbers (i mean one of them, they will be in array that will...)
    # ...be removing positions of previous numbers uz they useless,
    
    # not sure what code below does, apparently its not usefull since it was commented out so i think you can remove it, im leaving it cuz mby there is something
    # valuable in there but im p sure you can just remove it no problem 
    runner_pos = copy.deepcopy(start_pos)
        while maze_map1[runner_pos[1]+1][runner_pos[0]] != 'F' or maze_map1[runner_pos[1]-1][runner_pos[0]] != 'F' or maze_map1[runner_pos[1]][runner_pos[0]+1] != 'F' or maze_map1[runner_pos[1]][runner_pos[0]-1] != 'F':
            available_paths = 0
            move_to_right = 0 # like a bool 1 = yes 0 = no
            move_to_left = 0 # like a bool 1 = yes 0 = no
            move_to_up = 0 # like a bool 1 = yes 0 = no
            move_to_down = 0 # like a bool 1 = yes 0 = no
            if maze_map1[runner_pos[1]+1][runner_pos[0]] != '■':
                if maze_map1[runner_pos[1]+2][runner_pos[0]] != 'P':

                move_to_down = 1
            elif maze_map1[runner_pos[1]-1][runner_pos[0]] != '■':

                move_to_up = 1
            elif maze_map1[runner_pos[1]][runner_pos[0]+1] != '■':

                move_to_right = 1
            elif maze_map1[runner_pos[1]][runner_pos[0]-1] != '■':

                move_to_left = 1


while True:
    print("waiting")

    if mode == 'wait':
        recognized_text = listening()
        recognized_text = remove_the(recognized_text)
        if recognized_text == 'go' or recognized_text == 'goal' or recognized_text == 'girl':
            #say_('start')
            mode = 'go'
        else:
            print(recognized_text)
    elif mode == 'go':


        serial = ask_for_advanced("serial")
        info_dict["serial"] = serial
        #say_(f'serial: {serial}')
        lights, port, batteries = edgework()
        #lights,port = ask_for_advanced("edgework")

        #batteries = ask_for("batteries")
        #info_dict["batteries"] = batteries
        #say_(f'batteries: {batteries}')
        mode = 'play'
    elif mode == 'test':
        port = 'parallel'
        serial = 'jjjjk5'
        lights = ('asd','yes')
        batteries = 2
        mode = 'play'
    elif mode == 'play':

        #^^^ REMOVE THAT WHEN NOT TESTING OR COMMENT THAT OUR BECAUSE IT WILL OVERWRITE THINGS!!!!!!!!!!!!!!!!!!!!!!!!!!!
        print('entered play mode')
        say_('module')
        rec_text = listening()
        recognized_text = rec_text.replace('the ', '')

        print(recognized_text)
        #DONE
        if recognized_text == 'button' or recognized_text == 'bottom':
            say_('button')
            button_held = False
            say_('label')
            state_on_button = listening()
            state_on_button = remove_the(state_on_button)
            say_('color')
            color_of_button = listening()
            color_of_button = remove_the(color_of_button)
            if color_of_button == 'read':
                color_of_button = 'red'
            say_(f'button: {state_on_button}, color: {color_of_button}, correct?')
            answer_ = wait_()
            answer = remove_the(answer_)
            if answer in positive_answers:
                if color_of_button == 'blue' and state_on_button[0] == 'abort':
                    button_held = True

                elif int(batteries) > 1 and state_on_button[0] == 'detonate':
                    say_('press and release')
                elif color_of_button == 'white' and ('car','yes') in lights:

                    button_held = True
                elif int(batteries) > 2 and ('frk','yes') in lights:
                    say_('press and release')
                elif color_of_button == 'yellow':

                    button_held = True
                elif color_of_button == 'red' and state_on_button[0] == 'hold':
                    say_('press and release')
                else:
                    say_('hold')
                    button_held = True
                if button_held:
                    say_('stripe color')
                    stripe_color = wait_()
                    if stripe_color  == 'blue':
                        say_('4 at any position')
                    elif stripe_color == 'white':
                        say_('1 at any position')
                    elif stripe_color == 'yellow':
                        say_('5 at any position')
                    else:
                        say_('1 at any position')
            else: continue
        elif recognized_text == 'password':
            word = password('one',[],[],[],[],[])
        elif recognized_text == 'wires':
            wires(False,0)
        elif recognized_text == 'complicated':
            complicated()
        elif recognized_text == 'sequence' or recognized_text == 'sequins':
            sequence('start',0,0,0)
        elif recognized_text == 'colors' or recognized_text == 'color' or recognized_text == 'carlos':
            simon_says([],0,0)
        elif recognized_text == 'memory':
            memory()
        elif recognized_text == 'morse' or recognized_text == 'moors' or recognized_text == 'morris' or recognized_text == 'morphs' or recognized_text == 'mars':
            morse()
        elif recognized_text == 'key' or recognized_text == 'keys' or  recognized_text == 'pad' or recognized_text == 'pads' or recognized_text == 'keypads' or recognized_text == 'keypad' or recognized_text == 'he':
            keypads()
        elif recognized_text == 'knob' or recognized_text == 'knobs' or recognized_text == 'needy':
            knobs()
        elif recognized_text == 'speech' or recognized_text == 'peach' or recognized_text == 'bitch':
            first()
        elif recognized_text == 'maze' or recognized_text == 'maison' or recognized_text == 'made' or recognized_text == 'maith' or recognized_text == 'hey' or recognized_text == 'it is' or recognized_text == 'phase' or recognized_text == "he's":
            maze() # :(

'''