
"""Contains code for the creation of data"""

import time
import numpy as np
import os
import cv2

from Game import forwards_output, left_output, right_output
from Game import Game

IMG_PER_FILE = 99
CLASSES_PER_FILE = 33
assert IMG_PER_FILE % CLASSES_PER_FILE == 0

i = 500

WIDTH = 140
HEIGHT = 140
# WIDTH = 800
# HEIGHT = 600

if not os.path.exists('data'):
    os.makedirs('data')

while True:
    filename = 'data/{}.npy'.format(i)

    if os.path.isfile(filename):
        i += 1
    else:
        print('starting at', i)
        break

print('Starting collection of data!...')
print('Pausing!')
print('Press \'C\' to pause/unpause')
paused = True
# paused = False
game = Game(window_name="ePSXe - Enhanced PSX emulator", width=WIDTH, height=HEIGHT)

forwards_data = []
left_data = []
right_data = []

while True:
    if not paused:
        
        time.sleep(0.2)

        img = game.get_screen()

        cv2.imshow('Screen Capture.png', img)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

        keys = game.key_check()
        output = Game.get_output(keys)

        # Add image to appropriate array
        if output == forwards_output:
            forwards_data.append([img, output])
            # print('Forwards')
        elif output == right_output:
            right_data.append([img, output])
            # print('Right')
        elif output == left_output:
            left_data.append([img, output])
            # print('Left')
        else:
            pass

        len_forwards = len(forwards_data)
        len_right = len(right_data)
        len_left = len(left_data)

        # If the limit per file is reached
        if len_forwards + len_right + len_left == IMG_PER_FILE:

            if len_forwards > CLASSES_PER_FILE:
                np.random.shuffle(forwards_data)
                forwards_data = forwards_data[:CLASSES_PER_FILE]
                continue

            if len_right > CLASSES_PER_FILE:
                np.random.shuffle(right_data)
                right_data = right_data[:CLASSES_PER_FILE]
                continue

            if len_left > CLASSES_PER_FILE:
                np.random.shuffle(left_data)
                left_data = left_data[:CLASSES_PER_FILE]
                continue

            print('Starting to save data', i)
            # All arrays are of equal size, now save!
            data = np.concatenate([forwards_data, right_data, left_data])
            np.random.shuffle(data)
            print('length forwards {}, length rights {}, length lefts {}'.format(len(forwards_data), len(right_data),
                                                                                 len(left_data)))
            print('length of data saved', len(data))

            filename = 'data/{}.npy'.format(i)
            np.save(filename, data)
            i += 1
            print('\t\tSaved File', i)

            # Empty the data arrays
            forwards_data = []
            right_data = []
            left_data = []

    keys = game.key_check()
    if 'C' in keys:
        if paused:
            paused = False
            print('Unpaused!')
            time.sleep(1)
        else:
            print('Pausing!')
            paused = True
            time.sleep(1)

cv2.destroyAllWindows()
