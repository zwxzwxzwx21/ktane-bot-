import os
from vosk import Model, KaldiRecognizer
import pyaudio
import pyttsx3
import json
#code below changes the voice from polish to english
#region
engine = pyttsx3.init()
voices = engine.getProperty('voices')
for voice in voices:
    if "zira" in voice.id.lower():  # Use the ID for Microsoft Zira (English)
         engine.setProperty('voice', voice.id)
#endregion
info_dict = {} #this one stores values | CEREAL = SERIAL IDCCCCC

debug = True
model = Model('A:\\ktane bot\\vosk-model-en-us-0.22')
recognizer = KaldiRecognizer(model, 16000)
p = pyaudio.PyAudio()
stream = p.open(format=pyaudio.paInt16, channels=1, rate=16000, input=True,frames_per_buffer=8192)
stream.start_stream()
mode = 'go'

def convert_json(json_text):
    text = json.loads(json_text)
    return text['text']

def say_(text):
    engine = pyttsx3.init()
    engine.say(text)
    engine.runAndWait()

def button_(batteries,port,lights,serial):
    pass

def listening():



        while True:
            data = stream.read(4096, exception_on_overflow=False)
            if recognizer.AcceptWaveform(data):
                result = recognizer.Result()
                result_dict = json.loads(result)
                recognized_text = result_dict.get('text', '')
                return recognized_text

def ask_for(key):
    conf = False
    while True:
        if conf == False:
            say_(f'{key} waiting')
            response = listening()

            say_(f"{key}, {response}, correct?")
            print(f"{key}, {response}, correct?")

        confirm = listening()
        if confirm == 'yes':
            return response
        elif confirm == key:
            say_(f'lets try again')
        else:
            say_(f'unknown')
            conf = True #makes the bot remember the batteries if it wont understand 'yes' as an answer, you dont have to say it again

def wait_():
    while True:
        response = listening()
        if response:
            return response
        else: continue
def ask_for_advanced(key):
    #ports
    # for ports its cereal = serial, RCA (stereo),DVI,parallel,ps,rj
    port_LUT = {
                'cereal':'serial',
                'steral':'stereo',
                'sterile':'stereo',
                'stereo':'stereo',
                'serial':'serial',
                'd':'dvi',
                'd v i':'dvi',
                'ps': 'ps2',
                '2':'ps2',
                'parallel':'parallel',
                'forty five': 'rj',
                }
    if key == 'port':
        list = []
        number = 1
        while True:

            say_(f'{key} waiting')
            answer  = listening()
            if answer in port_LUT:
                list.append(port_LUT[answer])
                say_(f"{key}, {port_LUT[answer]}, done?")
                print(f"{key}, {port_LUT[answer]}, done?")

                confirm = wait_()

                if confirm == 'no':
                    print(list)
                    number += 1
                    say_(f'{key} {number}')
                elif confirm == key:
                    print(list)
                    number = 1
                    return ask_for_advanced(key)
                elif confirm == 'wrong':
                    if number > len(list):
                        number -= 1
                    del list[-1]
                    print(list,number)
                    say_('removed')
                elif confirm == 'yes':
                    print(list)
                    break
        return list
    #lights  | idea: lets say you have CAR lit and BOB not lit, you say 3 words like 'cristian, arnold, rock' and 'yes'
    #its always 3 long so then it proceses like: take first letter from first 3 words and then lit or 'no' (better over lit and unlit imo)
    #so it does have things going over n shit like that
    elif key == 'lights':
        list = []
        number = 1
        while True:

            say_(f'{key} waiting')
            answer = listening()
            if answer:
                answer_corrected = answer.replace('the','')
                print(answer_corrected)
                indicator = ''
                group = answer_corrected.split() #group ofwords from answer
                print(group)
                try:
                    for i in range(3):
                        indicator += group[i][0]
                except IndexError:
                    ask_for_advanced(key)
                light = (indicator, group[3])
                list.append(light)
                say_(f"{key}, {light}, done?")
                print(f"{key}, {light}, done?")

                confirm = wait_()

                if confirm == 'no':

                    print(list)
                    number += 1
                    say_(f'{key} {number}')
                elif confirm == key:
                    print(list)
                    number = 1
                    return ask_for_advanced(key)
                elif confirm == 'wrong':
                    if number > len(list):
                        number -= 1
                    del list[-1]
                    print(list, number)
                    say_('removed')
                elif confirm == 'yes':
                    print(list)
                    break
        return list

    elif key == 'serial':
        list = []
        numbers = {'zero':0,'one':1, 'two':2, 'three':3, 'four':4, 'five':5, 'six':6, 'seven':7, 'eight':8, 'nine':9,'for':4,'aids':8,'aid':8,'tree':3,'free':3}
        while True:

            say_(f'{key} waiting')
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

                say_(f"{key}, {' '.join(indicator)}, correct?")
                print(f"{key}, {serial}, correct?")

                confirm = wait_()

                if confirm == 'no':
                    print(serial)
                    say_(f'{key} ')

                elif confirm == key:
                    print(serial)
                    return ask_for_advanced(key)

                elif confirm == 'yes':
                    print(list)
                    return serial
                    break

        return serial

while True:
    print("waiting")
    recognized_text = listening()
    if mode == 'wait':
        if recognized_text == 'go':
            say_('start')
            mode = 'go'
        else:
            print(recognized_text)
    elif mode == 'go':
        port = ask_for_advanced("port")
        info_dict["port"] = port
        say_(f"port: {', '.join(port)}")

        serial = ask_for_advanced("serial")
        info_dict["serial"] = serial
        say_(f'serial: {serial}')

        lights = ask_for_advanced("lights")
        info_dict["lights"] = lights
        say_(f'lights: {lights}')

        batteries = ask_for("batteries")
        info_dict["batteries"] = batteries
        say_(f'batteries: {batteries}')






        mode = 'wait'
