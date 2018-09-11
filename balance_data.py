
"""Contains code that takes the dataset and balances it"""

from glob import glob
import numpy as np
import os

if not os.path.exists('balanced_data'):
    os.makedirs('balanced_data')

files = glob('data/*npy')
np.random.shuffle(files)

NEW_FILE_SIZE = 33
assert NEW_FILE_SIZE % 3 == 0


def batch(iterable, n=1):
    # source of function: 
    # https://stackoverflow.com/questions/8290397/how-to-split-an-iterable-in-constant-size-chunks

    a = len(iterable)
    for ndx in range(0, a, n):
        yield iterable[ndx:min(ndx + n, a)]


p = 0

for x in batch(range(0, len(files)), 10):

    forwards_data = []
    rights_data = []
    lefts_data = []

    # Load data into arrays
    for i in x:
        data = np.load(files[i])
        for j in data:
            if np.argmax(j[1]) == 0:
                forwards_data.append(j)
            elif np.argmax(j[1]) == 1:
                rights_data.append(j)
            elif np.argmax(j[1]) == 2:
                lefts_data.append(j)
            else:
                print('None of the above, somehow???')
    
    assert(len(forwards_data) == len(rights_data) == len(lefts_data))

    # Randomise the ordering of the arrays
    np.random.shuffle(forwards_data)
    np.random.shuffle(rights_data)
    np.random.shuffle(lefts_data)

    for k in batch(range(0, len(forwards_data)), int(NEW_FILE_SIZE/3)):

        new_data = []
        # Save data to new arrays
        for l in k:
            new_data.append(forwards_data[l])
            new_data.append(rights_data[l])
            new_data.append(lefts_data[l])

        np.random.shuffle(new_data)
        # print(len(new_data))
        np.save('balanced_data/{}.npy'.format(p), new_data)
        p += 1

    print('Finished {} of {} Files'.format(p, len(files)*3))

print(p)
