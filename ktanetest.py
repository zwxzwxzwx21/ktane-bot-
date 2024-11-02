import os
import cv2
import numpy as np
import pyautogui
import time
def distance_to_colors(pixel):
    white = np.array([255, 255,255])
    black = np.array([0, 0, 0])
    distance_to_white = np.linalg.norm(pixel - white)
    distance_to_black = np.linalg.norm(pixel - black)
    return distance_to_white, distance_to_black

def take_and_display_screenshot(x,y,width,height):
    screenshot = pyautogui.screenshot(region=(x,y,width,height))

    screenshot_np = np.array(screenshot)
    my_image = cv2.cvtColor(screenshot_np,cv2.COLOR_RGB2BGR)
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
            (78, 82, 81): "port plate", # works on every position
            (78, 81, 81) : "port plate",

        }
    # this one checks for batteries, battery

    # this one checks for labels and port plates

    numb_of_batteries = 0
    labels = []
    for i in range(5):
        dot_x, dot_y = 168 + i * 230, 79
        my_image[dot_y, dot_x] = (255, 100, 0)

        # Zczytaj piksel z ekranu w odpowiedniej pozycji
        screen_pixel_rgb = pyautogui.pixel(x + dot_x, y + dot_y)
        print(f'Loop {i} | Pixel at ({dot_x}, {dot_y}):', screen_pixel_rgb)
        label_LUT = \
             {
                 "0110101011001110101101101" : "FRK",
                 "0001101101000010110101101": 'A',
                 "0000101100000010110101101": 'A',
             }
        try:
            # Sprawdź wartość w `labels_LUT`
            labels_value = widgets_LUT[screen_pixel_rgb]

            # Zwiększ licznik baterii, jeśli etykieta to liczba
            if isinstance(labels_value, int):
                numb_of_batteries += labels_value

            # Warunek, jeśli etykieta to "label"
            if labels_value == "label":
                print("label")

                # Sprawdzenie pikseli w odpowiedniej pozycji
                screen = pyautogui.screenshot(region=(645 + i * 230, 34, 30, 45))
                screen_np = np.array(screen)

                # Przeskalowanie obrazu
                scale_percent = 500
                width = int(screen_np.shape[1] * scale_percent / 100)
                height = int(screen_np.shape[0] * scale_percent / 100)
                dim = (width, height)

                resized_image = cv2.resize(screen_np, dim, interpolation=cv2.INTER_LINEAR)

                xx, yy = 2, 25
                my_image2 = cv2.cvtColor(screen_np, cv2.COLOR_RGB2BGR)
                my_image2[yy, xx] = (2, 2, 2)
                print(pyautogui.pixel(645 + i * 230 + xx, 34 + yy))

                # Jeśli piksel jest biały
                if pyautogui.pixel(645 + i * 230 + xx, 34 + yy) == (255, 255, 255):
                    # Kontynuacja rozpoznawania obrazu
                    screen = pyautogui.screenshot(region=(745 + i * 230, 34, 40, 45))
                    screen_np = np.array(screen)

                    check_array = ''
                    for j in range(5):
                        for k in range(5):
                            dot_x, dot_y = 3 + k * 4, 6 + j * 8
                            screen_np[dot_y, dot_x] = (0, 0, 255)
                            screen_pixel_rgb = pyautogui.pixel(745 + i * 230 + dot_x, 34 + dot_y)
                            print(dot_x, dot_y, screen_pixel_rgb)

                            # Oblicz odległości od kolorów
                            distance_to_white, distance_to_black = distance_to_colors(np.array(screen_pixel_rgb))
                            closer_color = "white" if distance_to_white < distance_to_black else "black"

                            check_array += '0' if closer_color == "white" else '1'

                    print(check_array)
                    if check_array in label_LUT:
                        if label_LUT[check_array] == "FRK":
                            labels.append("FRK")
                            print("LIT FRK")
                        if label_LUT[check_array] == "A":
                            screen_car_check = pyautogui.screenshot(region=(725 + i * 230, 34, 40, 45))
                            screen_np_car = np.array(screen_car_check)

                            screen_np_car[6, 1] = (255, 0, 255)
                            print('pixel',pyautogui.pixel(725 + i * 230 + 1, 34 + 6))
                            if pyautogui.pixel(725 + i * 230 + 1, 34 + 6) == (210, 206, 191):
                                print("clr")
                            else:
                                labels.append("CAR")
                                print("car label")
                            cv2.imshow('Modified Screenshot', screen_np_car)
                            cv2.waitKey(0)
                    resized_image = cv2.resize(screen_np, dim, interpolation=cv2.INTER_LINEAR)
                    cv2.imshow('Modified Screenshot', resized_image)
                    print(f'Picture {i}')
                    cv2.waitKey(0)

            elif labels_value == "port plate":
                print("port plate")

        except KeyError:
            print(f"{check_array} not in LUT")

    print(f'Number of batteries: {numb_of_batteries}')
    cv2.destroyAllWindows()


take_and_display_screenshot(600,0,1200,100)


