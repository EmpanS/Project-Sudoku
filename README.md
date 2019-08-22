# Project-Sudoku
A couple of python-scripts were made, resulting in a program that takes an image of an unfinished Sudoku board as input and returns the solution in a numpy array.

Using prebuilt functions from OpenCV (Open Computer Vision Library) and CNNs in the Keras API together with my own algorithms, an image of a Sudoku board transforms from just pixel values to a numpy array with integers, which then enables a solution to be found using a Brute Force-algorithm.

In this project I got to practice many aspects of machine learning. I got to gather my own data, label it and build a data pipeline to automatically transform the data. I got to build a CNN and train it on the MNIST dataset and then use transfer learning to make it fit my own data. Finally, I also got to come up with my own algorithms, for example an algorithm used to identify if a gray-scale image contains a number.
