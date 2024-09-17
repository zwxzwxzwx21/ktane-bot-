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
###UNIMPLEMENTED
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
           'for': 4, 'aids': 8, 'aid': 8, 'tree': 3, 'free': 3, 'wow':1,'too':2}

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

def simon_says(color_array,loop,strike):
    colors = color_array
    engine.setProperty('rate', speed_up)
    has_vowel = False
    vowels = ['a', 'e', 'i', 'o', 'u']
    for sign in serial:
        if sign in vowels:
            has_vowel = True
            break
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

            say_(f'press {number3}')
        elif level5 == 4:

            say_(f'press {number4}')

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
    morse_code = morse_code.split(' ')
    if morse_code == 'module':
        return
    one_sign = []
    solution = ''
    for sign in morse_code:
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
            print(f' current solution {solution}')
            one_sign = []
        else:
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
    signs = signs.replace('see','c')
    signs = signs.replace('tree','three')
    signs = signs.replace('free','three')
    signs = signs.replace('tea','three')
    signs = signs.replace('start','star')
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
    for keys in keypad1:
        if keys not in k_array1:
            k_array1.remove(keys)
    for keys in keypad2:
        if keys not in k_array2:
            k_array2.remove(keys)
    for keys in keypad3:
        if keys not in k_array3:
            k_array3.remove(keys)
    for keys in keypad4:
        if keys not in k_array4:
            k_array4.remove(keys)
    for keys in keypad5:
        if keys not in k_array5:
            k_array5.remove(keys)
    for keys in keypad6:
        if keys not in k_array6:
            k_array6.remove(keys)

    if kp1 == 4:
        say_(f'{keypad1[0]} {keypad1[1]} {keypad1[2]} {keypad1[3]} ')
    elif kp2 == 4:
                say_(f'{keypad2[0]} {keypad2[1]} {keypad2[2]} {keypad2[3]}  ')
    elif kp3 == 4:
                say_(f'{keypad3[0]} {keypad3[1]} {keypad3[2]} {keypad3[3]} ')
    elif kp4 == 4:
                say_(f'{keypad4[0]} {keypad4[1]} {keypad4[2]} {keypad4[3]}  ')
    elif kp5 == 4:
                say_(f'{keypad5[0]} {keypad5[1]} {keypad5[2]} {keypad5[3]} ')
    elif kp6 == 4:
                say_(f'{keypad6[0]} {keypad6[1]} {keypad6[2]} {keypad6[3]}  ')

    return
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
        port = 'parallel'
        serial = 'zzzzzz'
        lights = ('asd', 'yes')
        batteries = 2
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
