import os
from vosk import Model, KaldiRecognizer
import pyaudio
import pyttsx3
import json
# LIST OF WORDS THAT SHOULD BE PUT INTO LUT BECAUSE BOT STUPID DD
# #desolate = detonate

#potential bugs:
#uhh i think when serial is not long enough it kinda fucks it over unsure tho
#not really a bug but sth that can be changed, on password gamemode i use double brackets because i tought there was a bug, you can remove one of the brackets but you would need to
#remove the [0] part  from rowX[0][_] and it should make stuff slightly cleaner, and also you wont really have to work on arrays inside of arrays, wont really mean that uch
# but to be fair could be changed later to make the code cleaner or so
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
mode = 'test'
numbers = {'zero': 0, 'one': 1, 'two': 2, 'three': 3, 'four': 4, 'five': 5, 'six': 6, 'seven': 7, 'eight': 8, 'nine': 9,
           'for': 4, 'aids': 8, 'aid': 8, 'tree': 3, 'free': 3, 'wow':1}


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
            res = listening()
            resp = res.replace('the','')
            response = resp.replace(' ','')
            if response in numbers:
                response = numbers[response]
            say_(f"{key}, {response}, correct?")
            print(f"{key}, {response}, correct?")

        confirm = listening()
        if confirm == 'yes':
            return response
        elif confirm == key:
            say_(f'lets try again')
        elif confirm == 'wrong':
            ask_for(key)
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
        letters_group = letters_replaced.split(' ')
        try:
            row_one = [letters_group[0][0],letters_group[1][0],letters_group[2][0],letters_group[3][0],letters_group[4][0],letters_group[5][0]]
        except IndexError:
            print(rows_done, 'wrong')
            password('one',r1,r2,r3,r4,r5)
        row1.append(row_one)
        say_(f'{row_one}, correct?')
        answer = wait_()
        print(answer)
        if answer == 'yes':
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
        letters_group = letters_replaced.split(' ')
        try:
            row_two = [letters_group[0][0],letters_group[1][0],letters_group[2][0],letters_group[3][0],letters_group[4][0],letters_group[5][0]]
        except IndexError:
            print(rows_done, 'wrong')
            password('two',r1,r2,r3,r4,r5)
        row2.append(row_two)
        say_(f'{row_two}, correct?')
        answer = wait_()
        print(answer)
        if answer == 'yes':
            print(row2)
            rows_done = 'three'

        elif answer == 'wrong':
            r2 = []
            password('two',r1,r2,r3,r4,r5)
        else: r2 = [];password('two',r1,r2,r3,r4,r5)
    if rows_done == 'three':
        say_('row three')
        letters = wait_()
        letters_replaced = letters.replace('the ', '')
        letters_group = letters_replaced.split(' ')
        try:
            row_three =[letters_group[0][0],letters_group[1][0],letters_group[2][0],letters_group[3][0],letters_group[4][0],letters_group[5][0]]
        except IndexError:
            print(rows_done, 'wrong')
            password('three',r1,r2,r3,r4,r5)
        row3.append(row_three)
        say_(f'{row_three}, correct?')
        answer = wait_()
        print(answer)
        if answer == 'yes':
            print(row3)
            rows_done = 'four'

        elif answer == 'wrong':
            r3 = [];password('three',r1,r2,r3,r4,r5)
        else: r3 = [];password('three',r1,r2,r3,r4,r5)
    if rows_done == 'four':
        say_('row four')
        letters = wait_()
        letters_replaced = letters.replace('the ', '')
        letters_group = letters_replaced.split(' ')
        try:
            row_four = [letters_group[0][0],letters_group[1][0],letters_group[2][0],letters_group[3][0],letters_group[4][0],letters_group[5][0]]
        except IndexError:
            print(rows_done, 'wrong')
            password('four',r1,r2,r3,r4,r5)
        row4.append(row_four)
        say_(f'{row_four}, correct?')
        answer = wait_()
        print(answer)
        if answer == 'yes':
            print(row4)
            rows_done = 'five'

        elif answer == 'wrong':
            r4 = [];password('four',r1,r2,r3,r4,r5)
        else: r4= [];password('four',r1,r2,r3,r4,r5)
    if rows_done == 'five':
        say_('row five')
        letters = wait_()
        letters_replaced = letters.replace('the ', '')
        letters_group = letters_replaced.split(' ')
        try:
            row_five = [letters_group[0][0], letters_group[1][0], letters_group[2][0],letters_group[3][0], letters_group[4][0], letters_group[5][0]]
        except IndexError:
            print(rows_done,'wrong')
            password('five',r1,r2,r3,r4,r5)
        row5.append(row_five)
        say_(f'{row_five}, correct?')
        answer = wait_()
        print(answer)
        if answer == 'yes':
            print(r1,r2,r3,r4,r5)
            for i in range(6):
                for j in range(6):
                    for k in range(6):
                        for l in range(6):
                            for m in range(6):
                                if debug:
                                    print(i,j,k,l,m)
                                    if len(row5[0]) < 6: say_('error')
                                    print(row1[0][i] , row2[0][j] , row3[0][k] , row4[0][l] , row5[0][m])
                                    print(row5)
                                    print(row4)
                                word = row1[0][i] + row2[0][j] + row3[0][k] + row4[0][l] + row5[0][m]
                                if word in password_LUT:
                                    say_(word)
                                    return
        elif answer == 'wrong':
            r5 = []
            password('five',r1,r2,r3,r4,r5)
        else:
            r5 = []
            password('five', r1, r2, r3, r4, r5)


password('five',[["a", "o", "p", "y", "t", "u"]],[["z", "l", "u" ,"o", "a", "h"]],[["z" ,"g" ,"f" ,"k" ,"l", "a"]],[["h" ,"v" ,"z" ,"c" ,"g","t"]],[])
#["h" ,"v" ,"z" ,"c" ,"g","t"]
while True:
    print("waiting")

    if mode == 'wait':
        recognized_text = listening()
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
        mode = 'play'
    elif mode == 'test':
        port = 'parallel'
        serial = 'abcdef'
        lights = ('asd','yes')
        batteries = 2
        mode = 'play'
    elif mode == 'play':
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
            say_('color')
            color_of_button = listening()
            if color_of_button == 'read':
                color_of_button = 'red'
            say_(f'button: {state_on_button}, color: {color_of_button}, correct?')
            answer = wait_()
            if answer == 'yes':
                if color_of_button == 'blue' and state_on_button == 'abort':
                    button_held = True
                    say_('hold')
                elif int(batteries) > 1 and state_on_button == 'detonate':
                    say_('press and release')
                elif color_of_button == 'white' and ('car','yes') in lights:
                    say_('hold')
                    button_held = True
                elif int(batteries) > 2 and ('frk','yes') in lights:
                    say_('press and release')
                elif color_of_button == 'yellow':
                    say_('hold')
                    button_held = True
                elif color_of_button == 'red' and state_on_button == 'hold':
                    say_('press and release')
                else:
                    say_('hold')
                    button_held = True
                if button_held:
                    say_('stripe color')
                    stripe_color = wait_()
                    if stripe_color == 'blue':
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

