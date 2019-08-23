import numpy as np
from skimage.transform import resize


class PreprocessNumber:
    """
        A class used to process images from a Sudoku board.

        The each box in the Sudoku board should be given an instance of this class. The class contains methods to
        determine if one box contains a number or not. If the box contains a number this class provices methods to
        extract and center the number in a new image with the dimension specified by the user.

        Attributes
        ----------
        NOT_BLACK_THRESHOLD : int (20)
            a threshold used to classify if a pixel is considered non-black.
        image : numpy array
            the input image represented by a numpy array
        extracted_feature : numpy array
            a numpy array representing the extracted feature from the image
        dimension : tuple
            a tuple describing the dimension input image
        __dct_groups : dictionary
            a dictionary used to keep track of all groups of feature in the image as well as the group that each pixel
            contains to.

        Methods
        -------
        def crop_feature(self):
            Crops the most centered feature in the image.

        def is_number(self):
            Validates if the instance of this class contains a number by using two conditions.

        def get_centered_number(self, dimension):
            Returns centered number.

        def __create_groups_of_features(self):
            Creates groups of features.

        def __check_left_and_above_pixel_for_group(self, pixel_coord):
            Returns the group value of adjacent pixels.

        def __get_group_number_of_centered_feature(self):
            Finds and returns the group number of the most centered feature.

        def __extract_feature(self, feature_group_number):
            Extracts all pixels corresponding to the given group number to self.extracted_feature.

        def __validate_first_condition(self, temp=0):
            Validates the first condition to determine if the instance of this class contains a number.

        def __validate_second_condition(self):
            Validates the second condition to determine if the instance of this class contains a number.
        """

    def __init__(self, image):
        """
        Parameters
        ----------
        image : numpy array
            the input image represented by a numpy array
        """
        self.NOT_BLACK_THRESHOLD = 20
        self.image = image
        self.extracted_feature = np.zeros_like(self.image)
        self.dimension = self.image.shape
        self.__dct_groups = {}

    def crop_feature(self):
        """Crops the most centered feature in the image.

        This method takes the most centered cohesive group of non-black pixels and crop them to self.extracted_feature.
        """

        self.__create_groups_of_features()
        self.__extract_feature(self.__get_group_number_of_centered_feature())

    def is_number(self):
        """Validates if the instance of this class contains a number by using two conditions.

        Returns
        -------
        boolean
            a boolean representing if self.extracted_feature contains a number or not. True if a number is present,
            False otherwise.
        """
        return self.__validate_first_condition() and self.__validate_second_condition()

    def get_centered_number(self, dimension):
        """Returns centered number.

        This method centers the number currently located in self.extracted_feature and then returns the centered number.

        Parameters
        ----------
        dimension : tuple
            A tuple describing the dimension of the centered number to return

        Returns
        -------
        numpy array
            a numpy array representing the centered number having the dimension as specified by the parameter.
        """

        # Initialize variables to find boundaries
        left_bound = self.extracted_feature.shape[0]
        right_bound = 0
        upper_bound = self.extracted_feature.shape[1]
        lower_bound = 0
        # Find top left and bottom right corners of the number
        for row in range(self.extracted_feature.shape[0]):
            for col in range(self.extracted_feature.shape[1]):
                if self.extracted_feature[row][col] > self.NOT_BLACK_THRESHOLD:
                    if row < upper_bound:
                        upper_bound = row
                    elif row > lower_bound:
                        lower_bound = row
                    if col < left_bound:
                        left_bound = col
                    elif col > right_bound:
                        right_bound = col
        width = right_bound - left_bound + 1
        height = lower_bound - upper_bound + 1

        extracted_number = np.zeros((height, width))

        # Extract the number
        for row in range(height):
            for col in range(width):
                extracted_number[row][col] = self.extracted_feature[upper_bound + row][left_bound + col]

        # Place the extracted number in a square
        if height != width:
            square_number = np.zeros((max((height, width)), max(height, width)))
            if height > width:
                # Add black columns to the left and right
                diff = int((height-width)/2)
                square_number[:, diff:diff + width] = extracted_number
            else:
                # Add black rows above and under
                diff = int((width-height)/2)
                square_number[diff:diff + height, :] = square_number
        else:
            square_number = extracted_number
        centered_number = np.zeros(dimension)

        # Assert that there is at least four black pixels closest to all edges.
        if np.any(np.array(square_number.shape) > 20):
            centered_number[4:24, 4:24] = resize(square_number, (20, 20), anti_aliasing=True)
        else:
            size = square_number.shape
            diff_height = int((dimension[0] - size[0])/2)
            diff_width = int((dimension[0] - size[1])/2)
            centered_number[diff_height:size[0] + diff_height, diff_width:size[1] + diff_width] = square_number
        return centered_number

    def __create_groups_of_features(self):
        """Creates groups of features.

        All different cohesive groups of non-black pixels will be treated as one feature. This method goes through all
        pixels and labels all cohesive groups of non-black pixels. Each pixel will be a key corresponding to its group
        in a dictionary. Black pixels will have its group number set to -1, indicating not a feature.
        """

        new_group = 0
        for row in range(self.dimension[0]):
            for col in range(self.dimension[1]):
                if self.image[row][col] > self.NOT_BLACK_THRESHOLD:
                    # Checks if the current pixel at (row, col) is adjacent to already assigned non-black pixels.
                    surrounding_group = self.__check_left_and_above_pixel_for_group(pixel_coord=[row, col])
                    if surrounding_group != -1:
                        self.__dct_groups[str(row) + ":" + str(col)] = surrounding_group
                    else:
                        self.__dct_groups[str(row) + ":" + str(col)] = new_group
                        new_group += 1
                else:
                    self.__dct_groups[str(row) + ":" + str(col)] = -1

    def __check_left_and_above_pixel_for_group(self, pixel_coord):
        """Returns the group value of adjacent pixels.

        Given a coordinate of a pixel, this method checks if the adjacent pixels to the left and above have already
        been assigned a group. If they have, this method returns the group number. If the pixel to the left and above
        have been assigned different groups, all pixels associated with the group of the pixel above will be assigned
        the group of the pixel to the left.
        """

        group_pixel_left = -1
        if pixel_coord[1] > 0:
            # If there is an adjacent pixel to the left
            group_pixel_left = self.__dct_groups[str(pixel_coord[0]) + ":" + str(pixel_coord[1]-1)]
        if pixel_coord[0] > 0:
            # If there is an adjacent pixel above
            group_pixel_above = self.__dct_groups[str(pixel_coord[0] - 1) + ":" + str(pixel_coord[1])]
            if group_pixel_left == -1:
                return group_pixel_above
            elif group_pixel_above == -1:
                return group_pixel_left
        else:
            # No adjacent pixel above, return the group of the pixel to the left
            return group_pixel_left

        if group_pixel_left != group_pixel_above:
            # Replacing pixels belonging to the group of the pixel above to the group of the pixel to the left
            for item in self.__dct_groups:
                if self.__dct_groups[item] == group_pixel_above:
                    self.__dct_groups[item] = group_pixel_left
        return group_pixel_left

    def __get_group_number_of_centered_feature(self):
        """Finds and returns the group number of the most centered feature.

        This method uses an algorithm that starts to search from the middle and then expands its search in all
        directions. When a non-black pixel is found, the corresponding group is returned.
        """

        center_row = int(self.dimension[0] / 2)
        center_col = int(self.dimension[1] / 2)
        nr_search_loops = min(self.dimension[0] - center_row, self.dimension[1] - center_row) - 1
        loop_directions = [[0, 1], [1, 0], [0, -1], [-1, 0]]

        # Starts looking at the centered pixel
        if self.image[center_row][center_col] > self.NOT_BLACK_THRESHOLD:
            return self.__dct_groups[str(center_row) + ":" + str(center_col)]
        else:
            for loop_nr in range(1, nr_search_loops):
                center_row -= 1
                center_col -= 1
                search_coord = [center_row, center_col]
                for direction in loop_directions:
                    vertical = direction[0]
                    horizontal = direction[1]
                    for i in range(loop_nr * 2):
                        if self.image[search_coord[0]][search_coord[1]] > self.NOT_BLACK_THRESHOLD:
                            return self.__dct_groups[str(search_coord[0]) + ":" + str(search_coord[1])]
                        search_coord[0] += 1 * vertical
                        search_coord[1] += 1 * horizontal
        # If no group was found, all pixels are black.
        return -1

    def __extract_feature(self, feature_group_number):
        """Extracts all pixels corresponding to the given group number to self.extracted_feature.

        Parameters
        ----------
        feature_group_number : int
            An integer representing the group number of the feature to extract.
        """

        for row in range(self.dimension[0]):
            for col in range(self.dimension[1]):
                if self.__dct_groups[str(row) + ":" + str(col)] == feature_group_number:
                    self.extracted_feature[row][col] = self.image[row][col]

    def __validate_first_condition(self):
        """Validates the first condition to determine if the instance of this class contains a number.

        Assume the image of the potential number is split into a 3x3-grid with 9 squares of equal size. The first
        condition is that the middle square should contain at least five non-black pixels.

        Returns
        -------
        boolean
            a boolean representing if self.extracted_feature contains a number or not. True if a number is present,
            False otherwise.
        """

        non_black_dot_counter = 0
        # x_box and y_box represents the coordinates of the upper left corner of the middle square
        x_box = int(self.extracted_feature.shape[0] / 9) * 3
        y_box = int(self.extracted_feature.shape[1] / 9) * 3
        for row in range(x_box, x_box + int(self.extracted_feature.shape[0] / 9)*3):
            for col in range(y_box, y_box + int(self.extracted_feature.shape[1] / 9) * 3):
                if self.extracted_feature[row][col] > self.NOT_BLACK_THRESHOLD:
                    non_black_dot_counter += 1
                    if non_black_dot_counter >= 5:
                        return True
        return False

    def __validate_second_condition(self):
        """Validates the second condition to determine if the instance of this class contains a number.

        The second condition is simply that the extracted feature should have at least 25 non-black pixels to be able
        to be classified as a number.

        Returns
        -------
        boolean
            a boolean representing if self.extracted_feature contains a number or not. True if a number is present,
            False otherwise.
        """

        counter = 0
        for row in self.extracted_feature:
            for pixel in row:
                if pixel > self.NOT_BLACK_THRESHOLD:
                    counter += 1
                    if counter >= 25:
                        return True
        return False
