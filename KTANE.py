import os
from vosk import Model, KaldiRecognizer
import pyaudio
import pyttsx3
import json

speed_up = 225 # speed and slowed down voice for bot to read faster or slower if needed
slow_down = 175
# LIST OF WORDS THAT SHOULD BE PUT INTO LUT BECAUSE BOT STUPID DD
# #desolate = detonate
positive_answers = ['yes','s','this','us','ps','as']
#potential bugs n todo:
#uhh i think when serial is not long enough it kinda fucks it over unsure tho
#not really a bug but sth that can be changed, on password gamemode i use double brackets because i tought there was a bug, you can remove one of the brackets but you would need to
#remove the [0] part  from rowX[0][_] and it should make stuff slightly cleaner, and also you wont really have to work on arrays inside of arrays, wont really mean that uch
# but to be fair could be changed later to make the code cleaner or so
#another thing, could be fixed already but idk, when bot wont understand 'yes' or 'wrong' it could go to say_('module') line which is really bad because it loses all progress
# if the error is still there FUCKING FIX IT
# make the bot read passwords faster - DONE

# GAMES TO REPLICATE
#region
###IMPLEMENTED
#BUTTON - WORKS 100% NO ERRORS FOUND
#PASSWORD - WORKS 100% NO ERRORS FOUND
#WIRES - HAVENT HAD AN ERROR RELATED TO SERIAL NUMBER, NEED TO TESTCASE THAT!!!
###UNIMPLEMENTED
#COMPLICATED (COMPLICATED WIRES) - PROB NEXT ONE, REALLY EASY
#SEQUENCE (WIRE SEQUENCE) - SEEMS EASY TBH, JUST MAKE IT SO SEA,SEE,C = C
#SIMON SAYS - PISS EASY JUST ASK FOR COLORS STRIKES N SHIT, AND CHECK FOR VOWELS
#MEMORY - JUST SAY 2 THINGS, MAIN NUMBER AND WHAT YOURE PRESSING LIKE 'PRESSING 2' AND YOU SHOULD BE DONE, GL WITH THE BOT RECOGNIZING IT EVERY TIME CORRECTLY THO XD
#MORSE - IDEK, DO BEFORE MAZE BUT STILL KINDA HARD SEEMS, PROB DO THE SAME AS PASSWORD
#KEYPADS - WELL TOU GONNA DO STH LIKE A SIGN THAT LOOKS LIKE A  C JUST IS A C AND BOT WILL GET IT YE???
#MAZE - FUCKING HELL NAH
#KNOBS - SEEMS HARD
#FIRST - FOR EMPTY SAY EMPTY, I THINK THE BEST THING IS TO USE SOME FUCKED UP PRONOUNCE TO WORK THIS OUT (THEIR , THERE = THERE, DEER = THEIR XD, TRY USING NUMBERS TOO, HONESLT YIT SEEMS THE WORST!!!!!!!!!!)

#endregion
#code below changes the voice from polish to english
#region
engine = pyttsx3.init()
engine.setProperty('read',210)
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

def remove_the(text):
    a = text.replace('the ','')
    return a

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
        if confirm in positive_answers:
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
            answer_  = listening()
            answer = remove_the(answer_)
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
            answer_ = listening()
            answer = remove_the(answer_)
            if answer:
                answer_corrected = answer.replace('the ','')
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
        row1 = row_one
        engine.setProperty('rate', speed_up)
        say_(f'{letters_group[0][0]} {letters_group[1][0]} {letters_group[2][0]} {letters_group[3][0]} {letters_group[4][0]} {letters_group[5][0]}, correct?')
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
        letters_group = letters_replaced.split(' ')
        try:
            row_two = [letters_group[0][0],letters_group[1][0],letters_group[2][0],letters_group[3][0],letters_group[4][0],letters_group[5][0]]
        except IndexError:
            print(rows_done, 'wrong')
            print('function : two',r1,r2,r3,r4,r5)
            password('two',r1,r2,r3,r4,r5)
        row2 = row_two
        say_(f'{letters_group[0][0]} {letters_group[1][0]} {letters_group[2][0]} {letters_group[3][0]} {letters_group[4][0]} {letters_group[5][0]}, correct?')
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
        letters_group = letters_replaced.split(' ')
        try:
            row_three =[letters_group[0][0],letters_group[1][0],letters_group[2][0],letters_group[3][0],letters_group[4][0],letters_group[5][0]]
        except IndexError:
            print(rows_done, 'wrong')
            password('three',r1,r2,r3,r4,r5)
        row3 = row_three
        engine.setProperty('rate',speed_up)
        say_(f'{letters_group[0][0]} {letters_group[1][0]} {letters_group[2][0]} {letters_group[3][0]} {letters_group[4][0]} {letters_group[5][0]}, correct?')
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
        letters_group = letters_replaced.split(' ')
        try:
            row_four = [letters_group[0][0],letters_group[1][0],letters_group[2][0],letters_group[3][0],letters_group[4][0],letters_group[5][0]]
        except IndexError:
            print(rows_done, 'wrong')
            password('four',r1,r2,r3,r4,r5)
        row4 = row_four
        engine.setProperty('rate', speed_up)
        say_(f'{letters_group[0][0]} {letters_group[1][0]} {letters_group[2][0]} {letters_group[3][0]} {letters_group[4][0]} {letters_group[5][0]}, correct?')
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
        letters_group = letters_replaced.split(' ')
        try:
            row_five = [letters_group[0][0], letters_group[1][0], letters_group[2][0],letters_group[3][0], letters_group[4][0], letters_group[5][0]]
        except IndexError:
            print(rows_done,'wrong')
            password('five',r1,r2,r3,r4,r5)
        row5 = row_five
        engine.setProperty('rate', speed_up)
        say_(f'{letters_group[0][0]} {letters_group[1][0]} {letters_group[2][0]} {letters_group[3][0]} {letters_group[4][0]} {letters_group[5][0]}, correct?')
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
        say_('wrong colors')
        wires(True,wire_number)

    say_(f'{colors_group}')
    answer_ = wait_()
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
            for signs in serial:
                try:
                    #int(signs)
                    last_int = int(signs)
                except ValueError:
                    continue
            if last_int % 2 == 1 and colors_group.count('red')>1: say_('cut last red')
            elif colors_group.count('red') == 0 and colors_group[-1] == 'yellow': say_('cut first')
            elif colors_group.count('blue') == 1: say_('cut first')
            elif colors_group.count('yellow') > 1: say_('cut last')
            else: say_('cut second')
        elif wire_number == 5:
            for signs in serial:
                try:
                    #int(signs)
                    last_int = int(signs)
                except ValueError:
                    continue
            if last_int % 2 == 1 and colors_group[-1] =='black': say_('cut fourth')
            elif colors_group.count('red') == 1 and colors_group.count('yellow') > 1: say_('cut first')
            elif colors_group.count('black') == 0: say_('cut second')
            else: say_('cut first')
        elif wire_number == 6:
            for signs in serial:
                try:
                    #int(signs)
                    last_int = int(signs)
                except ValueError:
                    continue
            if last_int % 2 == 1 and colors_group.count('yellow') == 0: say_('cut third')
            elif colors_group.count('yellow') == 1 and colors_group.count('white') > 1: say_('cut fourth')
            elif colors_group.count('red') == 0: say_('cut last')
            else: say_('cut fourth')
    elif answer == 'wrong':
        wires(True,wire_number)
    else:
        wires(True,wire_number)
    engine.setProperty('read',200)
    return
#password('one',[],[],[],[],[])
#5:["h" ,"v" ,"z" ,"c" ,"g","t"] 3:["z" ,"g" ,"f" ,"k" ,"l", "a"],4:["h" ,"v" ,"z" ,"c" ,"g","t"] 1: ["a", "o", "p", "y", "t", "u"],2:["z", "l", "u" ,"o", "a", "h"]
def complicated():
    say_('complicated')
    # idea basically separete wired by next and make bot just say, cut,skip...
    wires = wait_()
    wires_replaced2 = wires.replace('the ', '')
    wires_replaced3 = wires_replaced2.replace('read', 'red')
    wires_replaced = wires_replaced3.replace('start', 'star')
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
        if words == 'next':
            if 'lit' in wire_desc:
                if 'red' not in wire_desc and 'blue' not in wire_desc and 'star' not in wire_desc:
                    things_to_do.append('skip') # right D
                elif 'blue' in wire_desc and 'parallel' in port and 'red' not in wire_desc and 'star' not in wire_desc:
                    things_to_do.append('cut')# right P
                elif 'red' not in wire_desc and 'blue' not in wire_desc and 'star' in wire_desc and batteries > 1:
                    things_to_do.append('cut')# bottom B
                elif 'red' in wire_desc and 'blue' not in wire_desc  and batteries > 1:
                    things_to_do.append('cut') # star does not matter here, making it 2 | right down B
                elif 'blue' in wire_desc and 'parallel' in port and 'red' not in wire_desc and 'star' in wire_desc:
                    things_to_do.append('cut') # left down P
                elif 'red' in wire_desc and 'blue' in wire_desc and is_even == True and 'star' not in wire_desc:
                    things_to_do.append('cut') # middle right S
                elif 'star' in wire_desc and 'red' in wire_desc and 'blue' in wire_desc:
                    things_to_do.append('dont') # middle D
            else:
                if 'blue' not in wire_desc and 'red' not in wire_desc and 'star' not in wire_desc:
                    things_to_do.append('cut') # upper C
                elif 'blue' in wire_desc and 'star' not in wire_desc and 'red' not in wire_desc and is_even == True:
                    things_to_do.append('cut') # upper right S
                elif 'blue' in wire_desc and 'star' not in wire_desc and 'red' in wire_desc and is_even == True:
                    things_to_do.append('cut') # middle S
                elif 'blue' not in wire_desc and 'star' not in wire_desc and 'red' in wire_desc and is_even == True:
                    things_to_do.append('cut') # upper left S
                elif 'blue' in wire_desc and 'star' in wire_desc and 'red' in wire_desc and 'parallel' in port:
                    things_to_do.append('cut') # middle left P
                elif 'red' not in wire_desc and 'blue' in wire_desc and 'star' in wire_desc:
                    things_to_do.append('skip') # bottom left D
                elif 'red' not in wire_desc and 'blue' not in wire_desc and 'star' in wire_desc:
                    things_to_do.append('cut') # middle left C
                elif 'red' in wire_desc and 'blue' in wire_desc and 'star' in wire_desc:
                    things_to_do.append('cut') # upper left C
    for instruction in things_to_do:
        engine.setProperty('read',240)
        say_(instruction)
        engine.setProperty('read',200)




            wire_desc = []
        else:
            wire_desc.append(words)


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
        serial = 'ee5ek5'
        lights = ('asd','yes')
        batteries = 2
        mode = 'play'
    elif mode == 'play':
        #region
        '''port = 'parallel'
        serial = 'ee5ek5'
        lights = ('asd', 'yes')
        batteries = 2'''
        #endregion
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
            say_('color')
            color_of_button = listening()
            if color_of_button == 'read':
                color_of_button = 'red'
            say_(f'button: {state_on_button}, color: {color_of_button}, correct?')
            answer_ = wait_()
            answer = remove_the(answer_)
            if answer in positive_answers:
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
        elif recognized_text == 'wires':
            wires(False,0)
        elif recognized_text == 'complicated':
            complicated = complicated()

