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
import math

global parallel_port
parallel_port = False


def find_unique_match(string, lut):
    possible_matches = []

    # Przeszukiwanie LUT w poszukiwaniu dopasowań prefiksowych
    for pattern, value in lut.items():
        for i in range(len(pattern)):
            shifted_pattern = pattern[i:] + pattern[:i]
            # Jeśli string jest prefiksem przesuniętego wzorca, dodajemy go do dopasowań
            if shifted_pattern.startswith(string):
                possible_matches.append(value)

    # Sprawdzamy, czy pozostało dokładnie jedno możliwe dopasowanie
    if len(possible_matches) == 1:
        return possible_matches[0]  # Zwracamy jedyne możliwe dopasowanie

    return None
def do_morse():
    print('DOING MORSE')
    light_lut = \
        {
            (253, 222, 71) : "lit",
            (118, 63, 41) : "unlit"
        }
    #0.28s dot
    #0.81s dash
    #1.10s long break
    #0.28s short break
    #2.70s pause.
    morse_LUT = {
        'shell': 505,
        'halls': 515,
        'slick': 522,
        'trick': 532,
        'boxes': 535,
        'leaks': 542,
        'strobe': 545,
        'bistro': 552,
        'flick': 555,
        'bombs': 565,
        'break': 572,
        'brick': 575,
        'steak': 582,
        'sting': 592,
        'vector': 595,
        'beats': 600
    }
    morse_moves = {
        'shell': 0,
        'halls': 1,
        'slick': 2,
        'trick': 3,
        'boxes': 4,
        'leaks': 5,
        'strobe': 6,
        'bistro': 7,
        'flick': 8,
        'bombs': 9,
        'break': 10,
        'brick': 11,
        'steak': 12,
        'sting': 13,
        'vector': 14,
        'beats': 15
    }
    morse_LUT2 = ['shell', 'halls', 'slick', 'trick', 'boxes', 'leaks', 'strobe', 'bistro', 'flick', 'bombs', 'break',
                  'brick', 'steak', 'sting', 'vector', 'beats']
    morse_decode_LUT = {
        '.-': 'a',
        '-...': 'b',
        '-.-.': 'c',
        '-..': 'd',
        '.': 'e',
        '..-.': 'f',
        '--.': 'g',
        '....': 'h',
        '..': 'i',
        '.---': 'j',
        '-.-': 'k',
        '.-..': 'l',
        '--': 'm',
        '-.': 'n',
        '---': 'o',
        '.--.': 'p',
        '--.-': 'q',
        '.-.': 'r',
        '...': 's',
        '-': 't',
        '..-': 'u',
        '...-': 'v',
        '.--': 'w',
        '-..-': 'x',
        '-.--': 'y',
        '--..': 'z'
    }
    #region
    '''one_sign = []
    solution = ''

    numb_of_signs = 0
    for sign in morse_code:
        possible_sols = []
        if sign == 'next' or sign == 'mixed':
            temp_word = ''
            for signs in one_sign:
                print(f'current sign {sign}', f' one sign: {one_sign}', f'current signs {signs}')
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
                say_(possible_sols);
                return
            print(f' current solution {solution}')
            one_sign = []
        else:
            if sign == 'module': return
            one_sign.append(sign)
            print('appending one sign', one_sign)
    print(f'solution : {solution}')'''
    #endregion
    sign_array = []

    '''while True:

        print(f' {pyautogui.pixel(1220, 513)}')
        time.sleep(0.28)'''
    import pyautogui
    import time

    pixel_x, pixel_y = 1220, 513

    answer_lut = \
        {
        "N.........-...-.." :  'shell',
        'N.....-.-...-.....' : 'halls',
        'N....-....-.-.-.-' :  'slick',
        'N-.-...-.-.-.-' :        'trick',
        'N-...----..-....' :   'boxes',
        'N.-....--.-...' :      'leaks',
        'N...-.-.----....' :     'strobe',
        'N-........-.-.---' :     'bistro',
        'N..-..-....-.-.-.-' :    'flick',
        'N-...------......' :  'bombs',
        'N-....-...--.-' :     'break',
        'N-....-...-.-.-.-' :   'brick',
        'N...-..--.-':          'steak',
        'N...-..-.--.':           'sting',
        'N...-.-.-.----.-.':     'vector',
        'N-.....--...':         'beats',

        }

    time_per_loop = 0.01
    dot_threshold = int(0.30 / time_per_loop)
    dash_threshold = int(0.85 / time_per_loop)
    intra_gap_threshold = int(0.30 / time_per_loop)
    char_gap_threshold = int(1.11 / time_per_loop)
    word_gap_threshold = int(2.75 / time_per_loop)

    durations = []
    current_state = None
    loop_count = 0
    results = []
    string = ''
    state_transition_count = 0
    try:
        print("Monitoring pixel for Morse code... Press Ctrl+C to stop.")
        while True:
            pixel_color = pyautogui.pixel(pixel_x, pixel_y)
            new_state = "lit" if closest_color(pixel_color, light_lut) == "lit" else "unlit"

            if new_state != current_state:
                if current_state is not None and loop_count > 0:
                    state_transition_count += 1
                    if state_transition_count > 2:
                        if current_state == "lit":
                            string += '.' if loop_count <= dash_threshold else '-'
                        elif current_state == "unlit":
                            if loop_count > char_gap_threshold:
                                string += "" if loop_count <= word_gap_threshold else "N"
                        print(string)
                        # Sprawdź dopasowanie w czasie rzeczywistym
                        match = find_unique_match(string, answer_lut)
                        if match:
                            print(f"Znaleziono unikalne dopasowanie: {match}")
                            break  # Zakończ pętlę

                    loop_count = 0
                current_state = new_state

            loop_count += 1

    except KeyboardInterrupt:
        print("Monitoring stopped.")
        print("Final Morse code interpretation:")
        print(string)
    print(morse_moves[match])
    for i in range(morse_moves[match]):
        pyautogui.click(1482,758)
    pyautogui.click(1315,886)
    return
def maze_reverse(maze_map, current_number, goal_position, array_of_path_pos):
    while current_number > 0:
        current_number -= 1
        print(f' inside while loop checking for {current_number}')
        if goal_position[0] + 2 < 13:
            if maze_map[goal_position[1]][goal_position[0] + 2] == str(current_number)\
                    and maze_map[goal_position[1]][goal_position[0] + 1] != '■':  # right
                print(f'current number found at {goal_position[0] + 2}, {goal_position[1]}')
                goal_position = (goal_position[0] + 2, goal_position[1])
                array_of_path_pos.append(goal_position)
        if goal_position[0] - 2 > 0:
            if maze_map[goal_position[1]][goal_position[0] - 2] == str(current_number)\
                    and maze_map[goal_position[1]][goal_position[0] - 1] != '■':  # left
                print(f'current number found at {goal_position[0] - 2}, {goal_position[1]}')
                goal_position = (goal_position[0] - 2, goal_position[1])
                array_of_path_pos.append(goal_position)
        if goal_position[1] - 2 > 0:
            if maze_map[goal_position[1] - 2][goal_position[0]] == str(current_number)\
                    and maze_map[goal_position[1] - 1][goal_position[0]] != '■':  # up
                print(f'current number found at {goal_position[0]}, {goal_position[1] - 2}')
                goal_position = (goal_position[0], goal_position[1] - 2)
                array_of_path_pos.append(goal_position)
        if goal_position[1] + 2 < 13:
            if maze_map[goal_position[1] + 2][goal_position[0]] == str(current_number)\
                    and maze_map[goal_position[1] + 1][goal_position[0]] != '■':  # down
                print(f'current number found at {goal_position[0]}, {goal_position[1] + 2}')
                goal_position = (goal_position[0], goal_position[1] + 2)
                array_of_path_pos.append(goal_position)

    else:
        array_of_path_pos.reverse()
        print(array_of_path_pos, '123')
        return array_of_path_pos


def maze_solver(maze_map, starting_pos, goal_position, loop_array, current_number):
    # path = []
    loop_finished = False
    finish_found = False
    # loop array is an arrat that has number positions
    # current number is  number of loops in floodfill search
    print(current_number, loop_array, goal_position, 'cur number and loop array and goal pos')
    # maze_map[start_pos[1]][start_pos[0]] = current_num
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
                    pos = (numbers[0] + 2, numbers[1])
                    print('appending position', pos)
                    array_of_pos.append(pos)  # return as loopm array
                if maze_map[numbers[1]][numbers[0] + 2] == 'F':
                    print('finish found')
                    print(f'calling function with current number {current_number} and array = {[goal_position]}')
                    path = maze_reverse(maze_map, current_number, goal_position, [goal_position])
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
                    path = maze_reverse(maze_map, current_number, goal_position, [goal_position])
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
                    path = maze_reverse(maze_map, current_number, goal_position, [goal_position])
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
                    path = maze_reverse(maze_map, current_number, goal_position, [goal_position])
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
    pyautogui.PAUSE = 0.15
    # try:
    if finish_found:
        print(' finish found ')
        if len(path) > 0:
            print('path', path)
            for i in range(len(path)):
                try:
                    if path[i][0] + 2 == path[i + 1][0]:
                        moves_to_do.append('right')
                    if path[i][0] - 2 == path[i + 1][0]:
                        moves_to_do.append('left')
                    if path[i][1] - 2 == path[i + 1][1]:
                        moves_to_do.append('up')
                    if path[i][1] + 2 == path[i + 1][1]:
                        moves_to_do.append('down')
                except:
                    break
        print(moves_to_do, ' moves to do')
        string_moves = ''

        for move in moves_to_do:

            string_moves += move
        print(string_moves, "stirng to do")

        for moves in moves_to_do:

            '''screen = pyautogui.screenshot(region=(1050, 460, 500, 500))
            screen = np.array(screen)
            screen = cv2.cvtColor(screen, cv2.COLOR_BGR2RGB)
            screen[250, 15] = (0, 0, 255) # left
            screen[250, 450] = (0, 0, 255) # right
            screen[30, 250] = (0, 0, 255) # up
            screen[470, 250] = (0, 0, 255) # down'''
            pyautogui.PAUSE = 0.05
            if moves == 'left':
                pyautogui.click(1050+15,460+250)
            elif moves == 'right':
                pyautogui.click(1050+450,460+250)
            elif moves == 'up':
                pyautogui.click(1050+250,460+30)
            elif moves == 'down':
                pyautogui.click(1050+250,460+470)
            '''cv2.imshow('screen', screen)
            cv2.waitKey(0)'''
            print("foing moces")
            #time.sleep(1)
        return

    if current_number < 37 and loop_finished == False:
        maze_solver(maze_map, starting_pos, goal_position, array_of_pos, current_number)


def distance_to_colors(pixel):
    white = np.array([255, 255, 255])
    black = np.array([0, 0, 0])
    distance_to_white = np.linalg.norm(pixel - white)
    distance_to_black = np.linalg.norm(pixel - black)
    return distance_to_white, distance_to_black
cable_LUT =  \
        {
            (24, 27, 31) : None,

            (255, 255, 255) : "white",
            (255, 253, 236) : "white", # pos 3
            (209, 200, 186) : "white", # pos 4
            (215, 205, 191) : "white", # pos 4
            (210, 201, 187) : "white", # pos 4
            (255, 252, 235) : "white", # pos 6
            (239, 228, 212) : "white", # pos 5
            (241, 230, 214) : "white",

            (255, 98, 36) : 'red',
            (255, 142, 56) : "red", # pos 1
            (255, 100, 36) : 'red', # pos 2
            (255, 9, 7) : 'red', # pos 5
            (234, 8, 6): 'red', # pos 4
            (255, 10, 12): 'red', # pos 6 / pos 3

            (255, 255, 50) : "yellow",
            (255, 255, 52) : "yellow", # pos 1
            (255, 255, 54) : "yellow", # pos 1
            (255, 255, 36) : "yellow", # pos 2
            (234, 194, 6): "yellow", # pos 4
            (238, 197, 6): "yellow", # pos 4
            (255, 245, 12): "yellow", # pos 3 / pos 6
            (255, 223, 7) : "yellow", # pos 5
            (255, 244, 12) : "yellow", # pos 6

            (5, 4, 3) : "black",
            (8, 8, 8) : "black", # pos 1
            (10, 9, 8) : "black", # pos 1
            (2, 3, 2) : "black", # pos 5
            (6, 6, 6) : "black", # pos 2
            (0, 0, 0) : "black", # pos 3
            (2, 2, 2) : "black", # pos 3

            (57, 82, 216) : "blue",
            (57,82,217): "blue", # pos 3
            (57,82,218): "blue", # pos 3
            (57,82,219): "blue", # pos 3
            (93, 153, 244): "blue",
            (55, 76, 196): "blue", # pos 5
            (70, 114, 233): "blue", # pos 2
            (48, 67, 172): "blue", # pos 4
            (57, 83, 217): "blue", # pos 6
            (70, 114, 234): "blue", # pos 2
        }
password_color_lut = \
    {
        (30, 65, 10) : "go",
        (126, 204, 22) : None,
        (51, 74, 7) : "go",
        (34, 67, 8) : "go",
        (88, 185, 27) : None,
        (112, 200, 22) : None,
        (137, 210, 19) : None,
        (148, 214, 19) : None,
    }
def closest_color(rgb_color,lut):
    min_distance = float("inf")
    closest_color_name = None
    for color,name in lut.items():
        distance = math.sqrt(sum((rgb_color[i] - color[i]) ** 2 for i in range(3)))
        if distance < min_distance:
            min_distance = distance
            closest_color_name = name
    return closest_color_name
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


def do_maze():
    print('DOING MAZE')

    # i dont feel like doing loop xd
    '''screen[180, 95] = (0, 0, 255)   # maze 1
    screen[180, 290] = (0, 0, 255)  # maze 2
    screen[275, 385] = (0, 0, 255)  # maze 3
    screen[115, 105] = (0, 0, 255)  # maze 4
    screen[400, 270] = (0, 0, 255)  # maze 5
    screen[110, 310] = (0, 0, 255)  # maze 6
    screen[115, 155] = (0, 0, 255)  # maze 7
    screen[110, 260] = (0, 0, 255)  # maze 8
    screen[165, 200] = (0, 0, 255)  # maze 9'''
    maze_number = []

    print("pixel color maze #1: ", pyautogui.pixel(1050 + 95, 460 + 180))
    print("pixel color maze #2: ",pyautogui.pixel(1050+290, 460+180))
    print("pixel color maze #3: ",pyautogui.pixel(1050+385, 460+275))
    print("pixel color maze #4: ", pyautogui.pixel(1050 + 105, 460 + 115))
    print("pixel color maze #5: ",pyautogui.pixel(1050+270, 460+400))
    print("pixel color maze #6: ",pyautogui.pixel(1050+310, 460+115))
    print("pixel color maze #7: ",pyautogui.pixel(1050+155, 460+115))
    print("pixel color maze #8: ",pyautogui.pixel(1050+260, 460+110))
    print("pixel color maze #9: ",pyautogui.pixel(1050+200, 460+165))
    color_LUT = \
        {
            (76, 163, 57) : "maze 1",
            (77, 164, 57) : "maze 1",
            (78, 166, 58) : "maze 1",
            (99, 210, 71) : "maze 2",
            (66, 136, 51) : "maze 3",
            (66, 139, 52) : "maze 3",
            (68, 141, 53) : "maze 3",
            (99, 206, 70) : "maze 4",
            (101, 210, 70): "maze 4",
            (99, 205, 70) : "maze 4",
            (68, 142, 54) : "maze 5",
            (69, 144, 54) : "maze 5",
            (60, 126, 45) : "maze 6",
            (66, 138, 48) : "maze 6",
            (65, 135, 47) : "maze 6",
            (60, 127, 45) : "maze 6",
            (59, 122, 45) : "maze 6",
            (57, 121, 43) : "maze 6",
            (76, 157, 59) : "maze 7",
            (76, 158, 58) : "maze 7",
            (72, 153, 58) : "maze 7",
            (81, 164, 60) : "maze 7",
            (75, 157, 59) : "maze 7",
            (74, 154, 53) : "maze 8",
            (75, 156, 54) : "maze 8",
            (75, 155, 54) : "maze 8",
            (69, 145, 51) : "maze 8",
            (103, 215, 73): "maze 9",


        }
    pos_LUT = \
        {
            (214, 0, 8) : "goal",
            (211, 218, 220) : "start",

        }

    #im changing maze number to maze map cuz it makes no sense to have 2 variables for the same thing kinda
    if pyautogui.pixel(1050 + 95, 460 + 180) in color_LUT:
        print(color_LUT[pyautogui.pixel(1050 + 95, 460 + 180)])
        maze_number = [
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
    elif pyautogui.pixel(1050+290, 460+180) in color_LUT:
        print(color_LUT[pyautogui.pixel(1050+290, 460+180)])
        maze_number = [
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
    elif pyautogui.pixel(1050+385, 460+275) in color_LUT:
        print(color_LUT[pyautogui.pixel(1050+385, 460+275)])
        maze_number = [
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
    elif pyautogui.pixel(1050 + 105, 460 + 115) in color_LUT:
        print(color_LUT[pyautogui.pixel(1050 + 105, 460 + 115)])
        maze_number = [
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
    elif pyautogui.pixel(1050+270, 460+400) in color_LUT:
        print(color_LUT[pyautogui.pixel(1050+270, 460+400)])
        maze_number = [
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
    elif pyautogui.pixel(1050+310, 460+115) in color_LUT:
        print(color_LUT[pyautogui.pixel(1050+310, 460+115)])
        maze_number = [
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
        ]
    elif pyautogui.pixel(1050 + 155, 460 + 115) in color_LUT:
        print(color_LUT[pyautogui.pixel(1050+155, 460+115)])
        maze_number = [
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
    elif pyautogui.pixel(1050+260, 460+110) in color_LUT:
        print(color_LUT[pyautogui.pixel(1050+260, 460+110)])
        maze_number = [
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
    elif pyautogui.pixel(1050+200, 460+165) in color_LUT:
        print(color_LUT[pyautogui.pixel(1050+200, 460+165)])
        maze_number = [
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
        ]
    else:
        '''pyautogui.click(button="right")
        time.sleep(0.1)
        pyautogui.click(button="right")
        
        do_maze()''' #dont worry about it :3
        #upper one is like, place down and pick up bomb nbut its fucked kinda
        print("something is off | try placing the bomb and picking it up again, that helps")

    start_pos = ()
    end_pos = ()
    for x in range(6):
        for y in range(6):
            print(pyautogui.pixel(1050+118+x*49, 460  +135+y*49))
            #screen[135+y*49,118+x*49] = (0,0,255)
            if pyautogui.pixel(1050+118+x*49, 460  +135+y*49) == (211, 218, 220):
                # start
                start_pos = (x,y)
            elif pyautogui.pixel(1050+118+x*49, 460  +135+y*49) == (214, 0, 8):
                #end
                end_pos = (x,y)

    '''cv2.imshow('screen', screen)
    cv2.waitKey(0)'''
    print(start_pos,end_pos)
    start_pos_resized = [start_pos[0]*2+1,start_pos[1]*2+1]
    #start_pos_resized = (5,5)
    end_pos_resized = [end_pos[0]*2+1,end_pos[1]*2+1]
    print(start_pos_resized, end_pos_resized)
    print(type(start_pos_resized), ' ???')
    maze_number[start_pos_resized[1]][start_pos_resized[0]] = '0'
    maze_number[end_pos_resized[1]][end_pos_resized[0]] = 'F'

    maze_solver(maze_number,start_pos_resized,end_pos_resized,[start_pos_resized],0)

    def maze():
        # cry for help will not save my tarnished soul
        # idea is like, if you will be maze 6 and check both dead ends, just return to starting position and choose different direction
        # notes 2, here i think the best idea is, to black out all the places that are not goal and are dead ends, so when you take a bad
        # turn at maze 9 , and you check both dead ends, with no checkpoint behind that, returning to start is fine AS LONG AS you will just block
        # everything you have explored FROM THE CHECKPOINT, so you will not block what is an actuall path
        # circle positions (0 index, (x,y))
        say_('maze, position')
        position = wait_()
        position = remove_the(position)
        position = position.replace('you know', 'zero')
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
        print('circle positions', position)
        for word in position:
            if word in numbers:
                circle_pos += (numbers[word],)
        # MAPS
        # region

        #maze maps were here
          # podwojne rozwidlenie ale read idea
          # check notes 2
        # endregion
        print(circle_pos, 'position fo circles')
        maze1 = [(0, 1), (5, 2), (0, 1,), (5, 2,)]
        maze2 = [(1, 3), (4, 1), (1, 3,), (4, 1,)]
        maze3 = [(3, 3), (5, 3), (3, 3,), (5, 3,)]
        maze4 = [(0, 0), (0, 3), (0, 0,), (0, 3,)]
        maze5 = [(4, 2), (3, 5), (4, 2,), (3, 5,)]
        maze6 = [(4, 0), (2, 4), (4, 0,), (2, 4,)]
        maze7 = [(1, 0), (1, 5), (1, 0,), (1, 5,)]
        maze8 = [(3, 0), (2, 3), (3, 0,), (2, 3,)]
        maze9 = [(2, 1), (0, 4), (2, 1,), (0, 4,)]
        # my pos * 2 + 1 = new pos
        say_('start position')
        starting_pos = wait_()
        starting_pos = remove_the(starting_pos)
        starting_pos = starting_pos.replace('you know', 'zero')
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
        print(starting_pos, 'starting pos variable')
        start_pos = ()
        for word in starting_pos:
            if word in numbers:
                start_pos += (numbers[word] * 2 + 1,)
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
                goal_pos += (numbers[word] * 2 + 1,)

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

        maze_solver(map_number, start_pos, goal_pos, [start_pos], 0)
        # start_pos = (pos[0],pos[1])
        ## god help me
        # 4 check and then 4 more, make a variable that keeps track of newest number and make a check that if position of those newest numbers (i mean one of them, they will be in array that will...)
        # ...be removing positions of previous numbers uz they useless,

        # not sure what code below does, apparently its not usefull since it was commented out so i think you can remove it, im leaving it cuz mby there is something
        # valuable in there but im p sure you can just remove it no problem
        runner_pos = copy.deepcopy(start_pos)
        while maze_map1[runner_pos[1] + 1][runner_pos[0]] != 'F' or maze_map1[runner_pos[1] - 1][
            runner_pos[0]] != 'F' or maze_map1[runner_pos[1]][runner_pos[0] + 1] != 'F' or maze_map1[runner_pos[1]][
            runner_pos[0] - 1] != 'F':
            available_paths = 0
            move_to_right = 0  # like a bool 1 = yes 0 = no
            move_to_left = 0  # like a bool 1 = yes 0 = no
            move_to_up = 0  # like a bool 1 = yes 0 = no
            move_to_down = 0  # like a bool 1 = yes 0 = no
            if maze_map1[runner_pos[1] + 1][runner_pos[0]] != '■':
                if maze_map1[runner_pos[1] + 2][runner_pos[0]] != 'P':

                    move_to_down = 1
            elif maze_map1[runner_pos[1] - 1][runner_pos[0]] != '■':

                move_to_up = 1
            elif maze_map1[runner_pos[1]][runner_pos[0] + 1] != '■':

                move_to_right = 1
            elif maze_map1[runner_pos[1]][runner_pos[0] - 1] != '■':

                move_to_left = 1

    #print(a)

def do_wires(serial):
    print('DOING WIRES')


    '''screen[35, 110] = (0, 0, 255)   # wire 1
    screen[115, 110] = (0, 0, 255)  # wire 2
    screen[195, 110] = (0, 0, 255)  # wire 3
    screen[275, 110] = (0, 0, 255)  # wire 4
    screen[350, 110] = (0, 0, 255)  # wire 5
    screen[430, 110] = (0, 0, 255)  # wire 6'''
    print("wire 1",pyautogui.pixel(1050+110,460+35))
    print("wire 2",pyautogui.pixel(1050+110,460+115))
    print("wire 3",pyautogui.pixel(1050+110,460+195))
    print("wire 4",pyautogui.pixel(1050+110,460+275))
    print("wire 5",pyautogui.pixel(1050+110,460+350))
    print("wire 6",pyautogui.pixel(1050+110,460+430))
    print("color found #1:", closest_color(pyautogui.pixel(1050+110,460+35),cable_LUT))
    print("color found #2:", closest_color(pyautogui.pixel(1050+110,460+115),cable_LUT))
    print("color found #3:", closest_color(pyautogui.pixel(1050+110,460+195),cable_LUT))
    print("color found #4:", closest_color(pyautogui.pixel(1050+110,460+275),cable_LUT))
    print("color found #5:", closest_color(pyautogui.pixel(1050+110,460+350),cable_LUT))
    print("color found #6:", closest_color(pyautogui.pixel(1050+110,460+430),cable_LUT))

    wire_array = [] # this one is just wires lol
    # tuple ("wire color", number)
    if closest_color(pyautogui.pixel(1050+110,460+35),cable_LUT)!= None:
        tup = (closest_color(pyautogui.pixel(1050+110,460+35),cable_LUT),1)
        wire_array.append(tup)
    if closest_color(pyautogui.pixel(1050+110,460+115),cable_LUT) != None:
        tup = (closest_color(pyautogui.pixel(1050+110,460+115),cable_LUT),2)
        wire_array.append(tup)
    if closest_color(pyautogui.pixel(1050+110,460+195),cable_LUT) != None:
        tup = (closest_color(pyautogui.pixel(1050+110,460+195),cable_LUT),3)
        wire_array.append(tup)
    if closest_color(pyautogui.pixel(1050+110,460+275),cable_LUT) != None:
        tup = (closest_color(pyautogui.pixel(1050+110,460+275),cable_LUT),4)
        wire_array.append(tup)
    if closest_color(pyautogui.pixel(1050+110,460+350),cable_LUT) != None:
        tup = (closest_color(pyautogui.pixel(1050+110,460+350),cable_LUT),5)
        wire_array.append(tup)
    if closest_color(pyautogui.pixel(1050+110,460+430),cable_LUT) != None:
        tup = (closest_color(pyautogui.pixel(1050+110,460+430),cable_LUT),6)
        wire_array.append(tup)

    last_digit = int(serial[-1]) % 2 == 1
    #pyautogui.click((1050+110,460+35+80*wire_array[][1]))
    # case for 3 wires
    if len(wire_array) == 3:
        # Rule 1 If there are no red wires, cut second wire
        if not any(wire[0] == 'red' for wire in wire_array):
            pyautogui.click((1050 + 110, 460 + 35 + 80 * wire_array[1][1]-80))
            print(wire_array[1]," need to be cut")
            return
        # rule 2 if the last wire is white, cut last wire
        elif wire_array[-1][0]=="white":
            pyautogui.click((1050 + 110, 460 + 35 + 80 * wire_array[2][1]-80))
            print(wire_array[2], " need to be cut")
            return
        # rule 3 if there is more than one blue wire, cut last blue wire
        elif sum(1 for wire in wire_array if wire[0] == 'blue') > 1:
            for wire in reversed(wire_array):
                if wire[0] == "blue":
                    pyautogui.click((1050 + 110, 460 + 35 + 80 * wire_array[i][1]-80))
                    print(wire_array[i], " need to be cut")
                return


        # rule 4 otherwise, cut the last wire
        else:
            pyautogui.click((1050 + 110, 460 + 35 + 80 * wire_array[2][1]-80))
            print(wire_array[2], " need to be cut")
            return
    # case for 4 wires
    elif len(wire_array) == 4:
        red_count = sum(1 for wire in wire_array if wire[0] == 'red')
        yellow_count = sum(1 for wire in wire_array if wire[0] == 'yellow')
        blue_count = sum(1 for wire in wire_array if wire[0] == 'blue')

        # rule 1 moire than one red wire and last digit of serial is odd

        if red_count > 1 and last_digit:
            for wire in reversed(wire_array):
                if wire[0] == 'red':
                    pyautogui.click((1050 + 110, 460 + 35 + 80 * wire[1]-80))
                    print(wire," need to be cut")
                    return
        # rule 2 last wire is yellow and no red wires
        elif wire_array[-1][0] == 'yellow' and red_count == 0:
            pyautogui.click((1050 + 110, 460 + 35 + 80 * wire_array[0][1]-80))
            print(wire_array[0], " need to be cut")
            return
        # rule  3 exactly one blue wire
        elif blue_count == 1:
            pyautogui.click((1050 + 110, 460 + 35 + 80 * wire_array[0][1]-80))
            print(wire_array[0], " need to be cut")
            return
        #rule 4 more than one yellow
        elif yellow_count > 1:
            pyautogui.click((1050 + 110, 460 + 35 + 80 * wire_array[-1][1]-80))
            print(wire_array[-1], " need to be cut")
        # rule 5 otherwise cut second wire
        else:
            pyautogui.click((1050 + 110, 460 + 35 + 80 * wire_array[1][1]-80))
            print(wire_array[1], " need to be cut")
            return
    elif len(wire_array) == 5:
        red_count = sum(1 for wire in wire_array if wire[0] == 'red')
        yellow_count = sum(1 for wire in wire_array if wire[0] == 'yellow')
        black_count = sum(1 for wire in wire_array if wire[0] == 'black')

        # rule 1 last wire black and last digit or serial odd
        if wire_array[-1][0] == "black" and last_digit:
            pyautogui.click((1050 + 110, 460 + 35 + 80 * wire_array[3][1]-80))
            print(wire_array[3], " need to be cut")
            return
        # rule 2 one red wire and more than 1 yellow
        elif red_count == 1 and yellow_count > 1:
            pyautogui.click((1050 + 110, 460 + 35 + 80 * wire_array[0][1]-80))
            print(wire_array[0], " need to be cut")
            return
        # rule 3 no black wires
        elif black_count == 0:
            pyautogui.click((1050 + 110, 460 + 35 + 80 * wire_array[1][1]-80))
            print(wire_array[1], " need to be cut")
            return
        # rule 4 otherwise cut first
        else:
            pyautogui.click((1050 + 110, 460 + 35 + 80 * wire_array[0][1]-80))
            print(wire_array[0], " need to be cut")
            return
    elif len(wire_array) == 6:
        yellow_count = sum(1 for wire in wire_array if wire[0] == "yellow")
        white_count = sum(1 for wire in wire_array if wire[0] == "white")
        red_count = sum(1 for wire in wire_array if wire[0] == "red")

        # Rule 1: No yellow wires and last digit of serial number is odd
        if yellow_count == 0 and last_digit:
            pyautogui.click((1050 + 110, 460 + 35 + 80 * wire_array[2][1]-80))
            print(wire_array[2], "needs to be cut, rule 1")
            return

        # Rule 2: Exactly one yellow wire and more than one white wire
        elif yellow_count == 1 and white_count > 1:
            pyautogui.click((1050 + 110, 460 + 35 + 80 * wire_array[3][1]-80))
            print(wire_array[3], "needs to be cut")
            return

        # Rule 3: No red wires
        elif red_count == 0:
            pyautogui.click((1050 + 110, 460 + 35 + 80 * wire_array[-1][1]-80))
            print(wire_array[-1], "needs to be cut")
            return

        # Rule 4: Otherwise, cut the fourth wire
        else:
            pyautogui.click((1050 + 110, 460 + 35 + 80 * wire_array[3][1]-80))
            print(wire_array[3], "needs to be cut")
            return


    print(len(wire_array), "number of wires",wire_array)

    print(a)

password_LUT = [
                    'ABOUT', 'AFTER', 'AGAIN', 'BELOW', 'COULD',
                    'EVERY', 'FIRST', 'FOUND', 'GREAT', 'HOUSE',
                    'LARGE', 'LEARN', 'NEBER', 'OTHER', 'PLACE',
                    'PLANT', 'POINT', 'RIGHT', 'SMALL', 'SOUND',
                    'SPELL', 'STILL', 'STUDY', 'THEIR', 'THERE',
                    'THESE', 'THING', 'THINK', 'THREE', 'WATER',
                    'WHERE', 'WHICH', 'WORLD', 'WOULD', 'WRITE'
                   ]
def password_word(row1,row2,row3,row4,row5):
    print(row1, row2, row3, row4, row5)
    for o in range(6):
        for j in range(6):
            for k in range(6):
                for l in range(6):
                    for m in range(6):

                        # print(o, j, k, l, m)
                        # if len(row5) < 6: say_('error')
                        # print(row1[o], row2[j], row3[k], row4[l], row5[m])
                        # print(row5)
                        # print(row4)
                        word = row1[o] + row2[j] + row3[k] + row4[l] + row5[m]
                        #print(word)
                        if word in password_LUT:
                            #print(word)
                            return word
def do_password():
    print('DOING PASSWORD')
    # IT GOES LIKE:
    # 1 4 7
    # 2 5 8
    # 3 6 9.
    # this one checke for dark pixels and bases on the position of dark pixels, it returns letter
    row1 =[]
    row2 =[]
    row3 =[]
    row4 =[]
    row5 =[]
    letter_lut = \
        {
            '058' : "M",
            '4567' : "I",
            '05678' : "Y",
            '025810' : "X",
            '0510' : 'N',
            '345611' : 'W',
        }
    letter_lut2 = \
        {
            '0123457101216' : 'P',
            '01234571115' : 'P',
            '0123457101115' : 'P',
            '012347121516171819' : 'H',
            '012391415161718' : 'U',
            '01234571012' : "F",
            '015678910121517' : "F",
            "012345791012141618" : "B",
            '012345791011131517' : 'B',
            '01234914' : "L",
            '1235910141618' : 'C',
            '12359101214151718' : 'G',
            '05678910' : 'T',
            '05678101112131415' : 'T',
            '05101112131415': "T",
            '145791012141518' : 'S',
            '01234591014161718' : "D",
            '01234579101214' : "E",
            '012345781013' : 'E',
            '01234711131519' : "K",
            '01234571012131619' : "R",
            '23912131516' : "V",
            '123591014161718' : 'O',
            '391415161718' : 'J',
            '034579101114' : 'Z',
            '123457101216171819': 'A',
        }
    #big loop outside to check every letter
    for loop in range(6):


        for i in range(5):
            #print('NEW LETTER')
            letter_array = [] # new for each letter thats why inside this loop
            pixel_number = 0

            #second check
            print("second check")
            letter_array_2 = []  # new for each letter thats why inside this loop
            pixel_number_2 = 0

            if closest_color(pyautogui.pixel(1050 + 77 + i * 79 + 3 * 13, 460 + 218 + 5 * 13),
                             password_color_lut) != None:
                print('its a Q')
                if i == 0:
                    row1.append('Q')
                elif i == 1:
                    row2.append('Q')
                elif i == 2:
                    row3.append('Q')
                elif i == 3:
                    row4.append('Q')
                elif i == 4:
                    row5.append('Q')
                continue
            for x in range(4):
                for y in range(5):
                    # this one keeps track of which pixel is checked so its easier to tell which combination is what letter
                    #print(pyautogui.pixel(1050 + 77 + i * 79 + x * 13, 460 + 218 + y * 13), pixel_number_2)
                    if closest_color(pyautogui.pixel(1050 + 77 + i * 79 + x * 13, 460 + 218 + y * 13),
                                     password_color_lut) != None:
                        letter_array_2.append(pixel_number_2)
                        #print("appending", pixel_number_2)
                    pixel_number_2 += 1
            print(letter_array_2)
            temp_numb = ''
            for number in letter_array_2:
                temp_numb += str(number)
            '''rows = [row1,row2,row3,row4,row5]
            for i,temp_numb in enumerate():
                if temp_numb in letter_lut2:
                    print(temp_numb, letter_lut2[temp_numb], "numb")
                    if i < len(rows):
                        rows[i].append(letter_lut2[temp_numb])'''

            print("first checkl",temp_numb)
            if temp_numb in letter_lut2:
                print(temp_numb, letter_lut2[temp_numb], "numb")
                print("temp numb is in letter_lut2", temp_numb, letter_lut2[temp_numb], i)
                if i == 0:
                    print(row1, loop, letter_lut2[temp_numb])
                    row1.append(letter_lut2[temp_numb])
                elif i == 1:
                    print(row1, loop, letter_lut2[temp_numb])
                    row2.append(letter_lut2[temp_numb])
                elif i == 2:
                    print(row1, loop, letter_lut2[temp_numb])
                    row3.append(letter_lut2[temp_numb])
                elif i == 3:
                    print(row1, loop, letter_lut2[temp_numb])
                    row4.append(letter_lut2[temp_numb])
                elif i == 4:
                    print(row1, loop, letter_lut2[temp_numb])
                    row5.append(letter_lut2[temp_numb])
            for x in range(3):
                for y in range(4):
                     # this one keeps track of which pixel is checked so its easier to tell which combination is what letter
                    #print(pyautogui.pixel(1050+81+i*79 + x*13,460+226+ y * 13), pixel_number)
                    if closest_color(pyautogui.pixel(1050+81+i*79 + x*13,460+226+ y * 13),password_color_lut) != None:
                        letter_array.append(pixel_number)
                        #print("appending",pixel_number)
                    pixel_number += 1
            #print(letter_array)
            temp_numb = ''
            for number in letter_array:
                temp_numb += str(number)

            if temp_numb in letter_lut:
                print(temp_numb, letter_lut[temp_numb], "numb")
                print("temp numb is in letter_lut", temp_numb, letter_lut[temp_numb], i)
                if i == 0:
                    print(row1,loop,letter_lut[temp_numb])
                    if len(row1) < loop+1 :
                        row1.append(letter_lut[temp_numb])

                elif i == 1:
                    print(row1, loop, letter_lut[temp_numb])
                    if len(row2) < loop + 1 :
                        row2.append(letter_lut[temp_numb])
                elif i == 2:
                    print(row1, loop, letter_lut[temp_numb])
                    if len(row3) < loop + 1 :
                        row3.append(letter_lut[temp_numb])
                elif i == 3:
                    print(row1, loop, letter_lut[temp_numb])
                    if len(row4) < loop + 1 :
                        row4.append(letter_lut[temp_numb])
                elif i == 4:
                    print(row1, loop, letter_lut[temp_numb])
                    if len(row5) < loop + 1 :
                        row5.append(letter_lut[temp_numb])
        print(f'printing rows: \n row1: {row1} \n row2: {row2} \n row3: {row3} \n row4: {row4} \n row5: {row5}')
        for row  in range(5):
            pyautogui.PAUSE = 0.02
            pyautogui.click(1050+90+row*80,460+120)
        '''cv2.imshow('screen', screen)
        cv2.waitKey(0)'''
        time.sleep(0.7)
    word = password_word(row1,row2,row3,row4,row5)
    print("password is ", word)
    print('state of password module is ',row1[0] + row2[0] + row3[0] + row4[0] + row5[0])
    print(f'printing rows: \n row1: {row1} \n row2: {row2} \n row3: {row3} \n row4: {row4} \n row5: {row5}')
    rows = [row1, row2, row3, row4, row5]
    moves = []
    #a
    print(rows)
    for numb1 in range(0, 6):
        if row1[numb1] == word[0]:
            print("number to move up on row 1 ", numb1)
            moves.append(numb1)
    for numb2 in range(0, 6):
        if row2[numb2] == word[1]:
            print("number to move up on row 2 ", numb2)
            moves.append(numb2)
    for numb3 in range(0, 6):
        if row3[numb3] == word[2]:
            print("number to move up on row 3 ", numb3)
            moves.append(numb3)
    for numb4 in range(0, 6):
        if row4[numb4] == word[3]:
            print("number to move up on row 4 ", numb4)
            moves.append(numb4)
    for numb5 in range(0, 6):
        if row5[numb5] == word[4]:
            print("number to move up on row 5 ", numb5)
            moves.append(numb5)

    pyautogui.PAUSE = 0.1
    print("moves to do",moves)
    for huj in range(5):
        for j in range(moves[huj]):
            pyautogui.click(1050+90+huj*80,460+120)
    pyautogui.click(1050 + 90 + 2 * 80, 460 + 460)
    return

# can check for second and third leter in labels because __K is only for FRK and _A_ is only for CAR, but i think it is
# better to ccheck for 3rd pos only and then just check one pixel to determine if the second position is A or L if third one is R.
# i think doing it just like serial number is good, just use less pixels to save time



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
# serial_test = 'zz1ab1'
# parallel_test = False
# batteries_test = 3

def do_keypads():
    print('DOING KEYPADS')
    #120 274  | 684
    #116 813    687 812
    pyautogui.scroll(1)
    pyautogui.scroll(1)
    pyautogui.scroll(1)
    #keypads go (top right,top left, bottom right,bottom left )
    keypad_lut = \
        {
            (0,0,0) : "key",
            (225, 211, 190) : "bg",
            (230, 217, 193) : "bg",
            (228, 214, 191) : "bg",
            (223, 210, 190) : "bg",
            (229, 215, 194) : "bg",
        }

    # i think it should be named like row rather thankeypad, its confusing
    keypad1 = ['o', 'triangle', 'gamma', 'lightning', 'rocket', 'hello', 'c']
    keypad2 = ['monster', 'o', 'c', 'spring', 'star', 'hello', 'questionmark']
    keypad3 = ['copyright', 'bob', 'spring', 'octopus', 'line', 'gamma', 'star']
    keypad4 = ['six', 'paragraph', 'table', 'rocket','octopus', 'questionmark', 'face']
    keypad5 = ['trident', 'face', 'table', 'c', 'paragraph', 'three', 'star']
    keypad6 = ['six', 'monster', 'puzzle', 'something', 'trident', 'devil', 'omega']
    #                                      xxx     yyy
    #keypad width = 190, height 183
    keypad = ['','','','']
    for i in range(4):
        '''if (closest_color(pyautogui.pixel(1050+324,460+178),keypad_lut) == "key"
        and closest_color(pyautogui.pixel(1050+308,460+220),keypad_lut) == "key"
        and closest_color(pyautogui.pixel(1050+333,460+227),keypad_lut) == "key"):
            pass'''
        xx,yy,aa = 0,0,0
        if i == 1:
            xx = 1; aa = 2
        elif i == 2:
            xx = 1; yy = 1; aa=1
        elif i == 3:
            yy = 1; aa = 1
        #region

        #test push




        if (closest_color(pyautogui.pixel(780+0-aa*4+xx*571 + 127,115+yy*539 + 361),keypad_lut) == "key"
        and closest_color(pyautogui.pixel(780+0-aa*4+xx*571 + 218,115+yy*539 + 373),keypad_lut) == "key"
        and closest_color(pyautogui.pixel(780+0-aa*4+xx*571 + 171,115+yy*539 + 420),keypad_lut) == "key"
        and closest_color(pyautogui.pixel(780+0-aa*4+xx*571 + 223,115+yy*539 + 504),keypad_lut) == "key"
        and closest_color(pyautogui.pixel(780+0-aa*4+xx*571 + 254,115+yy*539 + 515),keypad_lut) == "key"):
            keypad[i] = "line"
        elif (closest_color(pyautogui.pixel(780+0-aa*4+xx*571 + 123,115+yy*539 + 418),keypad_lut) == "key"
        and   closest_color(pyautogui.pixel(780+0-aa*4+xx*571 + 116,115+yy*539 + 455),keypad_lut) == "key"
        and   closest_color(pyautogui.pixel(780+0-aa*4+xx*571 + 193,115+yy*539 + 451),keypad_lut) == "key"
        and   closest_color(pyautogui.pixel(780+0-aa*4+xx*571 + 271,115+yy*539 + 448),keypad_lut) == "key"
        and   closest_color(pyautogui.pixel(780+0-aa*4+xx*571 + 236,115+yy*539 + 525),keypad_lut) == "key"):
            keypad[i] = "spring"

        elif (closest_color(pyautogui.pixel(780+0-aa*4+xx*571 + 174,115+yy*539 + 319),keypad_lut) == "key"
        and   closest_color(pyautogui.pixel(780+0-aa*4+xx*571 + 226,115+yy*539 + 319),keypad_lut) == "key"
        and   closest_color(pyautogui.pixel(780+0-aa*4+xx*571 + 145,115+yy*539 + 382),keypad_lut) == "key"
        and   closest_color(pyautogui.pixel(780+0-aa*4+xx*571 + 148,115+yy*539 + 508),keypad_lut) == "key"
        and   closest_color(pyautogui.pixel(780+0-aa*4+xx*571 + 253,115+yy*539 + 503),keypad_lut) == "key"
        and   closest_color(pyautogui.pixel(780+0-aa*4+xx*571 + 255,115+yy*539 + 402),keypad_lut) == "key"
        and   closest_color(pyautogui.pixel(780+0-aa*4+xx*571 + 258,115+yy*539 + 580),keypad_lut) == "key"):
            keypad[i] = "devil"

        elif (closest_color(pyautogui.pixel(780+0-aa*4+xx*571 + 147,115+yy*539 + 530),keypad_lut) == "key"
        and   closest_color(pyautogui.pixel(780+0-aa*4+xx*571 + 126,115+yy*539 + 463),keypad_lut) == "key"
        and   closest_color(pyautogui.pixel(780+0-aa*4+xx*571 + 265,115+yy*539 + 441),keypad_lut) == "key"
        and   closest_color(pyautogui.pixel(780+0-aa*4+xx*571 + 228,115+yy*539 + 509),keypad_lut) == "key"
        and   closest_color(pyautogui.pixel(780+0-aa*4+xx*571 + 230,115+yy*539 + 376),keypad_lut) == "key"):
            keypad[i] = "puzzle"
        elif (closest_color(pyautogui.pixel(780+0-aa*4+xx*571 + 103,115+yy*539 + 372),keypad_lut) == "key"
        and   closest_color(pyautogui.pixel(780+0-aa*4+xx*571 + 201,115+yy*539 + 452),keypad_lut) == "key"
        and   closest_color(pyautogui.pixel(780+0-aa*4+xx*571 + 301,115+yy*539 + 546),keypad_lut) == "key"
        and   closest_color(pyautogui.pixel(780+0-aa*4+xx*571 + 185,115+yy*539 + 531),keypad_lut) == "key"
        and   closest_color(pyautogui.pixel(780+0-aa*4+xx*571 + 301,115+yy*539 + 375),keypad_lut) == "key"):
            keypad[i] = "octopus"
        elif (closest_color(pyautogui.pixel(780+0-aa*4+xx*571 + 172,115+yy*539 + 316),keypad_lut) == "key"
        and   closest_color(pyautogui.pixel(780+0-aa*4+xx*571 + 228,115+yy*539 + 316),keypad_lut) == "key"
        and   closest_color(pyautogui.pixel(780+0-aa*4+xx*571 + 261,115+yy*539 + 448),keypad_lut) == "key"
        and   closest_color(pyautogui.pixel(780+0-aa*4+xx*571 + 140,115+yy*539 + 526),keypad_lut) == "key"
        and   closest_color(pyautogui.pixel(780+0-aa*4+xx*571 + 203,115+yy*539 + 446),keypad_lut) == "key"):
            keypad[i] = "monster"
        elif (closest_color(pyautogui.pixel(780+0-aa*4+xx*571 + 226,115+yy*539 + 567),keypad_lut) == "key"
        and   closest_color(pyautogui.pixel(780+0-aa*4+xx*571 + 187,115+yy*539 + 392),keypad_lut) == "key"
        and   closest_color(pyautogui.pixel(780+0-aa*4+xx*571 + 238,115+yy*539 + 418),keypad_lut) == "key"
        and   closest_color(pyautogui.pixel(780+0-aa*4+xx*571 + 187,115+yy*539 + 451),keypad_lut) == "key"
        and   closest_color(pyautogui.pixel(780+0-aa*4+xx*571 + 157,115+yy*539 + 521),keypad_lut) == "key"):
            keypad[i] = "three"
        elif (closest_color(pyautogui.pixel(780+0-aa*4+xx*571 + 151,115+yy*539 + 470),keypad_lut) == "key"
        and   closest_color(pyautogui.pixel(780+0-aa*4+xx*571 + 252,115+yy*539 + 491),keypad_lut) == "key"
        and   closest_color(pyautogui.pixel(780+0-aa*4+xx*571 + 254,115+yy*539 + 373),keypad_lut) == "key"
        and   closest_color(pyautogui.pixel(780+0-aa*4+xx*571 + 142,115+yy*539 + 367),keypad_lut) == "key"
        and   closest_color(pyautogui.pixel(780+0-aa*4+xx*571 + 217,115+yy*539 + 423),keypad_lut) == "key"):
            keypad[i] = "hello"
        elif (closest_color(pyautogui.pixel(780+0-aa*4+xx*571 + 95 ,115+yy*539 + 352),keypad_lut) == "key"
        and   closest_color(pyautogui.pixel(780+0-aa*4+xx*571 + 94 ,115+yy*539 + 520),keypad_lut) == "key"
        and   closest_color(pyautogui.pixel(780+0-aa*4+xx*571 + 299,115+yy*539 + 518),keypad_lut) == "key"
        and   closest_color(pyautogui.pixel(780+0-aa*4+xx*571 + 284,115+yy*539 + 351),keypad_lut) == "key"
        and   closest_color(pyautogui.pixel(780+0-aa*4+xx*571 + 200,115+yy*539 + 434),keypad_lut) == "key"):
            keypad[i] = "rocket"
        elif (closest_color(pyautogui.pixel(780+0-aa*4+xx*571 + 197,115+yy*539 + 385),keypad_lut) == "key"
        and   closest_color(pyautogui.pixel(780+0-aa*4+xx*571 + 119,115+yy*539 + 420),keypad_lut) == "key"
        and   closest_color(pyautogui.pixel(780+0-aa*4+xx*571 + 196,115+yy*539 + 486),keypad_lut) == "key"
        and   closest_color(pyautogui.pixel(780+0-aa*4+xx*571 + 275,115+yy*539 + 412),keypad_lut) == "key"
        and   closest_color(pyautogui.pixel(780+0-aa*4+xx*571 + 197,115+yy*539 + 530),keypad_lut) == "key"):
            keypad[i] = "trident"
        elif (closest_color(pyautogui.pixel(780+0+xx*571 + 195,115+yy*539 + 364),keypad_lut) == "key"
        and   closest_color(pyautogui.pixel(780+0+xx*571 + 108,115+yy*539 + 425),keypad_lut) == "key"
        and   closest_color(pyautogui.pixel(780+0+xx*571 + 282,115+yy*539 + 425),keypad_lut) == "key"
        and   closest_color(pyautogui.pixel(780+0+xx*571 + 248,115+yy*539 + 526),keypad_lut) == "key"
        and   closest_color(pyautogui.pixel(780+0+xx*571 + 141,115+yy*539 + 525),keypad_lut) == "key"):
            keypad[i] = "star"

        elif (closest_color(pyautogui.pixel(780+0+xx*571 + 191,115+yy*539 + 381),keypad_lut) == "key"
        and   closest_color(pyautogui.pixel(780+0+xx*571 + 144,115+yy*539 + 436),keypad_lut) == "key"
        and   closest_color(pyautogui.pixel(780+0+xx*571 + 165,115+yy*539 + 489),keypad_lut) == "key"
        and   closest_color(pyautogui.pixel(780+0+xx*571 + 221,115+yy*539 + 483),keypad_lut) == "key"
        and   closest_color(pyautogui.pixel(780+0+xx*571 + 239,115+yy*539 + 436),keypad_lut) == "key"):
            keypad[i] = "star"
        elif (closest_color(pyautogui.pixel(780+0-aa*4+xx*571 + 167,115+yy*539 + 490),keypad_lut) == "key"
        and   closest_color(pyautogui.pixel(780+0-aa*4+xx*571 + 271,115+yy*539 + 502),keypad_lut) == "key"
        and   closest_color(pyautogui.pixel(780+0-aa*4+xx*571 + 112,115+yy*539 + 408),keypad_lut) == "key"
        and   closest_color(pyautogui.pixel(780+0-aa*4+xx*571 + 169,115+yy*539 + 371),keypad_lut) == "key"
        and   closest_color(pyautogui.pixel(780+0-aa*4+xx*571 + 224,115+yy*539 + 418),keypad_lut) == "key"):
            keypad[i] = "table"
        elif (closest_color(pyautogui.pixel(780+0-aa*4+xx*571 + 138,115+yy*539 + 424),keypad_lut) == "key"
        and   closest_color(pyautogui.pixel(780+0-aa*4+xx*571 + 257,115+yy*539 + 484),keypad_lut) == "key"
        and   closest_color(pyautogui.pixel(780+0-aa*4+xx*571 + 195,115+yy*539 + 526),keypad_lut) == "key"
        and   closest_color(pyautogui.pixel(780+0-aa*4+xx*571 + 251,115+yy*539 + 350),keypad_lut) == "key"
        and   closest_color(pyautogui.pixel(780+0-aa*4+xx*571 + 226,115+yy*539 + 400),keypad_lut) == "key"):
            keypad[i] = "six"
        elif (closest_color(pyautogui.pixel(780+0-aa*4+xx*571 + 193,115+yy*539 + 464),keypad_lut) == "key"
        and   closest_color(pyautogui.pixel(780+0-aa*4+xx*571 + 225,115+yy*539 + 399),keypad_lut) == "key"
        and   closest_color(pyautogui.pixel(780+0-aa*4+xx*571 + 193,115+yy*539 + 360),keypad_lut) == "key"
        and   closest_color(pyautogui.pixel(780+0-aa*4+xx*571 + 271,115+yy*539 + 490),keypad_lut) == "key"
        and   closest_color(pyautogui.pixel(780+0-aa*4+xx*571 + 132,115+yy*539 + 462),keypad_lut) == "key"):
            keypad[i] = "triangle"
        elif (closest_color(pyautogui.pixel(780+0-aa*4+xx*571 + 167,115+yy*539 + 442),keypad_lut) == "key"
        and   closest_color(pyautogui.pixel(780+0-aa*4+xx*571 + 177,115+yy*539 + 348),keypad_lut) == "key"
        and   closest_color(pyautogui.pixel(780+0-aa*4+xx*571 + 253,115+yy*539 + 455),keypad_lut) == "key"
        and   closest_color(pyautogui.pixel(780+0-aa*4+xx*571 + 122,115+yy*539 + 515),keypad_lut) == "key"
        and   closest_color(pyautogui.pixel(780+0-aa*4+xx*571 + 245,115+yy*539 + 387),keypad_lut) == "key"):
            keypad[i] = "c" # SEEMS TO WORK, ITS REVERSED C
        elif (closest_color(pyautogui.pixel(780+0-aa*4+xx*571 + 211,115+yy*539 + 441),keypad_lut) == "key"
        and   closest_color(pyautogui.pixel(780+0-aa*4+xx*571 + 124,115+yy*539 + 440),keypad_lut) == "key"
        and   closest_color(pyautogui.pixel(780+0-aa*4+xx*571 + 207,115+yy*539 + 348),keypad_lut) == "key"
        and   closest_color(pyautogui.pixel(780+0-aa*4+xx*571 + 205,115+yy*539 + 526),keypad_lut) == "key"
        and   closest_color(pyautogui.pixel(780+0-aa*4+xx*571 + 129,115+yy*539 + 383),keypad_lut) == "key"):
            keypad[i] = "c" # ?
        elif (closest_color(pyautogui.pixel(780+0-aa*4+xx*571 + 192,115+yy*539 + 414),keypad_lut) == "key"
        and   closest_color(pyautogui.pixel(780+0-aa*4+xx*571 + 193,115+yy*539 + 470),keypad_lut) == "key"
        and   closest_color(pyautogui.pixel(780+0-aa*4+xx*571 + 272,115+yy*539 + 425),keypad_lut) == "key"
        and   closest_color(pyautogui.pixel(780+0-aa*4+xx*571 + 129,115+yy*539 + 401),keypad_lut) == "key"
        and   closest_color(pyautogui.pixel(780+0-aa*4+xx*571 + 120,115+yy*539 + 477),keypad_lut) == "key"
        and   closest_color(pyautogui.pixel(780+0-aa*4+xx*571 + 240,115+yy*539 + 499),keypad_lut) == "key"):
            keypad[i] = "something"

        elif (closest_color(pyautogui.pixel(780+0-aa*4+xx*571 + 195,115+yy*539 + 571),keypad_lut) == "key"
        and   closest_color(pyautogui.pixel(780+0-aa*4+xx*571 + 116,115+yy*539 + 424),keypad_lut) == "key"
        and   closest_color(pyautogui.pixel(780+0-aa*4+xx*571 + 197,115+yy*539 + 336),keypad_lut) == "key"
        and   closest_color(pyautogui.pixel(780+0-aa*4+xx*571 + 271,115+yy*539 + 424),keypad_lut) == "key"):
            keypad[i] = "o"
        elif (closest_color(pyautogui.pixel(780+0-aa*4+xx*571 + 137,115+yy*539 + 377),keypad_lut) == "key"
        and   closest_color(pyautogui.pixel(780+0-aa*4+xx*571 + 144,115+yy*539 + 519),keypad_lut) == "key"
        and   closest_color(pyautogui.pixel(780+0-aa*4+xx*571 + 194,115+yy*539 + 428),keypad_lut) == "key"
        and   closest_color(pyautogui.pixel(780+0-aa*4+xx*571 + 194,115+yy*539 + 428),keypad_lut) == "key"
        and   closest_color(pyautogui.pixel(780+0-aa*4+xx*571 + 182,115+yy*539 + 388),keypad_lut) == "key"):
            keypad[i] = "gamma"
        elif (closest_color(pyautogui.pixel(780+0-aa*4+xx*571 + 216,115+yy*539 + 364),keypad_lut) == "key"
        and   closest_color(pyautogui.pixel(780+0-aa*4+xx*571 + 168,115+yy*539 + 484),keypad_lut) == "key"
        and   closest_color(pyautogui.pixel(780+0-aa*4+xx*571 + 240,115+yy*539 + 512),keypad_lut) == "key"
        and   closest_color(pyautogui.pixel(780+0-aa*4+xx*571 + 214,115+yy*539 + 433),keypad_lut) == "key"):
            keypad[i] = "questionmark"

        elif (closest_color(pyautogui.pixel(780+0-aa*4+xx*571 + 237,115+yy*539 + 351),keypad_lut) == "key"
        and   closest_color(pyautogui.pixel(780+0-aa*4+xx*571 + 200,115+yy*539 + 440),keypad_lut) == "key"
        and   closest_color(pyautogui.pixel(780+0-aa*4+xx*571 + 155,115+yy*539 + 405),keypad_lut) == "key"
        and   closest_color(pyautogui.pixel(780+0-aa*4+xx*571 + 184,115+yy*539 + 360),keypad_lut) == "key"
        and   closest_color(pyautogui.pixel(780+0-aa*4+xx*571 + 190,115+yy*539 + 396),keypad_lut) == "key"):
            keypad[i] = "paragraph"
        elif (closest_color(pyautogui.pixel(780+0-aa*4+xx*571 + 129,115+yy*539 + 532),keypad_lut) == "key"
        and   closest_color(pyautogui.pixel(780+0-aa*4+xx*571 + 245,115+yy*539 + 532),keypad_lut) == "key"
        and   closest_color(pyautogui.pixel(780+0-aa*4+xx*571 + 269,115+yy*539 + 431),keypad_lut) == "key"
        and   closest_color(pyautogui.pixel(780+0-aa*4+xx*571 + 113,115+yy*539 + 428),keypad_lut) == "key"
        and   closest_color(pyautogui.pixel(780+0-aa*4+xx*571 + 262,115+yy*539 + 470),keypad_lut) == "key"):
            keypad[i] = "omega"
        elif (closest_color(pyautogui.pixel(780+0-aa*4+xx*571 + 167,115+yy*539 + 400),keypad_lut) == "key"
        and   closest_color(pyautogui.pixel(780+0-aa*4+xx*571 + 200,115+yy*539 + 400),keypad_lut) == "key"
        and   closest_color(pyautogui.pixel(780+0-aa*4+xx*571 + 95 ,115+yy*539 + 447),keypad_lut) == "key"
        and   closest_color(pyautogui.pixel(780+0-aa*4+xx*571 + 288,115+yy*539 + 427),keypad_lut) == "key"
        and   closest_color(pyautogui.pixel(780+0-aa*4+xx*571 + 184,115+yy*539 + 533),keypad_lut) == "key"):
            keypad[i] = "face"
        elif (closest_color(pyautogui.pixel(780+0-aa*4+xx*571 + 149,115+yy*539 + 443),keypad_lut) == "key"
        and   closest_color(pyautogui.pixel(780+0-aa*4+xx*571 + 232,115+yy*539 + 403),keypad_lut) == "key"
        and   closest_color(pyautogui.pixel(780+0-aa*4+xx*571 + 231,115+yy*539 + 487),keypad_lut) == "key"
        and   closest_color(pyautogui.pixel(780+0-aa*4+xx*571 + 295,115+yy*539 + 444),keypad_lut) == "key"
        and   closest_color(pyautogui.pixel(780+0-aa*4+xx*571 + 100,115+yy*539 + 446),keypad_lut) == "key"):
            keypad[i] = "copyright"
        elif (closest_color(pyautogui.pixel(780+0-aa*4+xx*571 + 143,115+yy*539 + 355),keypad_lut) == "key"
        and   closest_color(pyautogui.pixel(780+0-aa*4+xx*571 + 149,115+yy*539 + 452),keypad_lut) == "key"
        and   closest_color(pyautogui.pixel(780+0-aa*4+xx*571 + 223,115+yy*539 + 514),keypad_lut) == "key"
        and   closest_color(pyautogui.pixel(780+0-aa*4+xx*571 + 241,115+yy*539 + 417),keypad_lut) == "key"
        and   closest_color(pyautogui.pixel(780+0-aa*4+xx*571 + 196,115+yy*539 + 433),keypad_lut) == "key"):
            keypad[i] = "lightning"
        else:
            keypad[i] = "bob"
        #endregion

        print(keypad)
        #color = screen[point_x, point_y]
    print(keypad)
    kp1 = 0
    kp2 = 0
    kp3 = 0
    kp4 = 0
    kp5 = 0
    kp6 = 0
    final_array =[]# this array will have everything you need to click, sorted
    k_array1 = []
    k_array2 = []
    k_array3 = []
    k_array4 = []
    k_array5 = []
    k_array6 = []
    for sign in keypad:
        print(sign)
        if sign in keypad1:
            k_array1.append(sign)
            kp1 += 1
            print('kp1 + 1', kp1)
        if sign in keypad2:
            k_array2.append(sign)
            kp2 += 1
            print('kp2 + 1', kp2)
        if sign in keypad3:
            k_array3.append(sign)
            kp3 += 1
            print('kp3 + 1', kp3)
        if sign in keypad4:
            k_array4.append(sign)
            kp4 += 1
            print('kp4 + 1', kp4)
        if sign in keypad5:
            k_array5.append(sign)
            kp5 += 1
            print('kp5 + 1', kp5)
        if sign in keypad6:
            k_array6.append(sign)
            kp6 += 1
            print('kp6 + 1', kp6)

    '''cv2.imshow('screen', screen)
    cv2.waitKey(0)'''
    if kp1 == 4:

        for keys in keypad1[:]:

            if keys not in k_array1:
                keypad1.remove(keys)

        print(keypad1, 'keypad1')
        final_array = [keypad1[0],keypad1[1],keypad1[2],keypad1[3]]
    elif kp2 == 4:

        for keys in keypad2[:]:
            print(f'current key {keys}')
            if keys not in k_array2:
                keypad2.remove(keys)


        final_array = [keypad2[0],keypad2[1],keypad2[2],keypad2[3]]
    elif kp3 == 4:

        for keys in keypad3[:]:
            print(f'current key {keys}')
            if keys not in k_array3:
                keypad3.remove(keys)


        final_array = [keypad3[0],keypad3[1],keypad3[2],keypad3[3]]
    elif kp4 == 4:

        for keys in keypad4[:]:
            print(f'current key {keys}')
            if keys not in k_array4:
                keypad4.remove(keys)


        final_array = [keypad4[0],keypad4[1],keypad4[2],keypad4[3]]
    elif kp5 == 4:

        for keys in keypad5[:]:  # Iterate over a copy of the list
            print(f'current key {keys}')
            if keys not in k_array5:
                keypad5.remove(keys)


        final_array = [keypad5[0],keypad5[1],keypad5[2],keypad5[3]]

    elif kp6 == 4:

        for keys in keypad6[:]:

            if keys not in k_array6:
                keypad6.remove(keys)


        final_array = [keypad6[0],keypad6[1],keypad6[2],keypad6[3]]
    print(keypad)
    print(final_array)

    for i,word in enumerate(final_array):
        new_pos = keypad.index(word)
        if new_pos == 0:
            pyautogui.click(970,560)
        elif new_pos == 1:
            pyautogui.click(1540,553)
        elif new_pos == 3:
            pyautogui.click(970,1133)
        elif new_pos == 2:
            pyautogui.click(1540,1133)
        print(new_pos)
    pyautogui.scroll(-1)
    pyautogui.scroll(-1)
    pyautogui.scroll(-1)


def do_sequence():
    print('DOING SEQUENCE')
    cable_lut =\
        {
            (255, 106, 40) : "red",
            (255, 53, 24) : "red",
            (61, 100, 204) : "blue",
            (103, 143, 199) : "blue",
            (2, 4, 2) : "black",
            (42, 47, 54) : "nothing",
            (120, 113, 96) : "nothing",
        }
    # 5 checks each hole tom check for wires
    #check one top hole
    coordinates = [
        (1050 + 155, 460 + 148),
        (1050 + 153, 460 + 154),
        (1050 + 149, 460 + 160),
        (1050 + 146, 460 + 166),
        (1050 + 143, 460 + 171)
    ]



    black_count = 0
    blue_count = 0
    red_count = 0
    #this one has to loop 4 times
    for j in range(4):
        print(f'reds {red_count} blue: {blue_count} black: {black_count}')


        print(f' stage: {j+1}')
        color1 = "nothing"
        for coord in coordinates:
            color = closest_color(pyautogui.pixel(*coord), cable_lut)
            if color != 'nothing':
                color1 = color
                print(f" number 1 has wire: {color1}")
                break
        # check two middle hole

        coordinates2 = [(1050 + 150, 460 + 224), (1050 + 150, 460 + 231), (1050 + 150, 460 + 239),
                        (1050 + 150, 460 + 247)]
        color2 = "nothing"
        for coord in coordinates2:
            color = closest_color(pyautogui.pixel(*coord), cable_lut)
            if color != 'nothing':
                color2 = color
                print(f" number 2 has wire: {color2}")

                break

            # check three, bottom hole

        coordinates3 = [(1050 + 142, 460 + 303), (1050 + 145, 460 + 309), (1050 + 148, 460 + 315),
                        (1050 + 151, 460 + 321)]
        color3 = "nothing"
        for coord in coordinates3:
            color = closest_color(pyautogui.pixel(*coord), cable_lut)
            if color != 'nothing':
                color3 = color
                print(f" number 3 has wire: {color3}")

                break
        print(color1,color2,color3)

        if color1 != 'nothing':
            print(f"checking color 1 which is {color1}")
            connection = ''
            #making 3 checks from place of first wire, this doesnt have to be done when wire isnt there, for obvious reasons
            check_1 = 0
            check_2 = 0
            check_3 = 0
            for i in range(10):
                if closest_color(pyautogui.pixel(1050+151+i*14, 460+150),cable_lut) == color1:
                    check_1 +=1
                #from 1 to B
                if closest_color(pyautogui.pixel(1050+151+i*14, 460+158+i*7),cable_lut) == color1:
                    check_2 +=1
                #from 1 to C
                if closest_color(pyautogui.pixel(1050+151+i*14, 460+158+i*14),cable_lut) == color1:
                    check_3 +=1
                #make 10 pixel checks, if 6 of them match the main color, that means the wire is connected here
            if color1 == "red":
                red_count += 1
            elif color1 == "blue":
                blue_count += 1
            elif color1 == "black":
                black_count += 1
            print(f'color 1 checks 1 2 3 {check_1}, {check_2}, {check_3}')
            check_values = [check_1, check_2, check_3]
            connections = ['A', 'B', 'C']

            max_value = max(check_values)
            max_index = check_values.index(max_value)

            connection = connections[max_index]

            if color1 == 'red':
                if red_count == 1 and connection == 'C':
                    # cut first wire, press it in the number field
                    pyautogui.click(1050 + 149,460+160)
                elif red_count == 2 and connection == 'B':
                    pyautogui.click(1050 + 149,460+160)
                elif red_count == 3 and connection == 'A':
                    pyautogui.click(1050 + 149,460+160)
                elif (red_count == 4 and connection == 'C') or (connection == 'A' and red_count == 4):
                    pyautogui.click(1050 + 149,460+160)
                elif red_count == 5 and connection == 'B':
                    pyautogui.click(1050 + 149,460+160)
                elif (red_count == 6 and connection == 'C') or (connection == 'A' and red_count == 6):
                    pyautogui.click(1050 + 149,460+160)
                elif red_count == 7:
                    pyautogui.click(1050 + 149,460+160)
                elif (red_count == 8 and connection == 'B') or (connection == 'A' and red_count == 8):
                    pyautogui.click(1050 + 149,460+160)
                elif (red_count == 9 and connection == 'B'):
                    pyautogui.click(1050 + 149,460+160)
            if color1 == 'blue':
                if blue_count == 1 and connection == 'B':
                    # cut first wire, press it in the number field
                    pyautogui.click(1050 + 149,460+160)
                elif (blue_count == 2 and connection == 'C') or (connection == 'A' and blue_count == 2):
                    pyautogui.click(1050 + 149,460+160)
                elif blue_count == 3 and connection == 'B':
                    pyautogui.click(1050 + 149,460+160)
                elif (blue_count == 4 and connection == 'A'):
                    pyautogui.click(1050 + 149,460+160)
                elif blue_count == 5 and connection == 'B':
                    pyautogui.click(1050 + 149,460+160)
                elif (blue_count == 6 and connection == 'C') or (connection == 'C' and blue_count == 6):
                    pyautogui.click(1050 + 149,460+160)
                elif blue_count == 7 and connection == 'C':
                    pyautogui.click(1050 + 149,460+160)
                elif (blue_count == 8 and connection == 'C') or (connection == 'A' and blue_count == 8):
                    pyautogui.click(1050 + 149,460+160)
                elif (blue_count == 9 and connection == 'A'):
                    pyautogui.click(1050 + 149,460+160)
            if color1 == 'black':
                if black_count == 1:
                    # cut first wire, press it in the number field
                    pyautogui.click(1050 + 149,460+160)
                elif (black_count == 2 and connection == 'C') or (connection == 'A' and black_count == 2):
                    pyautogui.click(1050 + 149,460+160)
                elif black_count == 3 and connection == 'B':
                    pyautogui.click(1050 + 149,460+160)
                elif (black_count == 4 and connection == 'C') or (connection == 'A' and black_count == 4):
                    pyautogui.click(1050 + 149,460+160)
                elif black_count == 5 and connection == 'B':
                    pyautogui.click(1050 + 149,460+160)
                elif (black_count == 6 and connection == 'C') or (connection == 'C' and black_count == 6):
                    pyautogui.click(1050 + 149,460+160)
                elif (black_count == 7 and connection == 'B') or (connection == 'A' and black_count == 7):
                    pyautogui.click(1050 + 149,460+160)
                elif (black_count == 8 and connection == 'C'):
                    pyautogui.click(1050 + 149,460+160)
                elif (black_count == 9 and connection == 'C'):
                    pyautogui.click(1050 + 149,460+160)
        if color2 != 'nothing':
            connection = ''
            check_1 = 0
            check_2 = 0
            check_3 = 0
            for i in range(10):
                '''screen[225-i*7, 144 + i * 14] = (255,255, 0)
                screen[230, 144 + i * 14] = (255, 255, 0)
                screen[241+i*7, 144 + i * 14] = (255,255, 0)'''
                if closest_color(pyautogui.pixel(1050 + 144 + i * 14, 460 + 225-i*7), cable_lut) == color2:
                    check_1 += 1
                # from 1 to B
                if closest_color(pyautogui.pixel(1050 + 144 + i * 14, 460 + 230), cable_lut) == color2:
                    check_2 += 1
                # from 1 to C
                if closest_color(pyautogui.pixel(1050 + 144 + i * 14, 460 + 241 + i * 7), cable_lut) == color2:
                    check_3 += 1
                # make 10 pixel checks, if 6 of them match the main color, that means the wire is connected here
            print(f'color 2 checks 1 2 3 {check_1}, {check_2}, {check_3}')
            check_values = [check_1, check_2, check_3]
            connections = ['A', 'B', 'C']

            max_value = max(check_values)
            max_index = check_values.index(max_value)

            connection = connections[max_index]
            if color2 == "red":
                red_count += 1
            elif color2 == "blue":
                blue_count += 1
            elif color2 == "black":
                black_count += 1
            if color2 == 'red':
                if red_count == 1 and connection == 'C':
                    # cut first wire, press it in the number field
                    pyautogui.click(1050 + 150,460+240)
                elif red_count == 2 and connection == 'B':
                    pyautogui.click(1050 + 150,460+240)
                elif red_count == 3 and connection == 'A':
                    pyautogui.click(1050 + 150,460+240)
                elif (red_count == 4 and connection == 'C') or (connection == 'A' and red_count == 4):
                    pyautogui.click(1050 + 150,460+240)
                elif red_count == 5 and connection == 'B':
                    pyautogui.click(1050 + 150,460+240)
                elif (red_count == 6 and connection == 'C') or (connection == 'A' and red_count == 6):
                    pyautogui.click(1050 + 150,460+240)
                elif red_count == 7:
                    pyautogui.click(1050 + 150,460+240)
                elif (red_count == 8 and connection == 'B') or (connection == 'A' and red_count == 8):
                    pyautogui.click(1050 + 150,460+240)
                elif (red_count == 9 and connection == 'B'):
                    pyautogui.click(1050 + 150,460+240)
            if color2 == 'blue':
                if blue_count == 1 and connection == 'B':
                    # cut first wire, press it in the number field
                    pyautogui.click(1050 + 150,460+240)
                elif (blue_count == 2 and connection == 'C') or (connection == 'A' and blue_count == 2):
                    pyautogui.click(1050 + 150,460+240)
                elif blue_count == 3 and connection == 'B':
                    pyautogui.click(1050 + 150,460+240)
                elif (blue_count == 4 and connection == 'A'):
                    pyautogui.click(1050 + 150,460+240)
                elif blue_count == 5 and connection == 'B':
                    pyautogui.click(1050 + 150,460+240)
                elif (blue_count == 6 and connection == 'C') or (connection == 'C' and blue_count == 6):
                    pyautogui.click(1050 + 150,460+240)
                elif blue_count == 7 and connection == 'C':
                    pyautogui.click(1050 + 150,460+240)
                elif (blue_count == 8 and connection == 'C') or (connection == 'A' and blue_count == 8):
                    pyautogui.click(1050 + 150,460+240)
                elif (blue_count == 9 and connection == 'A'):
                    pyautogui.click(1050 + 150,460+240)
            if color2 == 'black':
                if black_count == 1:
                    # cut first wire, press it in the number field
                    pyautogui.click(1050 + 150,460+240)
                elif (black_count == 2 and connection == 'C') or (connection == 'A' and black_count == 2):
                    pyautogui.click(1050 + 150,460+240)
                elif black_count == 3 and connection == 'B':
                    pyautogui.click(1050 + 150,460+240)
                elif (black_count == 4 and connection == 'C') or (connection == 'A' and black_count == 4):
                    pyautogui.click(1050 + 150,460+240)
                elif black_count == 5 and connection == 'B':
                    pyautogui.click(1050 + 150,460+240)
                elif (black_count == 6 and connection == 'C') or (connection == 'C' and black_count == 6):
                    pyautogui.click(1050 + 150,460+240)
                elif (black_count == 7 and connection == 'B') or (connection == 'A' and black_count == 7):
                    pyautogui.click(1050 + 150,460+240)
                elif (black_count == 8 and connection == 'C'):
                    pyautogui.click(1050 + 150,460+240)
                elif (black_count == 9 and connection == 'C'):
                    pyautogui.click(1050 + 150,460+240)
        if color3 != 'nothing':
            connection = ''
            check_1 = 0
            check_2 = 0
            check_3 = 0
            for i in range(10):
                '''screen[310-i*14, 147 + i * 14] = (0, 0, 255)
                screen[319-i*7, 147 + i * 14] = (0, 0, 255)
                screen[319, 147 + i * 14] = (0, 0, 255)'''
                if closest_color(pyautogui.pixel(1050 + 147 + i * 14, 460 + 310-i*14), cable_lut) == color3:
                    check_1 += 1
                # from 1 to B
                if closest_color(pyautogui.pixel(1050 + 147 + i * 14, 460 + 319-i*7), cable_lut) == color3:
                    check_2 += 1
                # from 1 to C
                if closest_color(pyautogui.pixel(1050 + 147 + i * 14, 460 + 319 ), cable_lut) == color3:
                    check_3 += 1
               # make 10 pixel checks, if 6 of them match the main color, that means the wire is connected here
            print(f'color 3 checks 1 2 3 {check_1}, {check_2}, {check_3}')

            check_values = [check_1, check_2, check_3]
            connections = ['A', 'B', 'C']

            max_value = max(check_values)
            max_index = check_values.index(max_value)

            connection = connections[max_index]
            if color3 == "red":
                red_count += 1
            elif color3 == "blue":
                blue_count += 1
            elif color3 == "black":
                black_count += 1
            if color3 == 'red':
                if red_count == 1 and connection == 'C':
                    # cut first wire, press it in the number field
                    pyautogui.click(1050 + 150,460+313)
                elif red_count == 2 and connection == 'B':
                    pyautogui.click(1050 + 150,460+313)
                elif red_count == 3 and connection == 'A':
                    pyautogui.click(1050 + 150,460+313)
                elif (red_count == 4 and connection == 'C') or (connection == 'A' and red_count == 4):
                    pyautogui.click(1050 + 150,460+313)
                elif red_count == 5 and connection == 'B':
                    pyautogui.click(1050 + 150,460+313)
                elif (red_count == 6 and connection == 'C') or (connection == 'A' and red_count == 6):
                    pyautogui.click(1050 + 150,460+313)
                elif red_count == 7:
                    pyautogui.click(1050 + 150,460+313)
                elif (red_count == 8 and connection == 'B') or (connection == 'A' and red_count == 8):
                    pyautogui.click(1050 + 150,460+313)
                elif (red_count == 9 and connection == 'B'):
                    pyautogui.click(1050 + 150,460+313)
            if color3 == 'blue':
                if blue_count == 1 and connection == 'B':
                    # cut first wire, press it in the number field
                    pyautogui.click(1050 + 150,460+313)
                elif (blue_count == 2 and connection == 'C') or (connection == 'A' and blue_count == 2):
                    pyautogui.click(1050 + 150,460+313)
                elif blue_count == 3 and connection == 'B':
                    pyautogui.click(1050 + 150,460+313)
                elif (blue_count == 4 and connection == 'A'):
                    pyautogui.click(1050 + 150,460+313)
                elif blue_count == 5 and connection == 'B':
                    pyautogui.click(1050 + 150,460+313)
                elif (blue_count == 6 and connection == 'C') or (connection == 'C' and blue_count == 6):
                    pyautogui.click(1050 + 150,460+313)
                elif blue_count == 7 and connection == 'C':
                    pyautogui.click(1050 + 150,460+313)
                elif (blue_count == 8 and connection == 'C') or (connection == 'A' and blue_count == 8):
                    pyautogui.click(1050 + 150,460+313)
                elif (blue_count == 9 and connection == 'A'):
                    pyautogui.click(1050 + 150,460+313)
            if color3 == 'black':
                if black_count == 1:
                    # cut first wire, press it in the number field
                    pyautogui.click(1050 + 150,460+313)
                elif (black_count == 2 and connection == 'C') or (connection == 'A' and black_count == 2):
                    pyautogui.click(1050 + 150,460+313)
                elif black_count == 3 and connection == 'B':
                    pyautogui.click(1050 + 150,460+313)
                elif (black_count == 4 and connection == 'C') or (connection == 'A' and black_count == 4):
                    pyautogui.click(1050 + 150,460+313)
                elif black_count == 5 and connection == 'B':
                    pyautogui.click(1050 + 150,460+313)
                elif (black_count == 6 and connection == 'C') or (connection == 'C' and black_count == 6):
                    pyautogui.click(1050 + 150,460+313)
                elif (black_count == 7 and connection == 'B') or (connection == 'A' and black_count == 7):
                    pyautogui.click(1050 + 150,460+313)
                elif (black_count == 8 and connection == 'C'):
                    pyautogui.click(1050 + 150,460+313)
                elif (black_count == 9 and connection == 'C'):
                    pyautogui.click(1050 + 150,460+313)

        pyautogui.click(1050 + 220, 460 + 446)

        if j < 3:
            time.sleep(3)


def do_first(start_flag):
    print('DOING WHOS ON FIRST')
    # this talb e is the one tha checks the mian screen
    screen_lut = \
        {
            (255,255,255) : "text",
            (0,0,50) : "no"
        }
    if start_flag:
        # this one scrolls 3 up only once cuz i plan to call this function 3 times total
        pyautogui.scroll(1)
        pyautogui.scroll(1)
        pyautogui.scroll(1)
        start_flag = False
    '''screen = pyautogui.screenshot(region=(780, 115, 1000, 1150))
    screen = np.array(screen)'''
    # YOU ARE
    '''screen[13,140] = (0,0,255)
    screen[13,200] = (0,0,255)
    screen[95,170] = (0,0,255)
    screen[50,295] = (0,0,255)
    screen[50,215] = (0,0,255)
    screen[95,595] = (0,0,255)
    screen[10,560] = (0,0,255)'''

    for i in range(3):
        display = 0 # changing how this one worst, instead its an int and it just goes buttonarray[display] and then just does notmal checkes
        #region
        if (closest_color(pyautogui.pixel(780+140,115+13),screen_lut) == 'text'
            and closest_color(pyautogui.pixel(780+200,115+13),screen_lut) == 'text'
            and closest_color(pyautogui.pixel(780+170,115+95),screen_lut) == 'text'
            and closest_color(pyautogui.pixel(780 + 295, 115 + 50), screen_lut) == 'text'
            and closest_color(pyautogui.pixel(780 + 215, 115 + 50), screen_lut) == 'text'
            and closest_color(pyautogui.pixel(780 + 595, 115 + 95), screen_lut) == 'text'
            and closest_color(pyautogui.pixel(780 + 560, 115 + 10), screen_lut) == 'text'
            and closest_color(pyautogui.pixel(780 + 450, 115 + 95), screen_lut) == 'text'
            and closest_color(pyautogui.pixel(780 + 670, 115 + 90), screen_lut) == 'text'
            and closest_color(pyautogui.pixel(780 + 632, 115 + 47), screen_lut) == 'text'
            and closest_color(pyautogui.pixel(780 + 390, 115 + 30), screen_lut) == 'text'
            and closest_color(pyautogui.pixel(780 + 480, 115 + 50), screen_lut) == 'no'):
            print(" word is YOU ARE")
            display = 5
        elif (closest_color(pyautogui.pixel(780 + 432, 115 + 93),screen_lut) == 'text'
            and closest_color(pyautogui.pixel(780 + 532, 115 + 93),screen_lut) == 'text'
            and closest_color(pyautogui.pixel(780 + 310, 115 + 95),screen_lut) == 'text'
            and closest_color(pyautogui.pixel(780 + 257, 115 + 95),screen_lut) == 'text'
            and closest_color(pyautogui.pixel(780 + 288, 115 + 60), screen_lut) == 'text'
            and closest_color(pyautogui.pixel(780 + 355, 115 + 10), screen_lut) == 'text'
            and closest_color(pyautogui.pixel(780 + 417, 115 + 40), screen_lut) == 'text'
            and closest_color(pyautogui.pixel(780 + 525, 115 + 10), screen_lut) == 'text'):
            print('word is REED')
            display = 2
        elif (
             closest_color(pyautogui.pixel(780 + 318, 115 + 44),screen_lut) == 'text'
            and closest_color(pyautogui.pixel(780 + 316, 115 + 35),screen_lut) == 'text'
            and closest_color(pyautogui.pixel(780 + 400, 115 + 88),screen_lut) == 'text'
            and closest_color(pyautogui.pixel(780 + 358, 115 + 11), screen_lut) == 'text'
            and closest_color(pyautogui.pixel(780 + 450, 115 + 34), screen_lut) == 'text'
            and closest_color(pyautogui.pixel(780 + 502, 115 + 77), screen_lut) == 'text'
            and closest_color(pyautogui.pixel(780 + 506, 115 + 21), screen_lut) == 'text'):
                print('word is YES') # i cuedk up check it later
                display = 1
        elif (closest_color(pyautogui.pixel(780 + 350, 115 + 16), screen_lut) == 'text'
              and closest_color(pyautogui.pixel(780 + 300, 115 + 30), screen_lut) == 'text'
              and closest_color(pyautogui.pixel(780 + 346, 115 + 63),screen_lut) == 'text'
              and closest_color(pyautogui.pixel(780 + 303, 115 + 93),screen_lut) == 'text'
              and closest_color(pyautogui.pixel(780 + 510, 115 + 95), screen_lut) == 'text'
              and closest_color(pyautogui.pixel(780 + 463, 115 + 15), screen_lut) == 'text'
              and closest_color(pyautogui.pixel(780 + 500, 115 + 50), screen_lut) == 'text'
              and closest_color(pyautogui.pixel(780 + 386, 115 + 92), screen_lut) == 'text'):
            print("word is SEE")
            display = 5
        elif (closest_color(pyautogui.pixel(780 + 457, 115 + 3), screen_lut) == 'text'
              and closest_color(pyautogui.pixel(780 + 467, 115 + 3), screen_lut) == 'text'
              and closest_color(pyautogui.pixel(780 + 462, 115 + 39),screen_lut) == 'text'):
            print("word is YOU'RE")
            display = 4
        elif (
              closest_color(pyautogui.pixel(780 + 389, 115 + 69), screen_lut) == 'text'
              and closest_color(pyautogui.pixel(780 + 415, 115 + 9),screen_lut) == 'text'
              and closest_color(pyautogui.pixel(780 + 365, 115 + 75),screen_lut) == 'text'
              and closest_color(pyautogui.pixel(780 + 440, 115 + 90), screen_lut) == 'text'
              and closest_color(pyautogui.pixel(780 + 500, 115 + 86), screen_lut) == 'text'
              and closest_color(pyautogui.pixel(780 + 553, 115 + 29), screen_lut) == 'text'
              and closest_color(pyautogui.pixel(780 + 266, 115 + 87), screen_lut) == 'text'):
            print("word is OKAY")
            display = 3
        elif (closest_color(pyautogui.pixel(780 + 262, 115 + 85), screen_lut) == 'text'
              and closest_color(pyautogui.pixel(780 + 320, 115 + 63),screen_lut) == 'text'
              and closest_color(pyautogui.pixel(780 + 430, 115 + 33),screen_lut) == 'text'
              and closest_color(pyautogui.pixel(780 + 490, 115 + 84), screen_lut) == 'text'
               and closest_color(pyautogui.pixel(780 + 544, 115 + 22), screen_lut) == 'text'
               and closest_color(pyautogui.pixel(780 + 462, 115 + 13), screen_lut) == 'text'
              and closest_color(pyautogui.pixel(780 + 373, 115 + 74), screen_lut) == 'text'):
            print("word is SAYS")
            display = 5
        elif (closest_color(pyautogui.pixel(780 + 120, 115 + 12), screen_lut) == 'text'
              and closest_color(pyautogui.pixel(780 + 120, 115 + 70),screen_lut) == 'text'
              and closest_color(pyautogui.pixel(780 + 170, 115 + 50),screen_lut) == 'text'
              and closest_color(pyautogui.pixel(780 + 444, 115 + 81), screen_lut) == 'text'
               and closest_color(pyautogui.pixel(780 + 217, 115 + 51), screen_lut) == 'text'
               and closest_color(pyautogui.pixel(780 + 442, 115 + 16), screen_lut) == 'text'
              and closest_color(pyautogui.pixel(780 + 642, 115 + 30), screen_lut) == 'text'):
            print("word is HOLD ON")
            display = 5
        elif (closest_color(pyautogui.pixel(780 + 206, 115 + 13), screen_lut) == 'text'
              and closest_color(pyautogui.pixel(780 + 235, 115 + 26),screen_lut) == 'text'
              and closest_color(pyautogui.pixel(780 + 500, 115 + 66),screen_lut) == 'text'
              and closest_color(pyautogui.pixel(780 + 522, 115 + 32), screen_lut) == 'text'
               and closest_color(pyautogui.pixel(780 + 588, 115 + 49), screen_lut) == 'text'
               and closest_color(pyautogui.pixel(780 + 292, 115 + 96), screen_lut) == 'text'
              and closest_color(pyautogui.pixel(780 + 390, 115 + 30), screen_lut) == 'text'):
            print("word is THERE")
            display = 5
        elif (closest_color(pyautogui.pixel(780 + 427, 115 + 66), screen_lut) == 'text'
              and closest_color(pyautogui.pixel(780 + 458, 115 + 84),screen_lut) == 'text'
              and closest_color(pyautogui.pixel(780 + 544, 115 + 83),screen_lut) == 'text'
              and closest_color(pyautogui.pixel(780 + 379, 115 + 12), screen_lut) == 'text'
               and closest_color(pyautogui.pixel(780 + 300, 115 + 96), screen_lut) == 'text'
               and closest_color(pyautogui.pixel(780 + 255, 115 + 96), screen_lut) == 'text'
              and closest_color(pyautogui.pixel(780 + 562, 115 + 38), screen_lut) == 'text'):
            print("word is READ")
            display = 4
        elif (closest_color(pyautogui.pixel(780 + 236, 115 + 7), screen_lut) == 'text'

              and closest_color(pyautogui.pixel(780 + 426, 115 + 69),screen_lut) == 'text'
              and closest_color(pyautogui.pixel(780 + 377, 115 + 77), screen_lut) == 'text'
               and closest_color(pyautogui.pixel(780 + 559, 115 + 63), screen_lut) == 'text'
               and closest_color(pyautogui.pixel(780 + 271, 115 + 64), screen_lut) == 'text'):
            print("word is YOUR")
            display = 4
        elif (closest_color(pyautogui.pixel(780 + 691, 115 + 91), screen_lut) == 'text'
              and closest_color(pyautogui.pixel(780 + 140, 115 + 32), screen_lut) == 'text'
              and closest_color(pyautogui.pixel(780 + 412, 115 + 46), screen_lut) == 'text'
              and closest_color(pyautogui.pixel(780 + 581, 115 + 73), screen_lut) == 'text'
              and closest_color(pyautogui.pixel(780 + 581, 115 + 73), screen_lut) == 'text'
              and closest_color(pyautogui.pixel(780 + 290, 115 + 35), screen_lut) == 'text'):
            print("word is NOTHING")
            display = 1
        elif (closest_color(pyautogui.pixel(780 + 111, 115 + 10), screen_lut) == 'text'
              ):
            print("word is THEY ARE")
            display = 1
        elif (closest_color(pyautogui.pixel(780 + 361, 115 + 17), screen_lut) == 'text'
              and closest_color(pyautogui.pixel(780 + 330, 115 + 90), screen_lut) == 'text'
              and closest_color(pyautogui.pixel(780 + 514, 115 + 90), screen_lut) == 'text'
              and closest_color(pyautogui.pixel(780 + 502, 115 + 47), screen_lut) == 'text'
              and closest_color(pyautogui.pixel(780 + 423, 115 + 46), screen_lut) == 'text'
              and closest_color(pyautogui.pixel(780 + 315, 115 + 13), screen_lut) == 'text'):
            print("word is CEE")
            display = 5
        elif (closest_color(pyautogui.pixel(780 + 350, 115 + 88), screen_lut) == 'text'
              and closest_color(pyautogui.pixel(780 + 300, 115 + 94), screen_lut) == 'text'
              and closest_color(pyautogui.pixel(780 + 306, 115 + 33), screen_lut) == 'text'
              and closest_color(pyautogui.pixel(780 + 405, 115 + 45), screen_lut) == 'text'
              and closest_color(pyautogui.pixel(780 + 503, 115 + 73), screen_lut) == 'text'
              and closest_color(pyautogui.pixel(780 + 497, 115 + 20), screen_lut) == 'text'):
            print("word is LED")
            display = 1
        elif (closest_color(pyautogui.pixel(780 + 457, 115 + 88), screen_lut) == 'text'
              and closest_color(pyautogui.pixel(780 + 535, 115 + 79), screen_lut) == 'text'
              and closest_color(pyautogui.pixel(780 + 535, 115 + 26), screen_lut) == 'text'
              and closest_color(pyautogui.pixel(780 + 456, 115 + 17), screen_lut) == 'text'
              and closest_color(pyautogui.pixel(780 + 350, 115 + 46), screen_lut) == 'text'
              and closest_color(pyautogui.pixel(780 + 275, 115 + 88), screen_lut) == 'text'):
            print("word is LEED")
            display = 2
        elif (closest_color(pyautogui.pixel(780 + 410, 115 + 87), screen_lut) == 'text'
              and closest_color(pyautogui.pixel(780 + 434, 115 + 85), screen_lut) == 'text'
              and closest_color(pyautogui.pixel(780 + 444, 115 + 39), screen_lut) == 'text'
              and closest_color(pyautogui.pixel(780 + 525, 115 + 14), screen_lut) == 'text'
              and closest_color(pyautogui.pixel(780 + 486, 115 + 20), screen_lut) == 'text'
              and closest_color(pyautogui.pixel(780 + 403, 115 + 15), screen_lut) == 'text'):
            print("word is FIRST")
            display = 3
        elif (closest_color(pyautogui.pixel(780 + 259, 115 + 84), screen_lut) == 'text'
              and closest_color(pyautogui.pixel(780 + 250, 115 + 55), screen_lut) == 'text'
              and closest_color(pyautogui.pixel(780 + 376, 115 + 73), screen_lut) == 'text'
              and closest_color(pyautogui.pixel(780 + 317, 115 + 88), screen_lut) == 'text'
              and closest_color(pyautogui.pixel(780 + 569, 115 + 61), screen_lut) == 'text'
              and closest_color(pyautogui.pixel(780 + 500, 115 + 75), screen_lut) == 'text'):
            print("word is BLANK")
            display = 4
        elif (closest_color(pyautogui.pixel(780 + 342, 115 + 97), screen_lut) == 'text'
              and closest_color(pyautogui.pixel(780 + 323, 115 + 62), screen_lut) == 'text'
              and closest_color(pyautogui.pixel(780 + 298, 115 + 93), screen_lut) == 'text'
              and closest_color(pyautogui.pixel(780 + 333, 115 + 21), screen_lut) == 'text'
              and closest_color(pyautogui.pixel(780 + 414, 115 + 47), screen_lut) == 'text'
              and closest_color(pyautogui.pixel(780 + 507, 115 + 75), screen_lut) == 'text'):
            print("word is RED")
            display = 4
        elif (closest_color(pyautogui.pixel(780 + 494, 115 + 3), screen_lut) == 'text'
              and closest_color(pyautogui.pixel(780 + 655, 115 + 90), screen_lut) == 'text'):
            print("word is THEY'RE")
            display = 2
        elif (closest_color(pyautogui.pixel(780 + 302, 115 + 95), screen_lut) == 'text'
              and closest_color(pyautogui.pixel(780 + 300, 115 + 38), screen_lut) == 'text'
              and closest_color(pyautogui.pixel(780 + 337, 115 + 17), screen_lut) == 'text'
              and closest_color(pyautogui.pixel(780 + 367, 115 + 82), screen_lut) == 'text'
              and closest_color(pyautogui.pixel(780 + 415, 115 + 129), screen_lut) == 'text'
              and closest_color(pyautogui.pixel(780 + 473, 115 + 82), screen_lut) == 'text'):
            print("word is YOU")
            display = 4
        elif (closest_color(pyautogui.pixel(780 + 335, 115 + 11), screen_lut) == 'text'
              and closest_color(pyautogui.pixel(780 + 343, 115 + 82), screen_lut) == 'text'
              and closest_color(pyautogui.pixel(780 + 383, 115 + 81), screen_lut) == 'text'
              and closest_color(pyautogui.pixel(780 + 434, 115 + 96), screen_lut) == 'text'
              and closest_color(pyautogui.pixel(780 + 487, 115 + 96), screen_lut) == 'text'
              and closest_color(pyautogui.pixel(780 + 478, 115 + 50), screen_lut) == 'text'):
            print("word is UR")
            display = 0
        elif (closest_color(pyautogui.pixel(780 + 263, 115 + 10), screen_lut) == 'text'
              and closest_color(pyautogui.pixel(780 + 268, 115 + 89), screen_lut) == 'text'
              and closest_color(pyautogui.pixel(780 + 413, 115 + 73), screen_lut) == 'text'
              and closest_color(pyautogui.pixel(780 + 534, 115 + 84), screen_lut) == 'text'
              and closest_color(pyautogui.pixel(780 + 541, 115 + 28), screen_lut) == 'text'
              and closest_color(pyautogui.pixel(780 + 350, 115 + 46), screen_lut) == 'text'):
            print("word is LEAD")
            display = 5
        elif (closest_color(pyautogui.pixel(780 + 494, 115 + 97), screen_lut) == 'text'
              and closest_color(pyautogui.pixel(780 + 580, 115 + 90), screen_lut) == 'text'
              and closest_color(pyautogui.pixel(780 + 567, 115 + 24), screen_lut) == 'text'
              and closest_color(pyautogui.pixel(780 + 362, 115 + 47), screen_lut) == 'text'
              and closest_color(pyautogui.pixel(780 + 262, 115 + 28), screen_lut) == 'text'
              and closest_color(pyautogui.pixel(780 + 426, 115 + 47), screen_lut) == 'text'):
            print("word is TREIR")
            display = 4
        elif (closest_color(pyautogui.pixel(780 + 220, 115 + 90), screen_lut) == 'text'
              and closest_color(pyautogui.pixel(780 + 352, 115 + 86), screen_lut) == 'text'
              and closest_color(pyautogui.pixel(780 + 424, 115 + 60), screen_lut) == 'text'
              and closest_color(pyautogui.pixel(780 + 506, 115 + 89), screen_lut) == 'text'
              and closest_color(pyautogui.pixel(780 + 543, 115 + 72), screen_lut) == 'text'
              and closest_color(pyautogui.pixel(780 + 627, 115 + 49), screen_lut) == 'text'):
            print("word is DISPLAY")
            display = 5
        elif (closest_color(pyautogui.pixel(780 + 317, 115 + 98), screen_lut) == 'text'
              and closest_color(pyautogui.pixel(780 + 332, 115 + 32), screen_lut) == 'text'
              and closest_color(pyautogui.pixel(780 + 372, 115 + 73), screen_lut) == 'text'
              and closest_color(pyautogui.pixel(780 + 376, 115 + 71), screen_lut) == 'text'
              and closest_color(pyautogui.pixel(780 + 355, 115 + 55), screen_lut) == 'text'
              and closest_color(pyautogui.pixel(780 + 428, 115 + 82), screen_lut) == 'text'):
            print("word is NO")
            display = 5
        elif (closest_color(pyautogui.pixel(780 + 415, 115 + 92), screen_lut) == 'text'
              and closest_color(pyautogui.pixel(780 + 385, 115 + 83), screen_lut) == 'text'
              and closest_color(pyautogui.pixel(780 + 429, 115 + 17), screen_lut) == 'text'):
            print("word is C")
            display = 3
        else:
            print("word is <nothing>")
            display = 2

        #endregion
        button_lut = \
            {
                (186, 165, 130) : "no",
                (47, 42, 33) : "text"
            }

        from math import floor
        button_array = [] # this one has all the buttons in set order, what you wanna do is have other
        # list that like: list when the wors is "display" which you should have lower in commented code for
        # old bot, then you just iterate through each thing in the list and when a word in list is in this array
        # you take the position this thing has in the array and based on that you make a button press, solving module
        for button in range(6):
            row = button // 3
            col = button % 3
            # this loops check 6 buttons, that will take some time too aaaaah
            print(col,row)
            '''screen[552+col*283,40+row*480] = (0,0,255)
        
            screen[505+col*283,106 + row * 480] = (0,0,255)
            screen[504+col*283,159 + row * 480] = (0,0,255)
            screen[448+col*283,243 + row * 480] = (0,0,255)
            screen[426+col*283,299 + row * 480] = (0,0,255)
            screen[416+col*283,175 + row * 480] = (0,0,255)
            screen[467 + col * 283,187 + row * 480] = (0,0,255)
            # green ready
            screen[505 + col * 283, 81 + row * 480] =  (255,0,0)
            screen[464 + col * 283, 113 + row * 480] =  (255,0,0)
            screen[466 + col * 283, 165 + row * 480] =  (255,0,0)
            screen[470 + col * 283, 256 + row * 480] =  (255,0,0)
            screen[498 + col * 283, 250 + row * 480] = (255,0,0)
            screen[462 + col * 283, 320 + row * 480] = (255,0,0)'''
            # print(pyautogui.pixel(780 + 106 + col * 480, 115 + 505 + row * 283))
            # print(pyautogui.pixel(780 + 159 + row * 480, 115 + 504 + col * 283))
            # print(pyautogui.pixel(780 + 243 + row * 480, 115 + 448 + col * 283))
            # print(pyautogui.pixel(780 + 299 + row * 480, 115 + 426 + col * 283))
            # print(pyautogui.pixel(780 + 175 + row * 480, 115 + 416 + col * 283))
            # print(pyautogui.pixel(780 + 187 + row * 480, 115 + 467 + col * 283))
            if         (closest_color(pyautogui.pixel(780 + 81  + row * 480, 115 + 505 + col * 283),button_lut) == "text"
                    and closest_color(pyautogui.pixel(780 + 111 + row * 480, 115 + 464 + col * 283),                 button_lut) == "text"
                    and closest_color(pyautogui.pixel(780 + 162 + row * 480, 115 + 462 + col * 283),                                  button_lut) == "text"
                    and closest_color(pyautogui.pixel(780 + 252 + row * 480, 115 + 470 + col * 283),                                  button_lut) == "text"
                    and closest_color(pyautogui.pixel(780 + 250 + row * 480, 115 + 498 + col * 283),                                  button_lut) == "text"
                    and closest_color(pyautogui.pixel(780 + 325 + row * 480, 115 + 462 + col * 283),                                  button_lut) == "text"):
                print("ready")
                button_array.append("ready")
            elif       (closest_color(pyautogui.pixel(780 + 103 + row * 480, 115 + 500 + col * 283), button_lut) == "text"
                    and closest_color(pyautogui.pixel(780 + 157 + row * 480, 115 + 500 + col * 283), button_lut) == "text"
                    and closest_color(pyautogui.pixel(780 + 243 + row * 480, 115 + 448 + col * 283), button_lut) == "text"
                    and closest_color(pyautogui.pixel(780 + 301 + row * 480, 115 + 426 + col * 283), button_lut) == "text"
                    and closest_color(pyautogui.pixel(780 + 175 + row * 480, 115 + 416 + col * 283), button_lut) == "text"
                    and closest_color(pyautogui.pixel(780 + 187 + row * 480, 115 + 467 + col * 283), button_lut) == "text"):
                print("first")
                button_array.append("first") #               xxx                    yyy
            elif       (closest_color(pyautogui.pixel(780 + 112 + row * 480, 115 + 498 + col * 283), button_lut) == "text"
                    and closest_color(pyautogui.pixel(780 + 139 + row * 480, 115 + 495 + col * 283), button_lut) == "text"
                    and closest_color(pyautogui.pixel(780 + 142 + row * 480, 115 + 440 + col * 283), button_lut) == "text"
                    and closest_color(pyautogui.pixel(780 + 111 + row * 480, 115 + 426 + col * 283), button_lut) == "text"
                    and closest_color(pyautogui.pixel(780 + 202 + row * 480, 115 + 457 + col * 283), button_lut) == "text"
                    and closest_color(pyautogui.pixel(780 + 169 + row * 480, 115 + 440 + col * 283), button_lut) == "text"
                    and closest_color(pyautogui.pixel(780 + 236 + row * 480, 115 + 449 + col * 283), button_lut) == "text"
                    and closest_color(pyautogui.pixel(780 + 259 + row * 480, 115 + 476 + col * 283), button_lut) == "text"
                    and closest_color(pyautogui.pixel(780 + 186 + row * 480, 115 + 418 + col * 283), button_lut) == "text"):
                print("done")
                button_array.append("done") #              xxx                    yyy

            elif       (closest_color(pyautogui.pixel(780 + 96  + row * 480, 115 + 500 + col * 283), button_lut) == "text"
                    and closest_color(pyautogui.pixel(780 + 152 + row * 480, 115 + 502 + col * 283), button_lut) == "text"
                    and closest_color(pyautogui.pixel(780 + 223 + row * 480, 115 + 478 + col * 283), button_lut) == "text"
                    and closest_color(pyautogui.pixel(780 + 280 + row * 480, 115 + 486 + col * 283), button_lut) == "text"
                    and closest_color(pyautogui.pixel(780 + 309 + row * 480, 115 + 485 + col * 283), button_lut) == "text"
                    and closest_color(pyautogui.pixel(780 + 208 + row * 480, 115 + 439 + col * 283), button_lut) == "text"):
                print("blank")
                button_array.append("blank") #              xxx                    yyy
            elif       (closest_color(pyautogui.pixel(780 + 127 + row * 480, 115 + 498 + col * 283), button_lut) == "text"
                    and closest_color(pyautogui.pixel(780 + 204 + row * 480, 115 + 499 + col * 283), button_lut) == "text"
                    and closest_color(pyautogui.pixel(780 + 173 + row * 480, 115 + 483 + col * 283), button_lut) == "text"
                    and closest_color(pyautogui.pixel(780 + 233 + row * 480, 115 + 457 + col * 283), button_lut) == "text"
                    and closest_color(pyautogui.pixel(780 + 247 + row * 480, 115 + 457 + col * 283), button_lut) == "text"
                    and closest_color(pyautogui.pixel(780 + 300 + row * 480, 115 + 458 + col * 283), button_lut) == "text"
                    and closest_color(pyautogui.pixel(780 + 188 + row * 480, 115 + 457 + col * 283),                                      button_lut) == "text"
                    and closest_color(pyautogui.pixel(780 + 146 + row * 480, 115 + 432 + col * 283),                                      button_lut) == "text"
                    and closest_color(pyautogui.pixel(780 + 112 + row * 480, 115 + 431 + col * 283),                                      button_lut) == "text"):
                print("uhhh")
                button_array.append("uhhh")  #              xxx                    yyy
            elif       (closest_color(pyautogui.pixel(780 + 167 + row * 480, 115 + 422 + col * 283), button_lut) == "text"
                    and closest_color(pyautogui.pixel(780 + 201 + row * 480, 115 + 422 + col * 283), button_lut) == "text"
                    and closest_color(pyautogui.pixel(780 + 184 + row * 480, 115 + 502 + col * 283), button_lut) == "text"
                    and closest_color(pyautogui.pixel(780 + 171 + row * 480, 115 + 500 + col * 283), button_lut) == "text"
                    and closest_color(pyautogui.pixel(780 + 198 + row * 480, 115 + 495 + col * 283), button_lut) == "text"
                    and closest_color(pyautogui.pixel(780 + 261 + row * 480, 115 + 503 + col * 283), button_lut) == "text"
                    and closest_color(pyautogui.pixel(780 + 228 + row * 480, 115 + 503 + col * 283), button_lut) == "text"
                    and closest_color(pyautogui.pixel(780 + 254 + row * 480, 115 + 463 + col * 283), button_lut) == "text"
                    and closest_color(pyautogui.pixel(780 + 230 + row * 480, 115 + 461 + col * 283), button_lut) == "text"
                    and closest_color(pyautogui.pixel(780 + 257 + row * 480, 115 + 424 + col * 283), button_lut) == "text"
                    and closest_color(pyautogui.pixel(780 + 132 + row * 480, 115 + 500 + col * 283), button_lut) == "text"
                    and closest_color(pyautogui.pixel(780 + 306 + row * 480, 115 + 492 + col * 283), button_lut) != "text"):
                print("sure")
                button_array.append("sure")  #              xxx                    yyy
            elif       (closest_color(pyautogui.pixel(780 + 167 + row * 480, 115 + 422 + col * 283), button_lut) == "text"
                    and closest_color(pyautogui.pixel(780 + 201 + row * 480, 115 + 422 + col * 283), button_lut) == "text"
                    and closest_color(pyautogui.pixel(780 + 184 + row * 480, 115 + 502 + col * 283), button_lut) == "text"
                    and closest_color(pyautogui.pixel(780 + 171 + row * 480, 115 + 500 + col * 283), button_lut) == "text"
                    and closest_color(pyautogui.pixel(780 + 198 + row * 480, 115 + 495 + col * 283), button_lut) == "text"
                    and closest_color(pyautogui.pixel(780 + 261 + row * 480, 115 + 503 + col * 283), button_lut) == "text"
                    and closest_color(pyautogui.pixel(780 + 228 + row * 480, 115 + 503 + col * 283), button_lut) == "text"
                    and closest_color(pyautogui.pixel(780 + 254 + row * 480, 115 + 463 + col * 283), button_lut) == "text"
                    and closest_color(pyautogui.pixel(780 + 230 + row * 480, 115 + 461 + col * 283), button_lut) == "text"
                    and closest_color(pyautogui.pixel(780 + 257 + row * 480, 115 + 424 + col * 283), button_lut) == "text"
                    and closest_color(pyautogui.pixel(780 + 306 + row * 480, 115 + 492 + col * 283), button_lut) != "text"):
                print("ur")
                button_array.append("ur")
            elif       (closest_color(pyautogui.pixel(780 + 99  + row * 480, 115 + 463 + col * 283), button_lut) == "text"
                    and closest_color(pyautogui.pixel(780 + 128 + row * 480, 115 + 474 + col * 283), button_lut) == "text"
                    and closest_color(pyautogui.pixel(780 + 112 + row * 480, 115 + 421 + col * 283), button_lut) == "text"
                    and closest_color(pyautogui.pixel(780 + 154 + row * 480, 115 + 474 + col * 283), button_lut) == "text"
                    and closest_color(pyautogui.pixel(780 + 200 + row * 480, 115 + 469 + col * 283), button_lut) == "text"
                    and closest_color(pyautogui.pixel(780 + 213 + row * 480, 115 + 469 + col * 283), button_lut) == "text"
                    and closest_color(pyautogui.pixel(780 + 213 + row * 480, 115 + 443 + col * 283), button_lut) == "text"
                    and closest_color(pyautogui.pixel(780 + 196 + row * 480, 115 + 422 + col * 283), button_lut) == "text"
                    and closest_color(pyautogui.pixel(780 + 254 + row * 480, 115 + 461 + col * 283), button_lut) == "text"):
                print("right")
                button_array.append("right") #              xxx                    yyy
            elif       (closest_color(pyautogui.pixel(780 + 121 + row * 480, 115 + 498 + col * 283), button_lut) == "text"
                    and closest_color(pyautogui.pixel(780 + 149 + row * 480, 115 + 499 + col * 283), button_lut) == "text"
                    and closest_color(pyautogui.pixel(780 + 121 + row * 480, 115 + 428 + col * 283), button_lut) == "text"
                    and closest_color(pyautogui.pixel(780 + 198 + row * 480, 115 + 416 + col * 283), button_lut) == "text"
                    and closest_color(pyautogui.pixel(780 + 172 + row * 480, 115 + 421 + col * 283), button_lut) == "text"
                    and closest_color(pyautogui.pixel(780 + 179 + row * 480, 115 + 458 + col * 283), button_lut) == "text"
                    and closest_color(pyautogui.pixel(780 + 232 + row * 480, 115 + 457 + col * 283), button_lut) == "text"
                    and closest_color(pyautogui.pixel(780 + 243 + row * 480, 115 + 416 + col * 283), button_lut) == "text"
                    and closest_color(pyautogui.pixel(780 + 284  + row * 480, 115 + 418 + col * 283), button_lut) == "text"):
                print("left")
                button_array.append("left")  #              xxx                    yyy
            elif       (closest_color(pyautogui.pixel(780 + 40  + row * 480, 115 + 503 + col * 283), button_lut) == "text"
                    and closest_color(pyautogui.pixel(780 + 43  + row * 480, 115 + 438 + col * 283), button_lut) == "text"
                    and closest_color(pyautogui.pixel(780 + 387 + row * 480, 115 + 469 + col * 283), button_lut) == "text"
                    and closest_color(pyautogui.pixel(780 + 387 + row * 480, 115 + 440 + col * 283), button_lut) == "text"
                    and closest_color(pyautogui.pixel(780 + 293 + row * 480, 115 + 504 + col * 283), button_lut) == "text"
                    and closest_color(pyautogui.pixel(780 + 380 + row * 480, 115 + 502 + col * 283), button_lut) == "text"):
                print("nothing")
                button_array.append("nothing")
                '''elif       (closest_color(pyautogui.pixel(780 + 128 + row * 480, 115 + 500 + col * 283), button_lut) == "text"
                    # and closest_color(pyautogui.pixel(780 + 180 + row * 480, 115 + 466 + col * 283), button_lut) == "text"
                    # and closest_color(pyautogui.pixel(780 + 200 + row * 480, 115 + 425 + col * 283), button_lut) == "text"
                    # and closest_color(pyautogui.pixel(780 + 237 + row * 480, 115 + 472 + col * 283), button_lut) == "text"
                    # and closest_color(pyautogui.pixel(780 + 302 + row * 480, 115 + 422 + col * 283), button_lut) == "text"
                    and closest_color(pyautogui.pixel(780 + 259 + row * 480, 115 + 466 + col * 283), button_lut) == "text"):
                print("okay")
                button_array.append("okay")'''  #              xxx                    yyy
            elif       (closest_color(pyautogui.pixel(780 + 81  + row * 480, 115 + 495 + col * 283), button_lut) == "text"
                    and closest_color(pyautogui.pixel(780 + 96  + row * 480, 115 + 458 + col * 283), button_lut) == "text"
                    and closest_color(pyautogui.pixel(780 + 109 + row * 480, 115 + 420 + col * 283), button_lut) == "text"
                    and closest_color(pyautogui.pixel(780 + 82  + row * 480, 115 + 418 + col * 283), button_lut) == "text"
                    and closest_color(pyautogui.pixel(780 + 170 + row * 480, 115 + 452 + col * 283), button_lut) == "text"
                    and closest_color(pyautogui.pixel(780 + 203 + row * 480, 115 + 458 + col * 283), button_lut) == "text"
                    and closest_color(pyautogui.pixel(780 + 269 + row * 480, 115 + 467 + col * 283), button_lut) == "text"
                    and closest_color(pyautogui.pixel(780 + 278 + row * 480, 115 + 436 + col * 283), button_lut) == "text"
                    and closest_color(pyautogui.pixel(780 + 306 + row * 480, 115 + 488 + col * 283), button_lut) == "text"):
                print("press")
                button_array.append("press")  #              xxx                    yyy
            elif       (closest_color(pyautogui.pixel(780 + 105 + row * 480, 115 + 435 + col * 283), button_lut) == "text"
                    and closest_color(pyautogui.pixel(780 + 111 + row * 480, 115 + 466 + col * 283), button_lut) == "text"
                    and closest_color(pyautogui.pixel(780 + 129 + row * 480, 115 + 448 + col * 283), button_lut) == "text"
                    and closest_color(pyautogui.pixel(780 + 142 + row * 480, 115 + 460 + col * 283), button_lut) == "text"
                    and closest_color(pyautogui.pixel(780 + 194 + row * 480, 115 + 458 + col * 283), button_lut) == "text"
                    and closest_color(pyautogui.pixel(780 + 214 + row * 480, 115 + 453 + col * 283), button_lut) == "text"
                    and closest_color(pyautogui.pixel(780 + 262 + row * 480, 115 + 472 + col * 283), button_lut) == "text"
                    and closest_color(pyautogui.pixel(780 + 265 + row * 480, 115 + 433 + col * 283), button_lut) == "text"
                    and closest_color(pyautogui.pixel(780 + 310 + row * 480, 115 + 419 + col * 283), button_lut) == "text"):
                print("what")
                button_array.append("what")  #              xxx                    yyy
            elif       (closest_color(pyautogui.pixel(780 + 112 + row * 480, 115 + 486 + col * 283), button_lut) == "text"
                    and closest_color(pyautogui.pixel(780 + 130 + row * 480, 115 + 501 + col * 283), button_lut) == "text"
                    and closest_color(pyautogui.pixel(780 + 122 + row * 480, 115 + 455 + col * 283), button_lut) == "text"
                    and closest_color(pyautogui.pixel(780 + 141 + row * 480, 115 + 425 + col * 283), button_lut) == "text"
                    and closest_color(pyautogui.pixel(780 + 171 + row * 480, 115 + 479 + col * 283), button_lut) == "text"
                    and closest_color(pyautogui.pixel(780 + 201 + row * 480, 115 + 498 + col * 283), button_lut) == "text"
                    and closest_color(pyautogui.pixel(780 + 257 + row * 480, 115 + 463 + col * 283), button_lut) == "text"
                    and closest_color(pyautogui.pixel(780 + 232 + row * 480, 115 + 474 + col * 283), button_lut) == "text"
                    and closest_color(pyautogui.pixel(780 + 310 + row * 480, 115 + 461 + col * 283), button_lut) == "text"):
                print("sure")
                button_array.append("sure")  #              xxx                    yyy
            elif       (closest_color(pyautogui.pixel(780 + 131 + row * 480, 115 + 500 + col * 283), button_lut) == "text"
                    and closest_color(pyautogui.pixel(780 + 130 + row * 480, 115 + 452 + col * 283), button_lut) == "text"
                    and closest_color(pyautogui.pixel(780 + 147 + row * 480, 115 + 423 + col * 283), button_lut) == "text"
                    and closest_color(pyautogui.pixel(780 + 113 + row * 480, 115 + 424 + col * 283), button_lut) == "text"
                    and closest_color(pyautogui.pixel(780 + 181 + row * 480, 115 + 421 + col * 283), button_lut) == "text"
                    and closest_color(pyautogui.pixel(780 + 250 + row * 480, 115 + 497 + col * 283), button_lut) == "text"
                    and closest_color(pyautogui.pixel(780 + 224 + row * 480, 115 + 460 + col * 283), button_lut) == "text"
                    and closest_color(pyautogui.pixel(780 + 310 + row * 480, 115 + 468 + col * 283), button_lut) == "text"
                    and closest_color(pyautogui.pixel(780 + 314 + row * 480, 115 + 429 + col * 283), button_lut) == "text"):
                print("your")
                button_array.append("your")  #              xxx                    yyy
            elif       (closest_color(pyautogui.pixel(780 + 120 + row * 480, 115 + 458 + col * 283), button_lut) == "text"
                    and closest_color(pyautogui.pixel(780 + 144 + row * 480, 115 + 429 + col * 283), button_lut) == "text"
                    and closest_color(pyautogui.pixel(780 + 144 + row * 480, 115 + 475 + col * 283), button_lut) == "text"
                    and closest_color(pyautogui.pixel(780 + 171 + row * 480, 115 + 476 + col * 283), button_lut) == "text"
                    and closest_color(pyautogui.pixel(780 + 205 + row * 480, 115 + 454 + col * 283), button_lut) == "text"
                    and closest_color(pyautogui.pixel(780 + 189 + row * 480, 115 + 416 + col * 283), button_lut) == "text"
                    and closest_color(pyautogui.pixel(780 + 231 + row * 480, 115 + 461 + col * 283), button_lut) == "text"
                    and closest_color(pyautogui.pixel(780 + 240 + row * 480, 115 + 498 + col * 283), button_lut) == "text"
                    and closest_color(pyautogui.pixel(780 + 306 + row * 480, 115 + 492 + col * 283), button_lut) == "text"):
                print("hold")
                button_array.append("hold")  #              xxx                    yyy
            elif       (closest_color(pyautogui.pixel(780 + 283 + row * 480, 115 + 422 + col * 283), button_lut) == "text"
                    and closest_color(pyautogui.pixel(780 + 235 + row * 480, 115 + 471 + col * 283), button_lut) == "text"
                    and closest_color(pyautogui.pixel(780 + 165 + row * 480, 115 + 457 + col * 283), button_lut) == "text"
                    # and closest_color(pyautogui.pixel(780 + 124 + row * 480, 115 + 454 + col * 283), button_lut) == "text"
                    # and closest_color(pyautogui.pixel(780 + 84  + row * 480, 115 + 436 + col * 283), button_lut) == "text"
                    # and closest_color(pyautogui.pixel(780 + 341 + row * 480, 115 + 417 + col * 283), button_lut) == "text"
                    # and closest_color(pyautogui.pixel(780 + 355 + row * 480, 115 + 437 + col * 283), button_lut) == "text"
                    # and closest_color(pyautogui.pixel(780 + 342 + row * 480, 115 + 461 + col * 283), button_lut) == "text"
                    and closest_color(pyautogui.pixel(780 + 337 + row * 480, 115 + 500 + col * 283), button_lut) == "text"):
                print("what?")
                button_array.append("what?")  #             xxx                    yyy
            elif       (closest_color(pyautogui.pixel(780 + 150 + row * 480, 115 + 464 + col * 283), button_lut) == "text"
                    and closest_color(pyautogui.pixel(780 + 128 + row * 480, 115 + 458 + col * 283), button_lut) == "text"
                    and closest_color(pyautogui.pixel(780 + 60  + row * 480, 115 + 460 + col * 283), button_lut) == "text"
                    and closest_color(pyautogui.pixel(780 + 91  + row * 480, 115 + 495 + col * 283), button_lut) == "text"
                    and closest_color(pyautogui.pixel(780 + 64  + row * 480, 115 + 494 + col * 283), button_lut) == "text"
                    and closest_color(pyautogui.pixel(780 + 215 + row * 480, 115 + 457 + col * 283), button_lut) == "text"
                    and closest_color(pyautogui.pixel(780 + 242 + row * 480, 115 + 460 + col * 283), button_lut) == "text"
                    and closest_color(pyautogui.pixel(780 + 363 + row * 480, 115 + 460 + col * 283), button_lut) == "text"
                    and closest_color(pyautogui.pixel(780 + 285 + row * 480, 115 + 500 + col * 283), button_lut) == "text"):
                print("uh huh")
                button_array.append("uh huh")  #             xxx                    yyy
            elif       (closest_color(pyautogui.pixel(780 + 110 + row * 480, 115 + 451 + col * 283), button_lut) == "text"
                    and closest_color(pyautogui.pixel(780 + 115 + row * 480, 115 + 451 + col * 283), button_lut) == "text"
                    and closest_color(pyautogui.pixel(780 + 120 + row * 480, 115 + 451 + col * 283), button_lut) == "text"
                    and closest_color(pyautogui.pixel(780 + 124 + row * 480, 115 + 476 + col * 283), button_lut) == "text"
                    and closest_color(pyautogui.pixel(780 + 177 + row * 480, 115 + 458 + col * 283), button_lut) == "text"
                    and closest_color(pyautogui.pixel(780 + 236 + row * 480, 115 + 472 + col * 283), button_lut) == "text"
                    and closest_color(pyautogui.pixel(780 + 241 + row * 480, 115 + 449 + col * 283), button_lut) == "text"
                    and closest_color(pyautogui.pixel(780 + 296 + row * 480, 115 + 419 + col * 283), button_lut) == "text"
                    and closest_color(pyautogui.pixel(780 + 303 + row * 480, 115 + 474 + col * 283), button_lut) == "text"):
                print("next")
                button_array.append("next")   #             xxx                    yyy
            elif       (closest_color(pyautogui.pixel(780 + 134 + row * 480, 115 + 500 + col * 283), button_lut) == "text"
                    and closest_color(pyautogui.pixel(780 + 181 + row * 480, 115 + 500 + col * 283), button_lut) == "text"
                    and closest_color(pyautogui.pixel(780 + 206 + row * 480, 115 + 457 + col * 283), button_lut) == "text"
                    and closest_color(pyautogui.pixel(780 + 219 + row * 480, 115 + 457 + col * 283), button_lut) == "text"
                    and closest_color(pyautogui.pixel(780 + 226 + row * 480, 115 + 439 + col * 283), button_lut) == "text"
                    and closest_color(pyautogui.pixel(780 + 238 + row * 480, 115 + 420 + col * 283), button_lut) == "text"
                    and closest_color(pyautogui.pixel(780 + 282 + row * 480, 115 + 458 + col * 283), button_lut) == "text"
                    and closest_color(pyautogui.pixel(780 + 270 + row * 480, 115 + 415 + col * 283), button_lut) == "text"
                    and closest_color(pyautogui.pixel(780 + 292 + row * 480, 115 + 501 + col * 283), button_lut) == "text"):
                print("like")
                button_array.append("like")   #             xxx                    yyy
                # you're not done!!
            elif       (closest_color(pyautogui.pixel(780 + 245 + row * 480, 115 + 418 + col * 283), button_lut) == "text"
                    and closest_color(pyautogui.pixel(780 + 74  + row * 480, 115 + 421 + col * 283), button_lut) == "text"
                    and closest_color(pyautogui.pixel(780 + 105 + row * 480, 115 + 421 + col * 283), button_lut) == "text"
                    and closest_color(pyautogui.pixel(780 + 91  + row * 480, 115 + 453 + col * 283), button_lut) == "text"
                    and closest_color(pyautogui.pixel(780 + 351 + row * 480, 115 + 415 + col * 283), button_lut) == "text"
                    and closest_color(pyautogui.pixel(780 + 270 + row * 480, 115 + 460 + col * 283), button_lut) == "text"
                    and closest_color(pyautogui.pixel(780 + 183 + row * 480, 115 + 446 + col * 283), button_lut) == "text"
                    and closest_color(pyautogui.pixel(780 + 150 + row * 480, 115 + 420 + col * 283), button_lut) == "text"
                    and closest_color(pyautogui.pixel(780 + 200 + row * 480, 115 + 501 + col * 283), button_lut) == "text"):
                print("you're")
                button_array.append("you're") #             xxx                    yyy
            elif       (closest_color(pyautogui.pixel(780 + 101 + row * 480, 115 + 500 + col * 283), button_lut) == "text"
                    and closest_color(pyautogui.pixel(780 + 122 + row * 480, 115 + 500 + col * 283), button_lut) == "text"
                    and closest_color(pyautogui.pixel(780 + 155 + row * 480, 115 + 499 + col * 283), button_lut) == "text"
                    and closest_color(pyautogui.pixel(780 + 187 + row * 480, 115 + 499 + col * 283), button_lut) == "text"
                    and closest_color(pyautogui.pixel(780 + 172 + row * 480, 115 + 458 + col * 283), button_lut) == "text"
                    and closest_color(pyautogui.pixel(780 + 261 + row * 480, 115 + 501 + col * 283), button_lut) == "text"
                    and closest_color(pyautogui.pixel(780 + 278 + row * 480, 115 + 473 + col * 283), button_lut) == "text"
                    and closest_color(pyautogui.pixel(780 + 244 + row * 480, 115 + 445 + col * 283), button_lut) == "text"
                    and closest_color(pyautogui.pixel(780 + 320 + row * 480, 115 + 458 + col * 283), button_lut) == "text"):
                print("uh uh")
                button_array.append("uh uh")  #             xxx                    yyy
            elif       (closest_color(pyautogui.pixel(780 + 160 + row * 480, 115 + 492 + col * 283), button_lut) == "text"
                    and closest_color(pyautogui.pixel(780 + 150 + row * 480, 115 + 442 + col * 283), button_lut) == "text"
                    and closest_color(pyautogui.pixel(780 + 171 + row * 480, 115 + 436 + col * 283), button_lut) == "text"
                    and closest_color(pyautogui.pixel(780 + 195 + row * 480, 115 + 464 + col * 283), button_lut) == "text"
                    and closest_color(pyautogui.pixel(780 + 211 + row * 480, 115 + 503 + col * 283), button_lut) == "text"
                    and closest_color(pyautogui.pixel(780 + 220 + row * 480, 115 + 422 + col * 283), button_lut) == "text"
                    and closest_color(pyautogui.pixel(780 + 229 + row * 480, 115 + 466 + col * 283), button_lut) == "text"
                    and closest_color(pyautogui.pixel(780 + 253 + row * 480, 115 + 456 + col * 283), button_lut) == "text"
                    and closest_color(pyautogui.pixel(780 + 211 + row * 480, 115 + 460 + col * 283), button_lut) != "text"
                    and closest_color(pyautogui.pixel(780 + 283 + row * 480, 115 + 498 + col * 283), button_lut) == "text"):
                print("you")
                button_array.append("you")  #               xxx                    yyy
            elif       (closest_color(pyautogui.pixel(780 + 40  + row * 480, 115 + 418 + col * 283), button_lut) == "text"
                    and closest_color(pyautogui.pixel(780 + 71  + row * 480, 115 + 420 + col * 283), button_lut) == "text"
                    and closest_color(pyautogui.pixel(780 + 57  + row * 480, 115 + 455 + col * 283), button_lut) == "text"
                    and closest_color(pyautogui.pixel(780 + 92  + row * 480, 115 + 456 + col * 283), button_lut) == "text"
                    and closest_color(pyautogui.pixel(780 + 385 + row * 480, 115 + 457 + col * 283), button_lut) == "text"
                    and closest_color(pyautogui.pixel(780 + 389 + row * 480, 115 + 500 + col * 283), button_lut) == "text"
                    and closest_color(pyautogui.pixel(780 + 371 + row * 480, 115 + 415 + col * 283), button_lut) == "text"
                    and closest_color(pyautogui.pixel(780 + 262 + row * 480, 115 + 469 + col * 283), button_lut) == "text"
                    and closest_color(pyautogui.pixel(780 + 166 + row * 480, 115 + 498 + col * 283), button_lut) == "text"):
                print("you are")
                button_array.append("you are")  #           xxx                    yyy
            elif       (closest_color(pyautogui.pixel(780 + 197 + row * 480, 115 + 438 + col * 283), button_lut) == "text"
                    and closest_color(pyautogui.pixel(780 + 213 + row * 480, 115 + 501 + col * 283), button_lut) == "text"
                    and closest_color(pyautogui.pixel(780 + 213 + row * 480, 115 + 453 + col * 283), button_lut) != "text"
                    and closest_color(pyautogui.pixel(780 + 252 + row * 480, 115 + 443 + col * 283), button_lut) != "text"
                    and closest_color(pyautogui.pixel(780 + 270 + row * 480, 115 + 455 + col * 283), button_lut) != "text"
                    and closest_color(pyautogui.pixel(780 + 145 + row * 480, 115 + 458 + col * 283), button_lut) != "text"
                    and closest_color(pyautogui.pixel(780 + 110 + row * 480, 115 + 455 + col * 283), button_lut) != "text"):
                print("u")
                button_array.append("u")  #                 xxx                    yyy
            elif       (closest_color(pyautogui.pixel(780 + 168 + row * 480, 115 + 500 + col * 283), button_lut) == "text"
                    and closest_color(pyautogui.pixel(780 + 204 + row * 480, 115 + 500 + col * 283), button_lut) == "text"
                    and closest_color(pyautogui.pixel(780 + 167 + row * 480, 115 + 424 + col * 283), button_lut) == "text"
                    and closest_color(pyautogui.pixel(780 + 202 + row * 480, 115 + 424 + col * 283), button_lut) == "text"
                    and closest_color(pyautogui.pixel(780 + 184 + row * 480, 115 + 454 + col * 283), button_lut) == "text"
                    and closest_color(pyautogui.pixel(780 + 230 + row * 480, 115 + 460 + col * 283), button_lut) == "text"
                    and closest_color(pyautogui.pixel(780 + 262 + row * 480, 115 + 460 + col * 283), button_lut) == "text"):
                print("no")
                button_array.append("no")  #                xxx                    yyy
            elif       (closest_color(pyautogui.pixel(780 + 140 + row * 480, 115 + 460 + col * 283), button_lut) == "text"
                    and closest_color(pyautogui.pixel(780 + 165 + row * 480, 115 + 455 + col * 283), button_lut) == "text"
                    and closest_color(pyautogui.pixel(780 + 147 + row * 480, 115 + 438 + col * 283), button_lut) == "text"
                    and closest_color(pyautogui.pixel(780 + 206 + row * 480, 115 + 476 + col * 283), button_lut) == "text"
                    and closest_color(pyautogui.pixel(780 + 205 + row * 480, 115 + 434 + col * 283), button_lut) == "text"
                    and closest_color(pyautogui.pixel(780 + 250 + row * 480, 115 + 470 + col * 283), button_lut) == "text"
                    and closest_color(pyautogui.pixel(780 + 285 + row * 480, 115 + 420 + col * 283), button_lut) == "text"):
                print("wait")
                button_array.append("wait")  #              xxx                    yyy
            elif       (closest_color(pyautogui.pixel(780 + 144 + row * 480, 115 + 426 + col * 283), button_lut) == "text"
                    and closest_color(pyautogui.pixel(780 + 159 + row * 480, 115 + 453 + col * 283), button_lut) == "text"
                    and closest_color(pyautogui.pixel(780 + 161 + row * 480, 115 + 490 + col * 283), button_lut) == "text"
                    and closest_color(pyautogui.pixel(780 + 206 + row * 480, 115 + 460 + col * 283), button_lut) == "text"
                    and closest_color(pyautogui.pixel(780 + 230 + row * 480, 115 + 420 + col * 283), button_lut) == "text"
                    and closest_color(pyautogui.pixel(780 + 250 + row * 480, 115 + 486 + col * 283), button_lut) == "text"
                    and closest_color(pyautogui.pixel(780 + 285 + row * 480, 115 + 440 + col * 283), button_lut) == "text"):
                print("yes")
                button_array.append("yes")  #               xxx                    yyy
            elif       (closest_color(pyautogui.pixel(780 + 80  + row * 480, 115 + 481 + col * 283), button_lut) == "text"
                    and closest_color(pyautogui.pixel(780 + 104 + row * 480, 115 + 478 + col * 283), button_lut) == "text"
                    and closest_color(pyautogui.pixel(780 + 136 + row * 480, 115 + 447 + col * 283), button_lut) == "text"
                    and closest_color(pyautogui.pixel(780 + 168 + row * 480, 115 + 500 + col * 283), button_lut) == "text"
                    and closest_color(pyautogui.pixel(780 + 183 + row * 480, 115 + 417 + col * 283), button_lut) == "text"
                    and closest_color(pyautogui.pixel(780 + 254 + row * 480, 115 + 457 + col * 283), button_lut) == "text"
                    and closest_color(pyautogui.pixel(780 + 354 + row * 480, 115 + 459 + col * 283), button_lut) == "text"):
                print("middle")
                button_array.append("middle")
            else: button_array.append("okay")#            xxx                    yyy
            # you're not done yet, i think im missing 1 more besides it
        what_to_press = [] # this array will have every word from the list, it will iterate through every single one
        # that is in there and then press it when its on the bomb
        print(display, button_array)
        display_b  = button_array[display]
        if display_b == "ready":
            what_to_press = ["yes", "okay", "what", "middle", "left", "press", "right", "blank", "ready", "no", "first","uhhh", "nothing", "wait"]
        elif display_b == "first":
            what_to_press = ["left", "okay", "yes", "middle", "no", "right", "nothing", "uhhh", "wait", "ready", "blank","what", "press", "first"]
        elif display_b == "no":
            what_to_press = ["blank", "uhhh", "wait", "first", "what", "ready", "right", "yes", "nothing", "left", "press","okay", "no", "middle"]
        elif display_b == "blank":
            what_to_press = ["wait", "right", "okay", "middle", "blank", "press", "ready", "nothing", "no", "what", "left", "uhhh","yes", "first"]
        elif display_b == "nothing":
            what_to_press = ["uhhh", "right", "okay", "middle", "yes", "blank", "no", "press", "left", "what", "wait","first", "nothing", "ready"]
        elif display_b == "yes":
            what_to_press = ["okay", "right", "uhhh", "middle", "first", "what", "press", "ready", "nothing", "yes", "left","blank", "no", "wait"]
        elif display_b == "what":
            what_to_press = ["uhhh", "what", "left", "nothing", "ready", "blank", "middle", "no", "okay", "first", "wait","yes", "press", "right"]
        elif display_b == "uhhh":
            what_to_press = ["ready", "nothing", "left", "what", "okay", "yes", "right", "no", "press", "blank", "uhhh","middle", "wait", "first"]
        elif display_b == "left":
            what_to_press = ["right", "left", "first", "no", "middle", "yes", "blank", "what", "uhhh", "wait", "press","ready", "okay", "nothing"]
        elif display_b == "right":
            what_to_press = ["yes", "nothing", "ready", "press", "no", "wait", "what", "right", "middle", "left", "uhhh","blank", "okay", "first"]
        elif display_b == "middle":
            what_to_press = ["blank", "ready", "okay", "what", "nothing", "press", "no", "wait", "left",  "middle","right", "first","uhhh", "yes"]
        elif display_b == "okay":
            what_to_press = ["middle", "no", "first", "yes", "uhhh", "nothing", "wait", "okay", "left", "ready", "blank","press", "what", "right"]
        elif display_b == "wait":
            what_to_press = ["uhhh", "no", "blank", "okay", "yes", "left", "first", "press", "what", "wait", "nothing","ready", "right", "middle"]
        elif display_b == "press":
            what_to_press = ["right", "middle", "yes", "ready", "press", "okay", "nothing", "uhhh", "blank", "left","first", "what", "no", "wait"]
        elif display_b == "you":
            what_to_press = ["sure", "you are", "your", "you're", "next", "uh huh", "ur", "hold", "what?", "you","uh uh", "like", "done", "u"]
        elif display_b == "you are":
            what_to_press = ["your", "next", "like", "uh huh", "what?", "done", "uh uh", "hold", "you","u", "you're", "sure","ur", "you are"]
        elif display_b == "your":
            what_to_press = ["uh uh", "you are", "uh huh", "your", "next", "ur", "sure", "u", "you're", "you","what?", "hold","like", "done"]
        elif display_b == "you're":
            what_to_press = ["you", "you're", "ur", "next", "uh uh", "you are", "u", "your", "what?", "uh huh", "sure","done", "like", "hold"]
        elif display_b == "ur":
            what_to_press = ["done", "u", "ur", "uh huh", "what?", "sure", "your", "hold", "you're", "like", "next", "uh uh","you are", "you"]
        elif display_b == "u":
            what_to_press = ["uh huh", "sure", "next", "what?", "you're", "ur", "uh uh", "done", "u", "you", "like", "hold","you are","your"]
        elif display_b == "uh huh":
            what_to_press = ["uh huh", "your", "you are", "you", "done", "hold", "uh uh", "next", "sure", "like", "you're","ur", "u", "what?"]
        elif display_b == "uh uh":
            what_to_press = ["ur", "u", "you are", "you're", "next", "uh uh", "done", "you", "uh huh", "like", "your","sure", "hold", "what?"]
        elif display_b == "what?":
            what_to_press = ["you", "hold", "you're", "your", "u", "done", "uh uh", "like", "you are", "uh huh", "ur","next", "what?", "sure"]
        elif display_b == "done":
            what_to_press = ["sure", "uh huh", "next", "what?", "your", "ur", "you're", "hold", "like", "you", "u","you are", "uh uh", "done"]
        elif display_b == "next":
            what_to_press = ["what?", "uh huh", "uh uh", "your", "hold", "sure", "next", "like", "done", "you are", "ur","you're", "u", "you"]
        elif display_b == "hold":
            what_to_press = ["you are", "u", "done", "uh uh", "you", "ur", "sure", "what?", "you're", "next", "hold","uh huh","your", "like"]
        elif display_b == "sure":
            what_to_press = ["you are", "done", "like", "you're", "you", "hold", "uh huh", "ur","sure",  "u", "what?","next","your","uh uh"]
        elif display_b == "like":
            what_to_press = ["you're", "next", "u", "ur", "hold", "done", "uh uh", "what?", "uh huh", "you", "like", "sure","you are", "your"]
        else:
            what_to_press = []  # Default if display doesn't match any case
            print()
        print("going into for loop")
        for button in what_to_press:
            print(button_array, button)
            if button in button_array:
                position = button_array.index(button)
                print("position")
                break
        if position == 0:
            pyautogui.click(990,577)
            pyautogui.moveTo(1,1)
        elif position == 1:
            pyautogui.click(990,840)
            pyautogui.moveTo(1,1)
        elif position == 2:
            pyautogui.click(990,1144)
            pyautogui.moveTo(1,1)
        elif position == 3:
            pyautogui.click(1473,577)
            pyautogui.moveTo(1,1)
        elif position == 4:
            pyautogui.click(1473,840)
            pyautogui.moveTo(1,1)
        elif position == 5:
            pyautogui.click(1473,1144)
            pyautogui.moveTo(1,1)

        '''cv2.imshow('screen', screen)
        cv2.waitKey(0)'''
        #temp,
        # if i < 2:
        time.sleep(3)
    pyautogui.scroll(-1)
    pyautogui.scroll(-1)
    pyautogui.scroll(-1)
def do_button(labels,batteries):
    print('DOING BUTTON')
    text_lut = \
        {
            (217, 171, 30) : "bg",
            (204, 44, 58) : "bg",
            (197, 154, 27) : "bg",
            (250, 233, 234) : 'text',
            (248, 232, 233) : 'text',
            (232, 236, 248) : "text",
            (247, 235, 219) : "bg",
            (41, 39, 37) : "text",
            (45, 43, 40) : "text",
            (38, 66, 170) : "bg",
            (187, 39, 51) : "bg",
        }
    but_col_lut = \
        {
            (217, 171, 30) : "yellow",
            (205, 45, 58) : 'red',
            (247, 235, 219) : "white",
            (42, 73, 189) : "blue"
        }
    stripe_lut = \
        {
            (29, 86, 188) : 'blue',
            (237, 200, 22) : 'yellow',
            (218, 46, 46) : "red",
            (247, 247, 247) : "white",
        }
    #time.sleep(1)


    print(pyautogui.pixel(1050+192, 460+325)," black")
    print(pyautogui.pixel(1050+115, 460+324)," red")
    print(pyautogui.pixel(1050+168, 460+205)," white")
    print(pyautogui.pixel(1050+470, 460+380)," green")


    # cv2.imshow('screen', screen)
    # cv2.waitKey(0)
    button = [] # [color,label]
    stripe = ''
    button.append(closest_color(pyautogui.pixel(1050+168, 460+205),but_col_lut))
    if closest_color(pyautogui.pixel(1050+192, 460+325),text_lut) == "text" and closest_color(pyautogui.pixel(1050+115, 460+324),text_lut) == "text":
        button.append("detonate")
    elif closest_color(pyautogui.pixel(1050+192, 460+325),text_lut) == "text" and closest_color(pyautogui.pixel(1050+115, 460+324),text_lut) == "bg":
        button.append("hold")
    elif closest_color(pyautogui.pixel(1050+192, 460+325),text_lut) == "bg" and closest_color(pyautogui.pixel(1050+115, 460+324),text_lut) == "text":
        button.append("press")
    elif closest_color(pyautogui.pixel(1050+192, 460+325),text_lut) == "bg" and closest_color(pyautogui.pixel(1050+115, 460+324),text_lut) == "bg":
        button.append("abort")
    module_done = False # checks if module is finished, if yes, exit the while loop
    print(button)
    stripe_press = False # this one will check for stripe after checks
    if "blue" in button and "abort" in button:
        stripe_press = True

    elif batteries > 1 and "detonate" in button:
        pyautogui.click(1050 + 168, 460 + 205)
        module_done = True
        # press and release immediately
    elif "white" in button and "CAR" in labels:
        stripe_press = True
    elif batteries > 2 and "FRK" in labels:
        pyautogui.click(1050 + 168, 460 + 205) # press and release immediately
        module_done= True
    elif "yellow" in button:
        stripe_press = True
    elif "red" in button and "hold" in button:
        pyautogui.click(1050 + 168, 460 + 205) # pess and release immedaitely
        module_done = True
    else:
        stripe_press = True

    if stripe_press:
        clock_lut = \
            {
                (0,0,0) : "off",
                (12, 10, 10) : "off",
                (7, 7, 6) : "off",
                (6, 5, 5) : "off",
                (0,255,255) : "on",
                (255,0,0) : "on",
            }
        number_lut = \
            {
                '1110111':'0',
                '0010010':'1',
                '1011101':'2',
                '1011011':'3',
                '0111010':'4',
                '1101011':'5',
                '1101111':'6',
                '1010010':'7',
                '1111111':'8',
                '1111011':'9'
            }
        pyautogui.mouseDown(1050+168, 460+205)
        time.sleep(0.7)
        stripe_col = closest_color(pyautogui.pixel(1050+470, 460+380),stripe_lut)
        print(stripe_col)
        while True:
            # the idea is to make it check miliseconds too but i think imrec is too slow, we willsee
            clock = pyautogui.screenshot(region=(2200, 95, 350, 130))
            clock = np.array(clock)
            clock = cv2.cvtColor(clock, cv2.COLOR_BGR2RGB)
            # cv2.imshow('clock', clock)
            # cv2.waitKey(0)
            numbers_array = []
            for i in range(4):
                number = ''
                a = 29 if i > 1 else 0
                # checking each number in clock
                # this moves check a little bit to right so dot wont fuck us over

                segment_coords = [
                    (14, 40 + 65 * i + a),  # up
                    (40, 20 + 65 * i + a),  # up left
                    (37, 58 + 65 * i + a),  # up right
                    (64, 40 + 65 * i + a),  # middle
                    (90, 20 + 65 * i + a),  # down left
                    (90, 58 + 65 * i + a),  # down right
                    (115, 40 + 65 * i + a)  # down
                ]

                for (y, x) in segment_coords:
                    pixel_color = pyautogui.pixel(2200 + x , 95 + y)
                    clock[ y, x ] = (0,0,255)
                    segment_state = '1' if closest_color(pixel_color, clock_lut) == "on" else '0'
                    number += segment_state
                print(number)
                # cv2.imshow("a",clock)
                # cv2.waitKey(0)
                if number in number_lut:
                    numbers_array.append(number_lut[number])
                else:
                    print(f"Unrecognized pattern at position {i}: {number}")
            # cv2.imshow('clock', clock)
            # cv2.waitKey(0)

            print(numbers_array)
            if closest_color(pyautogui.pixel(2350,120),clock_lut) == "on": # that means that we have minutes and seconds not seconds and mili
                if stripe_col == 'white' or stripe_col == 'red':
                    if '1' in numbers_array:
                        pyautogui.mouseUp()
                        module_done = True
                        break
                elif stripe_col == 'blue':
                    if '4' in numbers_array:
                        pyautogui.mouseUp()
                        module_done = True
                        break
                elif stripe_col == 'yellow':
                    if '5' in numbers_array:
                        pyautogui.mouseUp()
                        module_done = True
                        break
            else: # if it shows miliseconds
                for j in range(2):#only first 2 numbs
                    if stripe_col == 'white' or stripe_col == 'red':
                        if '1' in numbers_array[j]:
                            pyautogui.mouseUp()
                            module_done = True
                            break
                    elif stripe_col == 'blue':
                        if '4' in numbers_array[j]:
                            pyautogui.mouseUp()
                            module_done = True
                            break
                    elif stripe_col == 'yellow':
                        if '5' in numbers_array[j]:
                            pyautogui.mouseUp()
                            module_done = True
                            break
            if module_done:
                break
def do_simon(serial):
    #ANSWER IS GREEN YELLOW BLUE RED GREEN
    print('DOING SIMON SAYS')
    green_light_lut = \
        {
            (44, 42, 39) : "gray",
            (117, 172, 179) : "gray",
            (1, 170, 35) : "green"
        }


    print(pyautogui.pixel(1050+480,480))
    timer = 0
    serial_has_vowel = False
    vowels = ['a','e','i','o','u','A','E','I','O','U']
    for vowel in serial:
        print(vowel)
        if vowel in vowels:
            serial_has_vowel = True
            print("vowel in serial")
            break
    print(serial_has_vowel, "serial vowel, ", serial)
    color_lut = \
        {
            (22, 100, 5) : "green off",
            (48, 249, 188) : "green on",
            (106, 5, 10) : "red off",
            (251, 122, 48) : 'red on',
            (188, 70, 31) : 'red on',
            (0, 1, 126) : "blue off",
            (28, 189, 251) : 'blue on',
            (14, 96, 189) : "blue on",
            (123, 103, 0) : "yellow off",
            (218, 249, 99) : "yellow on",
        }
    press_array = [] # what to press
    is_flashing = False
    stage = 1
    eep = 0

    while True: # change true to check if there is green light

        print(f" co mowi debil green:  {closest_color(pyautogui.pixel(1050 + 260, 460 + 350), color_lut)}", " | time: ",  timer)
        print(f" co mowi debil yellow: {closest_color(pyautogui.pixel(1050 + 380, 460 + 240), color_lut)}", " | time: ",  timer)
        print(f" co mowi debil blue:   {closest_color(pyautogui.pixel(1050 + 250, 460 + 100), color_lut)}", " | time: ",    timer)
        print(f" co mowi debil red:    {closest_color(pyautogui.pixel(1050 + 160, 460 + 240), color_lut)}", " | time: ", timer)

        print('red ',pyautogui.pixel(1050+160,460+240))
        print('blue ',pyautogui.pixel(1050+250,460+100))
        print('yellow ',pyautogui.pixel(1050+380,460+240))
        print('green ',pyautogui.pixel(1050+260,460+350))
        timer += 1
        if stage < 6:
            #print(f'debug shit stage: {stage}, press_array: {press_array} is_flashing {is_flashing} eep = {eep}')
            if closest_color(pyautogui.pixel(1050 + 480, 480), green_light_lut) == "green":
                print(pyautogui.pixel(1050 + 480, 480))
                print("Green light detected. Exiting loop.")
                break
            #region
            # slows the check time after it notices a flash

            # this one counts colors to compare like on stage 3 should be 3 colors ofc
            # idea how to approach it
            # at first we are checking every 0.25 seconds for a flash, after that everything becomes normalized
            # since we already know what color to press, do it immediately and after that we wait set aomut of time for color to flash
            # however, first color remains the same, so what we can do is simply check when second color would be flashing
            # and since it would be normalized, we set the timer precisely and ur done with stage 2, other stages can be done in the same way
            # the only thing you need to also do check is light in the corner, can be checked after 3rd round to save time but idk really
            # if its gray, play until win, if its green, yippe you won.
            #endregion
            if not is_flashing:
                # nice push cutie >w<
                time.sleep(0.25)
                eep = 0.25
                # region
                if closest_color(pyautogui.pixel(1050+260,460+350),color_lut) == 'green on':
                    print("flashing green"," | time: ",timer)
                    #flashing_array.append("green")
                    if serial_has_vowel:
                        pyautogui.click(1050+380,460+240)
                        pyautogui.moveTo(1, 1)
                        press_array.append("yellow")
                        print('vowel, green flash'," | time: ",timer)
                    else:
                        pyautogui.click(1050+260,460+350)
                        pyautogui.moveTo(1, 1)
                        press_array.append("green")
                        print('NO vowel, green flash'," | time: ",timer)
                    is_flashing = True
                    stage += 1
                elif closest_color(pyautogui.pixel(1050+380,460+240),color_lut) == 'yellow on':
                    print("flashing yellow"," | time: ",timer)
                    if serial_has_vowel:
                        pyautogui.click(1050 + 260, 460 + 350)
                        pyautogui.moveTo(1, 1)
                        press_array.append("green")
                        print('vowel, yellow flash'," | time: ",timer)

                    else:
                        pyautogui.click(1050 + 160, 460 + 240)
                        pyautogui.moveTo(1, 1)
                        press_array.append("red")
                        print('NO vowel, yellow flash'," | time: ",timer)
                    #flashing_array.append("yellow")
                    is_flashing = True
                    stage += 1
                elif closest_color(pyautogui.pixel(1050+250,460+100),color_lut) == 'blue on':
                    print("flashing blue"," | time: ",timer)
                    if serial_has_vowel:
                        pyautogui.click(1050 + 160, 460 + 240)
                        pyautogui.moveTo(1, 1)
                        press_array.append("red")
                        print('vowel, blue flash'," | time: ",timer)
                    else:
                        pyautogui.click(1050 + 380, 460 + 240)
                        pyautogui.moveTo(1, 1)
                        press_array.append("yellow")
                        print('NO vowel, blue flash'," | time: ",timer)
                    #flashing_array.append("blue")
                    is_flashing = True
                    stage += 1
                elif closest_color(pyautogui.pixel(1050+160,460+240),color_lut) == 'red on':
                    print("flashing red"," | time: ",timer)
                    if serial_has_vowel:
                        pyautogui.click(1050+250,460+100)
                        pyautogui.moveTo(1, 1)
                        press_array.append("blue")
                        print('vowel, red flash'," | time: ",timer)
                    else:
                        pyautogui.click(1050+250,460+100)
                        pyautogui.moveTo(1, 1)
                        press_array.append("blue")
                        print('NO vowel, red flash'," | time: ",timer)
                    #flashing_array.append("red")
                    is_flashing = True
                    stage+=1
            print(f'entering isfashing if statement, array for stage {stage} is {press_array}')
            if is_flashing:

                #wait set amount of time to see exactly second flash
                if stage == 2:

                    eep = 2.7 #change from 2.6 to 2.7  (2.7 seems  ok )
                    print('stage 2 reached time to sleep for 2.6'," | time: ",timer)
                    time.sleep(eep)
                if stage == 3:
                    eep = 3 # 3.5 to 3.65 (3 seems ok.)

                    print('stage 3 reached time to sleep for 3.5'," | time: ",timer)
                    time.sleep(eep)
                if stage == 4:

                    eep = 3.6 # 4.4 to 4.5

                    print('stage 4 reached time to sleep for 4.4'," | time: ",timer )
                    time.sleep(eep)
                if stage == 5:
                    eep = 4.3 # unchanged

                    print("stage 5 reached, time to sleep for 5.3 "," | time: ",timer)
                    time.sleep(eep)
                screen = pyautogui.screenshot(region=(780, 115, 1000, 1150))
                screen = np.array(screen)
                screen[240, 160] = (0, 255, 255)  # red
                screen[100, 250] = (0, 255, 255)  # blue
                screen[240, 380] = (0, 255, 255)  # yellow
                screen[350, 260] = (0, 255, 255)  # green


                print(f" co mowi debil green:  {closest_color(pyautogui.pixel(1050 + 260, 460 + 350), color_lut)}"," | time: ",timer)
                print(f" co mowi debil yellow: {closest_color(pyautogui.pixel(1050 + 380, 460 + 240), color_lut)}"," | time: ",timer)
                print(f" co mowi debil blue:   {closest_color(pyautogui.pixel(1050 + 250, 460 + 100), color_lut)}"," | time: ",timer)
                print(f" co mowi debil red:    {closest_color(pyautogui.pixel(1050 + 160, 460 + 240), color_lut)}"," | time: ",timer)
                print(pyautogui.pixel(1050 + 260, 460 + 350), "green value "," time: ",timer)
                print(pyautogui.pixel(1050 + 380, 460 + 240), "yellow value"," time: ",timer)
                print(pyautogui.pixel(1050 + 250, 460 + 100), "blue value  "," time: ",timer)

                print(pyautogui.pixel(1050 + 160, 460 + 240), "red value   "," time: ",timer)
                # if stage > 4:
                #     cv2.imshow('screen', screen)
                #     cv2.waitKey(0)

                if closest_color(pyautogui.pixel(1050 + 260, 460 + 350), color_lut) == 'green on':
                    print("flashing green"," | time: ",timer)
                    # flashing_array.append("green")
                    if serial_has_vowel:
                        #pyautogui.click(1050 + 380, 460 + 240)
                        press_array.append("yellow")
                        print('vowel, greeb flash'," | time: ",timer)
                    else:
                        #pyautogui.click(1050 + 260, 460 + 350)
                        press_array.append("green")
                        print('NO vowel, greeb flash'," | time: ",timer)
                    is_flashing = True
                elif closest_color(pyautogui.pixel(1050 + 380, 460 + 240), color_lut) == 'yellow on':
                    print("flashing yellow"," | time: ",timer)
                    if serial_has_vowel:
                        #pyautogui.click(1050 + 260, 460 + 350)
                        press_array.append("green")
                        print('vowel, yellow flash'," | time: ",timer)
                    else:
                        #pyautogui.click(1050 + 160, 460 + 240)
                        press_array.append("red")
                        print('NO vowel, yellow flash'," | time: ",timer)
                    # flashing_array.append("yellow")
                    is_flashing = True
                elif closest_color(pyautogui.pixel(1050 + 250, 460 + 100), color_lut) == 'blue on':
                    print("flashing blue")
                    if serial_has_vowel:
                        #pyautogui.click(1050 + 160, 460 + 240)
                        press_array.append("red")
                        print('vowel, blue flash'," | time: ",timer)
                    else:
                        #pyautogui.click(1050 + 380, 460 + 240)
                        press_array.append("yellow")
                        print('NO vowel, blue flash'," | time: ",timer)
                    # flashing_array.append("blue")
                    is_flashing = True
                elif closest_color(pyautogui.pixel(1050 + 160, 460 + 240), color_lut) == 'red on':
                    print("flashing red"," | time: ",timer)
                    if serial_has_vowel:
                        #pyautogui.click(1050 + 250, 460 + 100)
                        press_array.append("blue")
                        print('vowel, red flash'," | time: ",timer)
                    else:
                        #pyautogui.click(1050 + 250, 460 + 100)
                        press_array.append("blue")
                        print('NO vowel, red flash'," | time: ",timer)
                else: print("xd?")
                    # flashing_array.append("red")
                print(press_array," should be: ['green', 'yellow', 'blue', 'red', 'green'] time: ",timer)

                for color in press_array:
                    if color == 'green':
                        pyautogui.click(1050 + 260, 460 + 350)
                        pyautogui.moveTo(1,1)
                    elif color == "blue":
                        pyautogui.click(1050 + 250, 460 + 100)
                        pyautogui.moveTo(1, 1)
                    elif color == "red":
                        pyautogui.click(1050 + 160, 460 + 240)
                        pyautogui.moveTo(1, 1)
                    elif color == "yellow":
                        pyautogui.click(1050 + 380, 460 + 240)
                        pyautogui.moveTo(1, 1)
                time.sleep(0.3) # so the color will have time to turn off, prob need to tune stage time sleeps -.3
                stage += 1


        else:
            print('something is off, time to break code sry')
            return

def do_complicated(serial,batteries,parallel):
    print('DOING COMPLICATED')
    #region
    led_lut = \
        {
            (252, 243, 190) : "lit",
            (1,1,1) : "off"
        }
    cable_lut =  \
        {
            (29, 59, 126) : "blue",
            (203, 0, 25) : "red",
            (255, 253, 235) : "white",
        }
    star_lut = \
        {
            (32, 26, 18) : "star",
            (125, 100, 71) : "no star"
        }
    last_digit_even = int(serial[-1]) % 2 == 0

    cable1 = []
    cable2 = []
    cable3 = []
    cable4 = []
    cable5 = []
    cable6 = []
    # cable format: (led,color_1,color_2,star)
    for led in range(6):
        # pixels that check for leds

        #print(pyautogui.pixel(1050+65+led*58,460+50))
        if led == 0:
            cable1.append(closest_color(pyautogui.pixel(1050+65+led*58,460+50),led_lut))
        elif led == 1:
            cable2.append(closest_color(pyautogui.pixel(1050 + 65 + led * 58, 460 + 50), led_lut))
        elif led == 2:
            cable3.append(closest_color(pyautogui.pixel(1050 + 65 + led * 58, 460 + 50), led_lut))
        elif led == 3:
            cable4.append(closest_color(pyautogui.pixel(1050 + 65 + led * 58, 460 + 50), led_lut))
        elif led == 4:
            cable5.append(closest_color(pyautogui.pixel(1050 + 65 + led * 58, 460 + 50), led_lut))
        elif led == 5:
            cable6.append(closest_color(pyautogui.pixel(1050 + 65 + led * 58, 460 + 50), led_lut))


    print(pyautogui.pixel(1050 + 65 + 0 * 58, 460 + 93))
    cable1.append(closest_color(pyautogui.pixel(1050 + 65 + 0 * 58, 460 + 93),cable_lut))
    print(pyautogui.pixel(1050 + 62 + 1 * 58, 460 + 90))
    cable2.append(closest_color(pyautogui.pixel(1050 + 62 + 1 * 58, 460 + 90),cable_lut))
    print(pyautogui.pixel(1050 + 59 + 2 * 58, 460 + 98))
    cable3.append(closest_color(pyautogui.pixel(1050 + 59 + 2 * 58, 460 + 98),cable_lut))
    print(pyautogui.pixel(1050 + 69 + 3 * 58, 460 + 93))
    cable4.append(closest_color(pyautogui.pixel(1050 + 69 + 3 * 58, 460 + 93),cable_lut))
    print(pyautogui.pixel(1050 + 67 + 4 * 58, 460 + 90))
    cable5.append(closest_color(pyautogui.pixel(1050 + 67 + 4 * 58, 460 + 90),cable_lut))
    print(pyautogui.pixel(1050 + 64 + 5 * 58, 460 + 95))
    cable6.append(closest_color(pyautogui.pixel(1050 + 64 + 5 * 58, 460 + 95),cable_lut))
    # another cable check
    print()

    print(pyautogui.pixel(1050 + 59 + 0 * 58, 460 + 93))
    cable1.append(closest_color(pyautogui.pixel(1050 + 59 + 0 * 58, 460 + 93), cable_lut))
    print(pyautogui.pixel(1050 + 67 + 1 * 58, 460 + 95))
    cable2.append(closest_color(pyautogui.pixel(1050 + 67 + 1 * 58, 460 + 95), cable_lut))
    print(pyautogui.pixel(1050 + 55 + 2 * 58, 460 + 93))
    cable3.append(closest_color(pyautogui.pixel(1050 + 55 + 2 * 58, 460 + 93), cable_lut))
    print(pyautogui.pixel(1050 + 80 + 3 * 58, 460 + 110))
    cable4.append(closest_color(pyautogui.pixel(1050 + 80 + 3 * 58, 460 + 110), cable_lut))
    print(pyautogui.pixel(1050 + 75 + 4 * 58, 460 + 100))
    cable5.append(closest_color(pyautogui.pixel(1050 + 75 + 4 * 58, 460 + 100), cable_lut))
    print(pyautogui.pixel(1050 + 64 + 5 * 58, 460 + 110))
    cable6.append(closest_color(pyautogui.pixel(1050 + 64 + 5 * 58, 460 + 110), cable_lut))
    # PYAUTOGUI.PIXEL IS NOT CHECKED, CHANGE IT LATER
    # ALL CABLES LOOK LIKE THEY WORK JSUT NEED TO SET UP PYAUTOGUI AND CHECKS
    # star check
    print()

    print(pyautogui.pixel(1050 + 70 + 0 * 70, 460 + 450))
    cable1.append(closest_color(pyautogui.pixel(1050 + 70 + 0 * 70, 460 + 450),star_lut))
    print(pyautogui.pixel(1050 + 72 + 1 * 70, 460 + 450))
    cable2.append(closest_color(pyautogui.pixel(1050 + 72 + 1 * 70, 460 + 450), star_lut))
    print(pyautogui.pixel(1050 + 75 + 2 * 70, 460 + 440))
    cable3.append(closest_color(pyautogui.pixel(1050 + 75 + 2 * 70, 460 + 440), star_lut))
    print(pyautogui.pixel(1050 + 80 + 3 * 70, 460 + 446))
    cable4.append(closest_color(pyautogui.pixel(1050 + 80 + 3 * 70, 460 + 446), star_lut))
    print(pyautogui.pixel(1050 + 85 + 4 * 70, 460 + 435))
    cable5.append(closest_color(pyautogui.pixel(1050 + 85 + 4 * 70, 460 + 435), star_lut))
    print(pyautogui.pixel(1050 + 92 + 5 * 70, 460 + 450))
    cable6.append(closest_color(pyautogui.pixel(1050 + 92 + 5 * 70, 460 + 450), star_lut))
    print(f"cable 1: {cable1} \n cable 2: {cable2} \n cable 3: {cable3} \n cable 4: {cable4} \n cable 5: {cable5} \n cable 6: {cable6}")
    #endregion
    cable_array = [cable1,cable2,cable3,cable4,cable5,cable6]
    print(last_digit_even,"last digit ven")
    loop = 0
    for cable in cable_array:
        # white
        to_cut = False
        if 'red' not in cable and 'blue' not in cable and 'lit' not in cable:
            print(cable,"cut")
            to_cut = True
        # upper one covers if star is in and it lit is in, it wont cut


        if 'red' not in cable and 'blue' not in cable and 'lit' in cable and "star" in cable and batteries > 1:
            print(cable,"cut")
            to_cut = True
        # red wire

        if "red" in cable and 'blue' not in cable and 'lit' not in cable and 'star' not in cable and last_digit_even:
            print(cable,"cut")
            to_cut = True
        if "red" in cable and 'blue' not in cable and 'lit' not in cable and 'star' in cable:
            print(cable,"cut")
            to_cut = True
        if "red" in cable and 'blue' not in cable and 'lit' in cable and 'star' not in cable and batteries > 1:
            print(cable,"cut")
            to_cut = True
        if "red" in cable and 'blue' not in cable and 'lit' in cable and 'star' in cable and batteries > 1:
            print(cable,"cut")
            to_cut = True
        # blue
        if "blue" in cable and "red" not in cable and "lit" not in cable and "star" not in cable and last_digit_even:
            print(cable,"cut")
            to_cut = True
        if 'blue' in cable and 'red' not in cable and 'lit' in cable and 'star' not in cable and parallel:
            print(cable,"cut")
            to_cut = True
        if 'blue' in cable and 'red' not in cable and 'lit' in cable and 'star' in cable and parallel:
            print(cable, "cut")
            to_cut = True
        # both
        if 'blue' in cable and 'red' in cable and 'lit' not in cable and 'star' not in cable and last_digit_even:
            print(cable,'cut')
            to_cut = True
        if 'blue' in cable and 'red' in cable and 'lit' not in cable and 'star'  in cable and parallel:
            print(cable, 'cut')
            to_cut = True
        if 'blue' in cable and 'red' in cable and 'lit'  in cable and 'star' not in cable and last_digit_even:
            print(cable, 'cut')
            to_cut = True
        if to_cut:
            pyautogui.click(1050 + 65 + loop * 58, 460 + 93)
            time.sleep(0.1)
        loop+=1


def click_position(index):
    x_coord = 1050 + 75 + index * 85
    y_coord = 460 + 385
    pyautogui.click(x_coord, y_coord)

def do_memory(previous_answers,stage,numbers):
    print('DOING MEMORY')
    # numbers are nubmers that were in prev stages, testing purpose only
    print(numbers , " numbers")
    print(stage, "stage")
    print(previous_answers, "previous")
    if stage != 1:
        time.sleep(3.5)
    memory_LUT = \
        {
            (50, 89, 72): "green",
            (255, 255, 255): "white",
        }
    memory_lut_bottom = \
        {
            (187, 167, 134) : "bg",
            (49, 44, 35) : "number"
        }

    #print(pyautogui.pixel(1050+200,460+155))
    #print(pyautogui.pixel(1050+235,460+155)) # red
    color_1 = closest_color(pyautogui.pixel(1050+200,460+155),memory_LUT)
    color_2 = closest_color(pyautogui.pixel(1050+235,460+155),memory_LUT) # red

    current_number = -1 # number that displays on the top
    if color_1 == "green" and color_2 == "white":
        current_number = 3
    if color_1 == "white" and color_2 =="green":
        current_number = 2
    if color_1 == "green" and color_2 =="green":
        current_number = 1
    if color_1 == "white" and color_2 =="white":
        current_number = 4
    print('number is ',current_number)
    numbers.append(current_number)
    bottom_numbers = []
    for i in range(4):
        #print(pyautogui.pixel(1050 + 75+i*85, 460 + 385))
        #print(pyautogui.pixel(1050 + 100+i*85, 460 + 385))

        color_3 =closest_color(pyautogui.pixel(1050 + 75+i*85, 460 + 385),memory_lut_bottom)
        color_4 = closest_color(pyautogui.pixel(1050 + 100+i*85, 460 + 385),memory_lut_bottom) # red
        if  color_3== "number" and color_4 == "bg":
            bottom_numbers.append(2)
        if  color_3== "bg" and color_4 == "bg":
            bottom_numbers.append(1)
        if  color_3== "bg" and color_4 == "number":
            bottom_numbers.append(3)
        if  color_3== "number" and color_4 == "number":
            bottom_numbers.append(4)
    print(bottom_numbers)

    previous_answers = previous_answers # append items like: (number, position)



    #we now have everything we need to solve the  module, it will take some place tho so this is like you know



    #stage 1
    if stage == 1:
        if current_number == 1:
            pos = 1  # Second position (1-based)
            click_position(pos)
            previous_answers.append((bottom_numbers[pos], pos))
        elif current_number == 2:
            pos = 1  # Second position (1-based)
            click_position(pos)
            previous_answers.append((bottom_numbers[pos], pos))
        elif current_number == 3:
            pos = 2  # Third position (1-based)
            click_position(pos)
            previous_answers.append((bottom_numbers[pos], pos))
        elif current_number == 4:
            pos = 3  # Fourth position (1-based)
            click_position(pos)
            previous_answers.append((bottom_numbers[pos], pos))
        do_memory(previous_answers,2,numbers)
    # Stage 2 Logic
    if stage == 2:
        if current_number == 1:
            # Press button labeled "4"
            for i, label in enumerate(bottom_numbers):
                if label == 4:
                    click_position(i)
                    previous_answers.append((label, i))
                    break
        elif current_number == 2:
            # Press button in the same position as in stage 1
            pos = previous_answers[0][1]
            click_position(pos)
            previous_answers.append((bottom_numbers[pos], pos))
        elif current_number == 3:
            pos = 0  # First position
            click_position(pos)
            previous_answers.append((bottom_numbers[pos], pos))
        elif current_number == 4:
            pos = previous_answers[0][1]
            click_position(pos)
            previous_answers.append((bottom_numbers[pos], pos))
        do_memory(previous_answers, 3, numbers)
    # Stage 3 Logic
    if stage == 3:
        if current_number == 1:
            # Press button with same label as in stage 2
            label_to_match = previous_answers[1][0]
            for i, label in enumerate(bottom_numbers):
                if label == label_to_match:
                    click_position(i)
                    previous_answers.append((label, i))
                    break
        elif current_number == 2:
            # Press button with same label as in stage 1
            label_to_match = previous_answers[0][0]
            for i, label in enumerate(bottom_numbers):
                if label == label_to_match:
                    click_position(i)
                    previous_answers.append((label, i))
                    break
        elif current_number == 3:
            pos = 2  # Third position
            click_position(pos)
            previous_answers.append((bottom_numbers[pos], pos))
        elif current_number == 4:
            # Press button labeled "4"
            for i, label in enumerate(bottom_numbers):
                if label == 4:
                    click_position(i)
                    previous_answers.append((label, i))
                    break
        do_memory(previous_answers, 4, numbers)
    # Stage 4 Logic
    if stage == 4:
        if current_number == 1:
            # Press button in the same position as in stage 1
            pos = previous_answers[0][1]
            click_position(pos)
            previous_answers.append((bottom_numbers[pos], pos))
        elif current_number == 2:
            pos = 0  # First position
            click_position(pos)
            previous_answers.append((bottom_numbers[pos], pos))
        elif current_number == 3:
            # Press button in the same position as in stage 2
            pos = previous_answers[1][1]
            click_position(pos)
            previous_answers.append((bottom_numbers[pos], pos))
        elif current_number == 4:
            # Press button in the same position as in stage 2
            pos = previous_answers[1][1]
            click_position(pos)
            previous_answers.append((bottom_numbers[pos], pos))
        do_memory(previous_answers, 5, numbers)
    # Stage 5 Logic
    if stage == 5:
        if current_number == 1:
            # Press button with the same label as in stage 1
            label_to_match = previous_answers[0][0]
            for i, label in enumerate(bottom_numbers):
                if label == label_to_match:
                    click_position(i)
                    previous_answers.append((label, i))
                    break
        elif current_number == 2:
            # Press button with the same label as in stage 2
            label_to_match = previous_answers[1][0]
            for i, label in enumerate(bottom_numbers):
                if label == label_to_match:
                    click_position(i)
                    previous_answers.append((label, i))
                    break
        elif current_number == 3:
            # Press button with the same label as in stage 4
            label_to_match = previous_answers[3][0]
            for i, label in enumerate(bottom_numbers):
                if label == label_to_match:
                    click_position(i)
                    previous_answers.append((label, i))
                    break
        elif current_number == 4:
            # Press button with the same label as in stage 3
            label_to_match = previous_answers[2][0]
            for i, label in enumerate(bottom_numbers):
                if label == label_to_match:
                    click_position(i)
                    previous_answers.append((label, i))
                    break
    '''cv2.imshow('screen', screen)
    cv2.waitKey(0)'''


labels = []

#IF PIXELS ARE OFF, ZOOM BY ONE
def check_pixel(x,y):
    a = pyautogui.pixel(x, y)
    print(a)
    return a
#do_simon('uuuaac')

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
    modules_LUT = [(33, 31, 28),(45, 41, 36),(35, 29, 25),(22, 22, 20),(141, 130, 114),(0, 1, 0),
                   (33, 30, 26),(45, 42, 36),(35, 31, 26),(21, 21, 20),
                   (33, 30, 28),(22, 21, 20),(31, 28, 26),(37, 33, 30),(21, 21, 19),
                   (31, 28, 25),(35, 30, 25),(35, 32, 28),(139, 128, 113),
                   (32, 30, 27),(140, 129, 113)
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
                #print(pyautogui.pixel(800+x*550+xx,yy+ 240+y*550))
                if pyautogui.pixel(800+x*550+xx,yy+ 240+y*550) in modules_LUT:

                    #print(f"we have module at ")
                    a = pyautogui.pixel(800+x*550+xx,yy+ 240+y*550)

                    tuple1 = ('str',x,y)
                    if front_side == 1:
                        module_array_front.append(tuple1)
                    else:
                        module_array_back.append(tuple1)
                else: print(f' not in table {pyautogui.pixel(800+x*550+xx,yy+ 240+y*550)}')
        if front_side == 1:
            pyautogui.dragTo(700,None,0.12,button="right")
            pyautogui.click(button='right')
            time.sleep(0.1)
            pyautogui.click(1200,1000,button='left')
            is_on_flipped = True
        time.sleep(1.5)

    print(module_array_back,"back \n", module_array_front, "front")
    # this one is what pixel color is what module

    type_of_module_LUT = \
        {
            (18, 24, 39) : "password",
            (18, 25, 40) : "password",
            (165, 150, 132) : 'sequence',
            (24, 70, 90) : "maze",
            (43, 49, 67) : "simon",
            (43, 48, 67) : "simon",
            (221, 208, 188) : "keypads",
            (92, 89, 84): "memory",
            (41, 109, 81) : 'password',
            (103, 115, 143) : 'wires',
            (103, 115, 144) : 'wires',
            (132, 137, 146) : "button",
        }
    type_of_module_LUT2 = \
    {
        (67, 66, 79) : "complicated",
        (67, 67, 79) : "complicated",
        (87, 91, 102) : "morse",
        (40, 36, 44) : "whos on first",
        (99, 110, 137): "wires",
        (99, 111, 137): "wires",
        (29, 41, 67) : 'password',
        (132, 137, 146) : 'button',
    }
    # if not in any then its button
    pixel_x,pixel_y=670,560 # those are the values to change for pixels checks, they wont be needed
    pixel_x2,pixel_y2=617,355 # those are the values to change for pixels checks, they wont be needed
    # later so dw changing as much as needed for testing purposes
    for module in module_array_back: # back because we are on the back
        #region
        # module is ("name",x,y)
        module_name = ''
        #print(module)
        pyautogui.click(650+module[1]*550,400+module[2]*550)
        #image to show what im clicking at more or less
        '''press_position = pyautogui.screenshot(region=(650+module[1]*550, 400+module[2]*550, 50, 50))
        press_position = np.array(press_position)
        press_position = cv2.cvtColor(press_position, cv2.COLOR_BGR2RGB)
        cv2.imshow("test",press_position)
        cv2.waitKey(0)'''
        print('doing the 0.7 time sleep')
        time.sleep(1.5) # used to be 0.7
        single_module_image = pyautogui.screenshot(region=(800, 240, 1300, 1200))
        single_module_image_np = np.array(single_module_image)
        single_module_image_with_pixels = cv2.cvtColor(single_module_image_np, cv2.COLOR_BGR2RGB)
        single_module_image_with_pixels[pixel_y,pixel_x] = (0, 0, 255)
        single_module_image_with_pixels[pixel_y2,pixel_x2] = (255, 0, 0)

        print(" " ,pyautogui.pixel(pixel_x2+800,240+pixel_y2)) # pixel check position
        first_px = closest_color(pyautogui.pixel(pixel_x2+800,240+pixel_y2),type_of_module_LUT)
        second_px = closest_color(pyautogui.pixel(pixel_x+800,240+pixel_y),type_of_module_LUT2)
        print(pyautogui.pixel(pixel_x + 800, 240 + pixel_y), ' red')  # red
        print(pyautogui.pixel(pixel_x2 + 800, 240 + pixel_y2), ' blue')  # blue
        if (first_px == 'wires' and second_px == 'complicated') or (first_px == 'memory' and second_px == 'complicated'):
            module_name = 'complicated'
        else:
            if first_px == second_px == 'button':
                module_name = 'button'
            else:
                if first_px != 'button':
                    module_name = first_px
                elif second_px != 'button':
                    module_name = second_px
        print(first_px,second_px,' first and second px' )
        print(module_name)
        '''if pyautogui.pixel(pixel_x2 + 800, 240 + pixel_y2) in type_of_module_LUT:
            module_name = type_of_module_LUT[pyautogui.pixel(pixel_x2 + 800, 240 + pixel_y2)]
            print(module_name, ' module')
        elif pyautogui.pixel(pixel_x + 800, 240 + pixel_y) in type_of_module_LUT2:
            module_name = type_of_module_LUT2[pyautogui.pixel(pixel_x + 800, 240 + pixel_y)]
            print(module_name, ' module')
        else:
            print(pyautogui.pixel(pixel_x + 800, 240 + pixel_y), 'not in lut') # red
            print(pyautogui.pixel(pixel_x2+800,240+pixel_y2), 'not in lut') # blue
            module_name = 'button'
            print("its a button")'''
            #do_button(labels,batteries)
        '''cv2.imshow("test", single_module_image_with_pixels)
        cv2.waitKey(0)'''
        #EXECUTING MODULE IMMEDIATELY
        #endregion
        if module_name == 'maze':
            do_maze()
        elif module_name == "sequence":
            do_sequence()
        elif module_name == 'wires':
            do_wires(serial)
        elif module_name == 'whos on first':
            do_first(True)
        elif module_name == 'morse':
            do_morse()
        elif module_name == 'memory':
            do_memory([],1,[])
        elif module_name == 'simon':
            do_simon(serial)
        elif module_name == 'password':
            do_password()
        elif module_name == 'keypads':
            do_keypads()
        elif module_name == 'button':
            do_button(labels,batteries)
        elif module_name == 'complicated':
            do_complicated(serial,batteries,parallel_port)
        time.sleep(0.3)
        print('going back shoundt be zoomed')
        pyautogui.click(button = "right")
        print('doing the 0.5 time sleep')
        time.sleep(1.5) # used to be 0.5

    pyautogui.dragTo(700, None, 0.12, button="right")
    pyautogui.click(button='right')
    time.sleep(0.1)
    pyautogui.click(1200, 1000, button='left')
    is_on_flipped = False
    time.sleep(1)
    #checking modules on other side
    for module in module_array_front:
        # region
        # module is ("name",x,y)
        module_name = ''
        # print(module)
        pyautogui.click(650 + module[1] * 550, 400 + module[2] * 550)
        # image to show what im clicking at more or less
        '''press_position = pyautogui.screenshot(region=(650+module[1]*550, 400+module[2]*550, 50, 50))
        press_position = np.array(press_position)
        press_position = cv2.cvtColor(press_position, cv2.COLOR_BGR2RGB)
        cv2.imshow("test",press_position)
        cv2.waitKey(0)'''
        print('doing the 0.7 time sleep')
        time.sleep(1.5)  # used to be 0.7
        single_module_image = pyautogui.screenshot(region=(800, 240, 1300, 1200))
        single_module_image_np = np.array(single_module_image)
        single_module_image_with_pixels = cv2.cvtColor(single_module_image_np, cv2.COLOR_BGR2RGB)
        single_module_image_with_pixels[pixel_y, pixel_x] = (0, 0, 255)
        single_module_image_with_pixels[pixel_y2, pixel_x2] = (255, 0, 0)

        print(" ", pyautogui.pixel(pixel_x2 + 800, 240 + pixel_y2))  # pixel check position
        first_px = closest_color(pyautogui.pixel(pixel_x2 + 800, 240 + pixel_y2), type_of_module_LUT)
        second_px = closest_color(pyautogui.pixel(pixel_x + 800, 240 + pixel_y), type_of_module_LUT2)
        print(pyautogui.pixel(pixel_x + 800, 240 + pixel_y), ' red')  # red
        print(pyautogui.pixel(pixel_x2 + 800, 240 + pixel_y2), ' blue')  # blue
        if first_px == 'wires' and second_px == 'complicated':
            module_name = 'complicated'
        else:
            if first_px == second_px == 'button':
                module_name = 'button'
            else:
                if first_px != 'button':
                    module_name = first_px
                elif second_px != 'button':
                    module_name = second_px
        print(first_px, second_px, ' first and second px')
        print(module_name)
        '''if pyautogui.pixel(pixel_x2 + 800, 240 + pixel_y2) in type_of_module_LUT:
            module_name = type_of_module_LUT[pyautogui.pixel(pixel_x2 + 800, 240 + pixel_y2)]
            print(module_name, ' module')
        elif pyautogui.pixel(pixel_x + 800, 240 + pixel_y) in type_of_module_LUT2:
            module_name = type_of_module_LUT2[pyautogui.pixel(pixel_x + 800, 240 + pixel_y)]
            print(module_name, ' module')
        else:
            print(pyautogui.pixel(pixel_x + 800, 240 + pixel_y), 'not in lut') # red
            print(pyautogui.pixel(pixel_x2+800,240+pixel_y2), 'not in lut') # blue
            module_name = 'button'
            print("its a button")'''
        # do_button(labels,batteries)
        '''cv2.imshow("test", single_module_image_with_pixels)
        cv2.waitKey(0)'''
        # EXECUTING MODULE IMMEDIATELY
        # endregion
        if module_name == 'maze':
            do_maze()
        elif module_name == "sequence":
            do_sequence()
        elif module_name == 'wires':
            do_wires(serial)
        elif module_name == 'whos on first':
            do_first(True)
        elif module_name == 'morse':
            do_morse()
        elif module_name == 'memory':
            do_memory([], 1, [])
        elif module_name == 'simon':
            do_simon(serial)
        elif module_name == 'password':
            do_password()
        elif module_name == 'keypads':
            do_keypads()
        elif module_name == 'button':
            do_button(labels, batteries)
        elif module_name == 'complicated':
            do_complicated(serial, batteries, parallel_port)
        time.sleep(0.3)
        print('going back shoundt be zoomed')
        pyautogui.click(button="right")
        print('doing the 0.5 time sleep')
        time.sleep(1.5)  # used to be 0.5
    print(f"printing ciapka at {module[1]*550}, {module[2]*550}")


    #single_module_image_with_pixels[yy + y , xx + x ] = (0, 0, 255)
