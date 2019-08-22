# Imports
import cv2
import numpy as np
from PreprocessGrid import get_corner_points_of_largest_contour, crop_and_reshape
from PreprocessNumber import PreprocessNumber


def preprocess_sudoku_board(board_img, dimension):
    """Processes an image of a Sudoku board by finding all numbers and extracting them to a new Sudoku board with 81
    squares of equal size.

    Parameters
    ----------
    board_img : numpy array
        An numpy array describing an image of a Sudoku Board.
    dimension : tuple
        A tuple of two integers describing the dimension of each square of the 81 squares in the resulting Sudoku board.

    Returns
    -------
    numpy array
        A numpy array describing the resulting processed Sudoku board.
    """

    # Thicker lines to ease the finding of the largest contour
    processed = __preprocess_image(board_img.copy(), line_thickness=3)
    corners = get_corner_points_of_largest_contour(processed_sudoku_board=processed)

    # Extract the Sudoku board
    cropped_grid = crop_and_reshape(__preprocess_image(board_img.copy(), line_thickness=1), corners)

    # Split the Sudoku board in 81 squares of equal size, then expand each square to minimize the risk that a
    # substantial part of a number is lost between two squares.
    expand_ratio = 1.05
    expanded_images = __get_expanded_images(img=cropped_grid.copy(), expand_ratio=expand_ratio)

    # Find and center numbers and add them to centered_numbers, if no number is found, add a black image.
    centered_numbers = []
    for image in expanded_images:
        process_number = PreprocessNumber(image.copy())
        process_number.crop_feature()
        is_number = process_number.is_number()
        if is_number:
            centered_number = process_number.get_centered_number(dimension)
        else:
            # Create a black image
            centered_number = np.zeros(dimension)
        centered_numbers.append((centered_number, is_number))

    return centered_numbers


def __preprocess_image(img, line_thickness=3):
    """Processes a given image by applying Guassian-blur, using adaptive-threshold, invert the colors and dilate.

    Parameters
    ----------
    img : numpy array
        An image described by an numpy array.
    line_thickness : int
        A number describing line thickness to dilate to.

    Returns
    -------
    numpy array
        A numpy array describing the processed image.
    """

    img = cv2.GaussianBlur(img.copy(), (9, 9), 0)
    thresh_hold = cv2.adaptiveThreshold(img, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 4)

    # Inverts the picture
    inverted = cv2.bitwise_not(thresh_hold, thresh_hold)

    # Adjusting the lines thickness
    kernel = np.ones((line_thickness, line_thickness), np.uint8)
    return cv2.dilate(inverted, kernel)


def __get_expanded_images(img, expand_ratio):
    """Splits the input image into 81 squares (9x9-grid) of equal size. Then expand each square with the expand ratio.

    Parameters
    ----------
    img : numpy array
        An image described by an numpy array
    expand_ratio : float
        A number describing the float number

    Returns
    -------
    list
        A list of 81 numpy arrays describing the expanded images.
    """

    nr_rows = 9
    expanded_images = []
    width = int(np.floor(min(img.shape) / nr_rows))
    height = width
    for row in range(1, 1 + nr_rows):
        for col in range(1, 1 + nr_rows):
            # Only expand in directions where there is something, for example, do not expand upwards if the affected
            # image is already at the first row.
            adj_height_upper = adj_height_lower = adj_width_left = adj_width_right = 0
            if row != 1 and row != 9:
                adj_height_upper = int(height / expand_ratio) - height
            if row != 9:
                adj_height_lower = int(height * expand_ratio) - height
            if col != 1:
                adj_width_left = int(width / expand_ratio) - width
            if col != 9:
                adj_width_right = int(width * expand_ratio) - width
            from_row = (row - 1) * height + adj_height_upper
            to_row = row * height + adj_height_lower

            # Making sure that all rows at the bottom will be included
            if row == 9:
                to_row = img.shape[0]
            expanded_image = np.zeros((int((to_row - from_row)), width + (adj_width_right - adj_width_left)))

            # Expands each image
            for index, k in enumerate(range(from_row, to_row)):
                expanded_image[index] = img[k][(col - 1) * width + adj_width_left:col * width + adj_width_right]
            expanded_images.append(expanded_image)
    return expanded_images
