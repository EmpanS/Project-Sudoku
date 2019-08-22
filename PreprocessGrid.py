import cv2
import numpy as np


def get_corner_points_of_largest_contour(processed_sudoku_board):
    """Finds and returns the corner points of the largest contour in the processed image of a Sudoku board.

    Given a quadrangle in a two-dimensional grid, the four corners of the quadrangle can be expressed as the solution
    of an optimization problem:
    Upper left  corner: the coordinates (x,y) that minimizes x + y
    Lower right corner: the coordinates (x,y) that maximizes x + y
    Upper right corner: the coordinates (x,y) that maximizes x - y
    Upper right corner: the coordinates (x,y) that maximizes y - x

    Parameters
    ----------
    processed_sudoku_board : numpy array
        A processed image of a Sudoku board described by an numpy array.

    Returns
    -------
    list
        a list with four coordinate-points describing the four corners of the largest contour.
    """

    largest_contour = __get_largest_contour(img=processed_sudoku_board)
    quadrangle = largest_contour

    # We will loop through all coordinates and calculate the expressions above and save the result in the variable evals
    evals = np.zeros([3, len(quadrangle)])
    for index, coordinates in enumerate(quadrangle):
        coordinates = coordinates[0]
        # To find upper left, lower right
        evals[0, index] = sum(coordinates)
        # To find upper right
        evals[1, index] = coordinates[0] - coordinates[1]
        # To find lower right
        evals[2, index] = coordinates[1] - coordinates[0]
    upper_left = quadrangle[np.argmin(evals, axis=1)[0]][0]
    lower_right = quadrangle[np.argmax(evals, axis=1)[0]][0]
    upper_right = quadrangle[np.argmax(evals, axis=1)[1]][0]
    lower_left = quadrangle[np.argmax(evals, axis=1)[2]][0]
    return np.array([upper_left, upper_right, lower_right, lower_left])


def crop_and_reshape(original_img, quadrangle):
    """Crops and warps a rectangular section from an image into a square having the same size as the smallest side of
    the rectangular section.

    Parameters
    ----------
    original_img : numpy array
        An image described by an numpy array containing a rectangular section
    quadrangle : numpy array
        A numpy array of coordinates describing the four corner points of the rectangular section that will be cropped
        from the image.

    Returns
    -------
    numpy array
        a numpy array describing the cropped and warped rectangular section
    """

    # Get coordinates of the square in which the rectangular section should be cropped and warped into.
    destination = __get_dst(quadrangle)
    side_length = np.ceil(__get_distance(destination[0], destination[1]))

    # Gets the transformation matrix for skewing the image to fit a square
    source = np.array(quadrangle, dtype='float32')  # Necessary to explicitly specify the data type to avoid error
    transformation_matrix = cv2.getPerspectiveTransform(source, destination)

    # Performs the transformation on the original image
    return cv2.warpPerspective(original_img, transformation_matrix, (int(side_length), int(side_length)))


def __get_distance(p1, p2):
    """Calculate and returns the euclidean distance between to points

    Parameters
    ----------
    p1 : List of two numbers
        The first point described as a coordinate of two numbers
    p2 : List of two numbers
        The second point described as a coordinate of two numbers

    Returns
    -------
    float
        The euclidean distance
    """

    difference = np.array([p2[i] - p1[i] for i in range(len(p1))])
    euclidean_distance = np.sqrt(sum(difference ** 2))
    return euclidean_distance


def __get_dst(quadrangle):
    """Calculates and returns four coordinates describing the perspective to crop and warp to.

    Parameters
    ----------
    quadrangle : list
        A list of coordinates describing the four corner points of a rectangular section

    Returns
    -------
    float
        A list of coordinates in which the rectangular section should be cropped and warped into.
    """

    upper_left, upper_right, lower_right, lower_left = [item for item in quadrangle]
    smallest_side = min([
        __get_distance(upper_left, upper_right),
        __get_distance(upper_right, lower_right),
        __get_distance(lower_right, lower_left),
        __get_distance(lower_left, upper_left)
    ])
    return np.array([[0, 0], [smallest_side, 0], [smallest_side, smallest_side], [0, smallest_side]],
                    dtype='float32')


def __get_largest_contour(img):
    """Finds and returns the largest contour given an image.

    Parameters
    ----------
    img : numpy array
        An image described by an numpy array.

    Returns
    -------
    list
        a list with coordinates describing the largest contour in the image img.
    """

    contours, hierarchy = cv2.findContours(img, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    # Sort the contours by area in the descending order.
    contours = sorted(contours, key=cv2.contourArea, reverse=True)
    return contours[0]
