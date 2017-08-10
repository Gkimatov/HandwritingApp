"""
Convolutional Neural Net MNIST
ORIG: RUNS 100 SECONDS PER EPOCH
"""
from keras.datasets import mnist
from keras.models import Sequential
from keras.layers import Dense
from keras.layers import Dropout
from keras.layers import Flatten
from keras.layers.convolutional import Conv2D
from keras.layers.convolutional import MaxPooling2D
from keras.utils import np_utils
#from keras import backend as K
#K.set_image_dim_ordering('th')

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import MultiLabelBinarizer
from scipy.misc import imread
import numpy as np
import os
from img_read2 import resize_and_normalize_image

# ~~~~~~~~~~~~~~~~ Fix Random Seed for Reproducibility ~~~~~~~~~~~~~~~~
seed = 7
np.random.seed(seed)

# ~~~~~~~~~~~~~~~~ Process Dataset ~~~~~~~~~~~~~~~~ 
mnist = mnist.load_data()

# nist folder from this script
nist_path = "./NIST/"
NIST = os.listdir(nist_path)

nist_imgs = []
nist_tags = []

# reading through NIST folder: extracting .png images and corresponding hexcode tags
for super_cat in NIST: #caps, digits, small folders
	if (super_cat != '.DS_Store'):
		print super_cat
		new_path = os.path.join(nist_path, super_cat)
		super_cat = os.listdir(new_path)
		
		for cat in super_cat: # A-Z, a-z, 0-9
			if (cat != '.DS_Store'):
				print("---> " + cat)
				new_sub_path = os.path.join(new_path, cat)
				cat = os.listdir(new_sub_path)
				index = 0;
				
				for image in cat:
					if index < 10:
						# getting the first ten images from each category
						read_image = imread(os.path.join(new_sub_path,image))
 						nist_imgs.append(read_image)
 						# getting the hexcode
						hexcode = image.split('_')[1]
						hexcode = hexcode.decode('hex')
						nist_tags.append(hexcode)
						index = index + 1 
						
# resize_and_normalize_image(<list of images>)
# input_dataset will be split into train and validate set and then shuffle it
input_dataset = resize_and_normalize_image(nist_imgs)
#print(nist_tags)

# one hot encoded nist tags
mlb = MultiLabelBinarizer()
mlb_tags = mlb.fit_transform(s.split(', ') for s in nist_tags)
y_train = mlb_tags

"""
# manually split data between train and test
train, test = train_test_split(mnist, train_size = 0.8)

X_train = train[0][0]
y_train = train[0][1]
X_test = test[0][0]
y_test = test[0][1]

print X_train.shape


# reshape to be [samples][pixels][width][height]
X_train = X_train.reshape(X_train.shape[0], 1, 28, 28).astype('float32')
X_test = X_test.reshape(X_test.shape[0], 1, 28, 28).astype('float32')
print X_train.shape


# normalize inputs from 0-255 to 0-1
X_train = X_train / 255
X_test = X_test / 255

# one hot encode outputs
y_train = np_utils.to_categorical(y_train)
y_test = np_utils.to_categorical(y_test)
num_classes = y_test.shape[1]

# ~~~~~~~~~~~~~~~~ Create the Convo Neural Net Model ~~~~~~~~~~~~~~~~ 
def cnn_model():
	# create model
	model = Sequential()
	model.add(Conv2D(30, (5, 5), input_shape=(1, 28, 28), activation='relu'))
	model.add(MaxPooling2D(pool_size=(2, 2)))
	model.add(Conv2D(15, (3, 3), activation='relu'))
	model.add(MaxPooling2D(pool_size=(2, 2)))
	model.add(Dropout(0.2))
	model.add(Flatten())
	model.add(Dense(128, activation='relu'))
	model.add(Dense(50, activation='relu'))
	model.add(Dense(num_classes, activation='softmax'))
	
	# Compile model
	model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])
	return model
	

# build the model
print("Building model...")
model = cnn_model()

# fit the model
print("Fitting model...")
model.fit(X_train, y_train, validation_data=(X_test, y_test), epochs=5, batch_size=200)

# Save model and datasets
model.save('character_recognition_cnn.h5')
print("Model saved in character_recognition_cnn.h5")

np.save('x_train_data.npy', X_train)
print("X_train dataset saved in x_train_data.npy")

np.save('y_train_data.npy', y_train)
print("y_train dataset saved in y_train_data.npy")

np.save('x_test_data.npy', X_test)
print("X_test dataset saved in x_test_data.npy")

np.save('y_test_data.npy', y_test)
print("y_test dataset saved in y_test_data.npy")

# Final evaluation of the model
scores = model.evaluate(X_test, y_test, verbose=0)
print("\n%s: %.2f%%" % (model.metrics_names[1], scores[1]*100))
"""