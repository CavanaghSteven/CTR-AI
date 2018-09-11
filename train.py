
"""Contains code for the training of the model"""

from nn_model import model_simple
from glob import glob
import keras
from keras.callbacks import ModelCheckpoint
import time
import numpy as np
import os

WIDTH = 140
HEIGHT = 140


if not os.path.exists('models'):
    os.makedirs('models')

if not os.path.exists('log'):
    os.makedirs('log')

files = glob('balanced_data/*npy')
np.random.shuffle(files)

split_ratio = 0.1
train_files = files[:-int(len(files) * split_ratio)]
test_files = files[-int(len(files) * split_ratio):]


# Create generator for training
def generate_data(train_files, dataset_length):
    while True:
        for i in range(dataset_length):
            data = np.load(train_files[i])

            X = np.array([i[0] for i in data]).reshape(-1, WIDTH, HEIGHT, 1)
            X = X / 255
            y = np.array([i[1] for i in data])
            yield X, y


nn = model_simple(WIDTH, WIDTH, 0.01, 3)

train_gen = generate_data(train_files, len(train_files))
test_gen = generate_data(test_files, len(test_files))

model_name = 'adam-{}.model'.format(int(time.time()))
# model_name = 'adam-{}'.format('binary_crossent')

reducelrcallback = keras.callbacks.ReduceLROnPlateau(
    monitor='val_acc',
    verbose=1,
    factor=0.1,
    patience=5,
    min_delta=0.001,
    min_lr=0)

tensorboard = keras.callbacks.TensorBoard(
    log_dir='log/{}'.format(model_name),
    histogram_freq=0,
    write_graph=True,
    write_images=True)

filepath = 'weights-{}.hdf5'.format(model_name)
checkpoint = ModelCheckpoint(
    'models/{}'.format(filepath),
    monitor='val_acc',
    verbose=1,
    save_best_only=True,
    mode='max')

nn.fit_generator(
    generator=train_gen,
    validation_data=test_gen,
    steps_per_epoch=len(train_files),
    validation_steps=len(test_files),
    epochs=10,
    callbacks=[tensorboard, checkpoint, reducelrcallback])
