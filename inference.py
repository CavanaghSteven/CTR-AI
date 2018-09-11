
"""Contains code that uses the model on the running game"""

import time
import cv2

from Game import Game

from keras.models import load_model

WIDTH = 140
HEIGHT = 140

paused = True
# paused = False

game = Game(window_name="ePSXe - Enhanced PSX emulator", width=WIDTH, height=HEIGHT)
nn = load_model('models/weights-adam-binary_crossent-lr-callback-mindelta0.01.hdf5')

print('Starting inference!...')
print('Pausing!')
print('Press \'C\' to pause/unpause')

while True:
    if not paused:

        img = game.get_screen()
        
        cv2.imshow('Screen Capture.png', img)
        
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
        img = img.reshape(1, WIDTH, HEIGHT, 1)
        img = img / 255

        prediction = nn.predict([img])
        Game.send_input(prediction)

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
