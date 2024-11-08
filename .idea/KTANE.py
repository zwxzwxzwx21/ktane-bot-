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
    screen = pyautogui.screenshot(region=(1050, 460, 500, 500))
    screen = np.array(screen)
    screen = cv2.cvtColor(screen, cv2.COLOR_BGR2RGB)
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
            screen[135+y*49,118+x*49] = (0,0,255)
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

    screen = pyautogui.screenshot(region=(1050, 460, 500, 500))
    screen = np.array(screen)
    screen = cv2.cvtColor(screen, cv2.COLOR_BGR2RGB)

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
    cv2.imshow('screen', screen)
    cv2.waitKey(0)
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
        screen = pyautogui.screenshot(region=(1050, 460, 500, 500))
        screen = np.array(screen)
        screen = cv2.cvtColor(screen, cv2.COLOR_BGR2RGB)

        for i in range(5):
            #print('NEW LETTER')
            letter_array = [] # new for each letter thats why inside this loop
            pixel_number = 0

            #second check
            print("second check")
            letter_array_2 = []  # new for each letter thats why inside this loop
            pixel_number_2 = 0
            screen[ 218 + 5 * 13][ 77 + i * 79 + 3 * 13] = (255,255,255)
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
                    screen[218 + y * 13][77 + i * 79 + x * 13] = (255, 0, 0)
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
                    screen[226+ y * 13][81+i*79 + x*13 ]=(0,0,255)
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
serial_test = 'zz1ab1'
parallel_test = False
batteries_test = 3
def do_simon(serial):
    green_light_lut = \
        {
            (44, 42, 39) : "gray",
            (1, 170, 35) : "green"
        }
    screen = pyautogui.screenshot(region=(1050, 460, 500, 500))
    screen = np.array(screen)
    screen = cv2.cvtColor(screen, cv2.COLOR_BGR2RGB)
    screen[20,480] = (0,0,255)

    print(pyautogui.pixel(1050+480,480))

    serial_has_vowel = False
    vowels = ['a','e','i','o','u']
    for vowel in vowels:
        if vowel in serial:
            serial_has_vowel = True
            print("vowel in serial")
            break
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
    while True: # change true to check if there is green light
        if closest_color(pyautogui.pixel(1050+480,480),green_light_lut) == "green":
            break
        # slows the check time after it notices a flash

        # this one counts colors to compare like on stage 3 should be 3 colors ofc
        # idea how to approach it
        # at first we are checking every 0.25 seconds for a flash, after that everything becomes normalized
        # since we already know what color to press, do it immediately and after that we wait set aomut of time for color to flash
        # however, first color remains the same, so what we can do is simply check when second color would be flashing
        # and since it would be normalized, we set the timer precisely and ur done with stage 2, other stages can be done in the same way
        # the only thing you need to also do check is light in the corner, can be checked after 3rd round to save time but idk really
        # if its gray, play until win, if its green, yippe you won.
        if is_flashing == False:
            time.sleep(0.25)
            # screen[240,160] = (0,255,255) # red
            # screen[100,250] = (0,255,255) # blue
            # screen[240,380] = (0,255,255) # yellow
            # screen[350,260] = (0,255,255) # green
            # print('red ',pyautogui.pixel(1050+160,460+240))
            # print('blue ',pyautogui.pixel(1050+250,460+100))
            # print('yellow ',pyautogui.pixel(1050+380,460+240))
            # print('green ',pyautogui.pixel(1050+260,460+350))

            if closest_color(pyautogui.pixel(1050+260,460+350),color_lut) == 'green on':
                print("flashing green")
                #flashing_array.append("green")
                if serial_has_vowel:
                    pyautogui.click(1050+380,460+240)
                    press_array.append("yellow")
                else:
                    pyautogui.click(1050+260,460+350)
                    press_array.append("green")
                is_flashing = True
            elif closest_color(pyautogui.pixel(1050+380,460+240),color_lut) == 'yellow on':
                print("flashing yellow")
                if serial_has_vowel:
                    pyautogui.click(1050 + 260, 460 + 350)
                    press_array.append("green")

                else:
                    pyautogui.click(1050 + 160, 460 + 240)
                    press_array.append("red")
                #flashing_array.append("yellow")
                is_flashing = True
            elif closest_color(pyautogui.pixel(1050+250,460+100),color_lut) == 'blue on':
                print("flashing blue")
                if serial_has_vowel:
                    pyautogui.click(1050 + 160, 460 + 240)
                    press_array.append("red")
                else:
                    pyautogui.click(1050 + 380, 460 + 240)
                    press_array.append("yellow")
                #flashing_array.append("blue")
                is_flashing = True
            elif closest_color(pyautogui.pixel(1050+160,460+240),color_lut) == 'red on':
                print("flashing red")
                if serial_has_vowel:
                    pyautogui.click(1050+250,460+100)
                    press_array.append("blue")
                else:
                    pyautogui.click(1050+250,460+100)
                    press_array.append("blue")
                #flashing_array.append("red")
                is_flashing = True
        if is_flashing:

            #wait set amount of time to see exactly second flash
            if stage == 1:
                time.sleep(2.6)
            if stage == 2:
                time.sleep(3.5)
            if stage == 3:
                time.sleep(4.4)
            if stage == 4:
                time.sleep(5.3)
            screen = pyautogui.screenshot(region=(1050, 460, 500, 500))
            screen = np.array(screen)
            screen = cv2.cvtColor(screen, cv2.COLOR_BGR2RGB)
            # if stage == 2:
            #     cv2.imshow('screen', screen)
            #     cv2.waitKey(0)
            if closest_color(pyautogui.pixel(1050 + 260, 460 + 350), color_lut) == 'green on':
                print("flashing green")
                # flashing_array.append("green")
                if serial_has_vowel:
                    #pyautogui.click(1050 + 380, 460 + 240)
                    press_array.append("yellow")
                else:
                    #pyautogui.click(1050 + 260, 460 + 350)
                    press_array.append("green")
                is_flashing = True
            elif closest_color(pyautogui.pixel(1050 + 380, 460 + 240), color_lut) == 'yellow on':
                print("flashing yellow")
                if serial_has_vowel:
                    #pyautogui.click(1050 + 260, 460 + 350)
                    press_array.append("green")

                else:
                    #pyautogui.click(1050 + 160, 460 + 240)
                    press_array.append("red")
                # flashing_array.append("yellow")
                is_flashing = True
            elif closest_color(pyautogui.pixel(1050 + 250, 460 + 100), color_lut) == 'blue on':
                print("flashing blue")
                if serial_has_vowel:
                    #pyautogui.click(1050 + 160, 460 + 240)
                    press_array.append("red")
                else:
                    #pyautogui.click(1050 + 380, 460 + 240)
                    press_array.append("yellow")
                # flashing_array.append("blue")
                is_flashing = True
            elif closest_color(pyautogui.pixel(1050 + 160, 460 + 240), color_lut) == 'red on':
                print("flashing red")
                if serial_has_vowel:
                    #pyautogui.click(1050 + 250, 460 + 100)
                    press_array.append("blue")
                else:
                    #pyautogui.click(1050 + 250, 460 + 100)
                    press_array.append("blue")
                # flashing_array.append("red")
            print(press_array)
            for color in press_array:
                if color == 'green':
                    pyautogui.click(1050 + 260, 460 + 350)
                elif color == "blue":
                    pyautogui.click(1050 + 250, 460 + 100)
                elif color == "red":
                    pyautogui.click(1050 + 160, 460 + 240)
                elif color == "yellow":
                    pyautogui.click(1050 + 380, 460 + 240)

            stage += 1
    cv2.imshow('screen', screen)
    cv2.waitKey(0)
    if serial_has_vowel:
        pass


def do_complicated(serial,batteries,parallel):
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
    screen = pyautogui.screenshot(region=(1050, 460, 500, 500))
    screen = np.array(screen)
    screen = cv2.cvtColor(screen, cv2.COLOR_BGR2RGB)
    cable1 = []
    cable2 = []
    cable3 = []
    cable4 = []
    cable5 = []
    cable6 = []
    # cable format: (led,color_1,color_2,star)
    for led in range(6):
        # pixels that check for leds
        screen[50,65+led*58] = (0,0,255)
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

    screen[93, 65 + 0 * 58] = (0, 255, 0) # cable1 (on blue)
    screen[90, 62 + 1 * 58] = (0, 255, 0) # cable2 (white) (meaning that second color_2  should check for red)
    screen[98, 59 + 2 * 58] = (0, 255, 0) # cable3 (red)
    screen[93, 69 + 3 * 58] = (0, 255, 0) # cable4 (blue)
    screen[90, 67 + 4 * 58] = (0, 255, 0) # cable5 (white)
    screen[95, 64 + 5 * 58] = (0, 255, 0) # cable6 (blue)
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
    screen[93, 59 + 0 * 58] = (0, 0, 0)  # cable1
    screen[95, 67 + 1 * 58] = (0, 0, 0)  # cable2  (meaning that second color_2  should check for red)
    screen[93, 55 + 2 * 58] = (0, 0, 0)  # cable3
    screen[110, 80 + 3 * 58] = (0, 0, 0)  # cable4 ()
    screen[100, 75 + 4 * 58] = (0, 0, 0)  # cable5 ()
    screen[110, 64 + 5 * 58] = (0, 0, 0)  # cable6 ()
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
    screen[450, 70 + 0 * 70] = (255, 255, 0)  # star1
    screen[450, 72 + 1 * 70] = (255, 255, 0)  #   star2
    screen[440, 75 + 2 * 70] = (255, 255, 0)  # star3
    screen[446, 80 + 3 * 70] = (255, 255, 0) #  star4
    screen[435, 85 + 4 * 70] = (255, 255, 0)  # star5
    screen[450, 92 + 5 * 70] = (255, 255, 0)  # star6
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
    cv2.imshow('screen', screen)
    cv2.waitKey(0)

def click_position(index):
    x_coord = 1050 + 75 + index * 85
    y_coord = 460 + 385
    pyautogui.click(x_coord, y_coord)

def do_memory(previous_answers,stage,numbers):
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
    screen = pyautogui.screenshot(region=(1050, 460, 500, 500))
    screen = np.array(screen)
    screen = cv2.cvtColor(screen, cv2.COLOR_BGR2RGB)
    screen[155,200] = (0,0,0)
    screen[155,235] = (0,0,255)
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
        screen[385, 75+i*85] = (0, 0, 0)
        screen[385, 100+i*85] = (0, 0, 255)
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



do_simon(serial_test)
time.sleep(21)
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
        }
    type_of_module_LUT2 = \
    {
        (67, 66, 79) : "sequence",
        (67, 67, 79) : "sequence",
        (87, 91, 102) : "morse",
        (40, 36, 44) : "whos on first",
        (99, 110, 137): "wires",
        (99, 111, 137): "wires",
    }
    # if not in any then its button
    pixel_x,pixel_y=670,560 # those are the values to change for pixels checks, they wont be needed
    pixel_x2,pixel_y2=617,355 # those are the values to change for pixels checks, they wont be needed
    # later so dw changing as much as needed for testing purposes
    for module in module_array_back: # back because we are on the back
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
        time.sleep(0.7)
        '''single_module_image = pyautogui.screenshot(region=(800, 240, 1300, 1200))
        single_module_image_np = np.array(single_module_image)
        single_module_image_with_pixels = cv2.cvtColor(single_module_image_np, cv2.COLOR_BGR2RGB)
        single_module_image_with_pixels[pixel_y,pixel_x] = (0, 0, 255)'''

        print(" " ,pyautogui.pixel(pixel_x2+800,240+pixel_y2)) # pixel check position
        if pyautogui.pixel(pixel_x2 + 800, 240 + pixel_y2) in type_of_module_LUT:
            module_name = type_of_module_LUT[pyautogui.pixel(pixel_x2 + 800, 240 + pixel_y2)]
            print(module_name, ' module')
        elif pyautogui.pixel(pixel_x + 800, 240 + pixel_y) in type_of_module_LUT2:
            module_name = type_of_module_LUT2[pyautogui.pixel(pixel_x + 800, 240 + pixel_y)]
            print(module_name, ' module')
        else:
            module_name = 'button'
            print("its a button")
        #EXECUTING MODULE IMMEDIATELY
        if module_name == 'maze':
            do_maze()
        '''cv2.imshow("test", single_module_image_with_pixels)
        cv2.waitKey(0)'''
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
        module_name = ''
        #print(module)
        pyautogui.click(650 + module[1] * 550, 400 + module[2] * 550)
        time.sleep(0.7)
        #image testing
        '''single_module_image = pyautogui.screenshot(region=(800, 240, 1300, 1200))
        single_module_image_np = np.array(single_module_image)
        single_module_image_with_pixels = cv2.cvtColor(single_module_image_np, cv2.COLOR_BGR2RGB)
        single_module_image_with_pixels[pixel_y, pixel_x] = (0, 0, 255)'''
        print(" ", pyautogui.pixel(pixel_x + 800, 240 + pixel_y)) # pixel check position
        if pyautogui.pixel(pixel_x2+800,240+pixel_y2) in type_of_module_LUT:
            module_name = type_of_module_LUT[pyautogui.pixel(pixel_x2+800,240+pixel_y2)]
            print(module_name, ' module')
        elif pyautogui.pixel(pixel_x+800,240+pixel_y) in type_of_module_LUT2:
            module_name = type_of_module_LUT2[pyautogui.pixel(pixel_x+800,240+pixel_y)]
            print(module_name, ' module')
        else:
            print("its a button");
            module_name = 'button'
        '''
        cv2.imshow("test", single_module_image_with_pixels)
        cv2.waitKey(0)'''


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