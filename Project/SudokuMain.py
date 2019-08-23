# Importing useful libraries
import sys
import os
from keras.models import load_model
from SudokuSolver import SudokuSolver
from Preprocess import *
import tensorflow as tf
import matplotlib.pyplot as plt
tf.logging.set_verbosity(tf.logging.ERROR)
MNIST_DIMENSION = (28, 28)


def main():
    """Sudoku solver
    This script allows the user to solve a Sudoku board by specifying the image-path as an argument (with quotation
    marks), the image needs to contain a Sudoku board. This script works best on image taken on real paper where the
    Sudoku board takes up almost the whole picture.

    This script requires that the following dependencies to be within the Python
    environment you are running this script in:
    - keras
    - tensorflow
    - numpy
    - matplotlib
    - scikit-image

    This script can also be run in an IDE, but then the user has to manipulate and manually set the image path.
    """

    image_path = str(sys.argv[1])
    input_sudoku_img = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
    plt.imshow(input_sudoku_img, cmap='gray')
    plt.show()
    resized_sudoku_img = cv2.resize(input_sudoku_img, (1200, 900), interpolation=cv2.INTER_AREA)
    processed_sudoku_img = preprocess_sudoku_board(resized_sudoku_img.copy(), MNIST_DIMENSION)
    sudoku_board = np.zeros((9, 9), dtype=np.int8)

    # Import final model
    model = load_model(os.path.dirname(os.path.realpath(__file__)) + "\Final_model")

    for index, square in enumerate(processed_sudoku_img):
        if square[1]:
            # Normalize number
            number = square[0] / 255
            number = np.reshape(number, newshape=(1, 28, 28, 1))
            prediction = model.predict(number)[0]
            sudoku_board[int(index / 9)][index % 9] = int(np.argmax(prediction)) + 1
        else:
            sudoku_board[int(index / 9)][index % 9] = -1

    print("Interpreted the Sudoku to be:")
    sudoku_solver = SudokuSolver()
    sudoku_solver.print_board(sudoku_board)

    if not sudoku_solver.is_valid_board(sudoku_board):
        print("Sorry, no solution was found. Take a new picture and try again.")
        quit()

    solved_sudoku = np.array(sudoku_solver.solve(sudoku_board)[0])
    sudoku_solver.print_board(solved_sudoku)

if __name__ == "__main__":
    main()
