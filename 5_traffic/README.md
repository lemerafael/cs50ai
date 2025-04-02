# Project 5 - Traffic
The program runs with Python minimum version 3.10
Before running the program, install the requirements using the command:
> pip3 install -r requirements.txt

The data set should be downloaded from https://cdn.cs50.net/ai/2023/x/projects/5/gtsrb.zip and extracted inside a directory named gtsrb

To identify which traffic sign appears in a photograph using the Traffic app, run the command:
> python traffic.py <directory with data>

e.g.:
> python traffic.py gtsrb

# Testing Notes

I started the process of making the neural network model by studying the suggested website (official Tensorflow Keras overview - source: https://www.tensorflow.org/guide/keras). I tried to understand the Keras API parameters specifically for generating a model (source: https://keras.io/api/models/model_training_apis/). I also tried studying the lecture source code (source: https://cdn.cs50.net/ai/2020/spring/lectures/5/src5/digits/handwriting.py). Eventually, I ended up using the latter as basis for a successfully running model. This model features a convolutional layer that learns with 32 filters using a 3x3 kernel. There is a max-pooling layer, using 2x2 pool size. The units are flattened. There is a hidden layer with dropout and an output layer with output units for all NUM_CATEGORIES.
By removing the hidden layer with dropout, the output printed on the terminal has a great accuracy, about 0.935. However, this is still worse than the example, so there might be some tweeks needed to achieve better results. I also tried changing the filter quantity and the pool size.