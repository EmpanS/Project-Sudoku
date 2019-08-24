# Project-Sudoku

### Using computer vision to solve Sudoku puzzles automatically

![readme](https://user-images.githubusercontent.com/38049633/63642689-5fd18600-c6c3-11e9-864c-c5125c7048ca.png)

This was a hobby project where I built a python-program that takes an image of an unfinished Sudoku board as input and returns the solution in a numpy array.

Using prebuilt functions from OpenCV (Open Computer Vision Library) and Convolutional Neural Networks (CNNs) in the Keras API together with my own algorithms, an image of a Sudoku board transforms from just pixel values to a numpy array with integers, which then enables a solution to be found using a Brute Force-algorithm.

## How to run the program
There are two ways to run the program, first you have to download the project. Then, you can:
1. Solve your own Sudoku by taking an image of the Sudoku board, save it on your computer. Then, run the SudokuMain.py from the command prompt and specify the image path as an argument.
2. Solve one of the sample boards found in \Project, by running SudokuMain.py without specifying an image path.

## Examples
The folder \Example contains three jupyter notebooks. Two of them, shows how I trained two CNNs using the Keras API. The third one, called Complete Example.ipyn, contains an example on how to use the program without using the SudokuMain.py. The folder also contains some images used in the examples.

The folder \docs contains further examples with the purpose of explaining concepts, rather than explaining code. It contains a pdf visualizing how the data pipeline manipulates input images. There is also a jupyter notebook that visualizes how some algorithms (that I came up with) work. Do not put any effort in trying to understand the code in the notebook, but rather look at the source code where the algorithm is implemented together with the animation plots in the notebook. 

## Further improvements
These are my ideas for further improvements and possible extensions:
- Error handling, there is currently no error handling in the project.
- A better way to visualize the result, perhaps visualizing the solution onto the input image.
- Implement the program in an android app using Tensorflow Lite

## Lessons learned
In this project I got to practice many aspects of machine learning. I got to gather my own data, label it and build a data pipeline to automatically transform the data. I got to build a CNN and train it on the MNIST dataset and then use transfer learning to make it fit my own data. Even though transfer learning might not be the best strategy to this problem, I chose this strategy to understand how it works. Further, I also used the inbuilt functionality earlystopper (in Keras) to mitigate overfitting. Finally, I got to come up with my own algorithms, for example an algorithm used to identify if a gray-scale image contains a number and an algorithm to extract a number from an image.

I trained the final model on images of Sudokus printed on paper and when I tried the program on 10 different Sudokus (all on paper), it could solve everyone of them as long as I held the camera straight above the Sudoku when taking the pictures. I was amazed when the program solved a Sudoku, where the image was taken on my computer screen.

Any comments, suggestions or feedback is heavily appreciated. Thanks and happy Sudoking!

Emil Sandström
