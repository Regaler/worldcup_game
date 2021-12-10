#-*- coding:utf-8 -*-
"""


Developed by:
    minuk@lunit.io
    rjw0205@lunit.io
"""
import cv2
import numpy as np
import random
import os

WIDTH = 500
HEIGHT = 500


class Game:
    def __init__(self, data_root, num_of_round=6):
        self.data_root = data_root
        self.image_list = self._get_image_list()
        self.survived_data = self.image_list.copy()
        self.num_of_round = num_of_round
        self.survived_this_round = []  # useful cache

    def _get_image_list(self):
        files = os.listdir(self.data_root)
        files = [f"{self.data_root}/{x}" for x in files]
        return files

    def start(self):
        print("Welcome!!!")
        for round in range(self.num_of_round, -1, -1):
            num_of_iter = 2 ** (round - 1)
            if isinstance(num_of_iter, float):
                break
            self.survived_this_round = []
            random.shuffle(self.survived_data)
            for iter in range(num_of_iter):
                left, right = self.fetch_images(round, iter)
                key = self.show_images(left, right, title=f"Round: {round}, {iter}-th iter")
                if key == 'x':
                    self.survived_this_round.append(right)
                elif key == 'z':
                    self.survived_this_round.append(left)
            self.survived_data = self.survived_this_round.copy()
        print("The best data!!")
        print(self.survived_data)
        self.open_image(self.survived_data[0])

    def fetch_images(self, round, iter):
        """
        Fetch two images from the survived data pool
        """
        left = self.survived_data.pop()
        right = self.survived_data.pop()
        return left, right

    def show_images(self, left, right, title):
        """
        Show the screen with left and right images
        """
        img1 = cv2.imread(left)
        img2 = cv2.imread(right)
        img1 = cv2.resize(img1, dsize=(WIDTH, HEIGHT))
        img2 = cv2.resize(img2, dsize=(WIDTH, HEIGHT))
        combined_image = np.concatenate((img1, img2), axis=1)
        cv2.imshow(title, combined_image)
        key = chr(cv2.waitKey(0))
        cv2.destroyAllWindows()
        if key != "z":
            key = "x"
        return key

    def open_image(self, path):
        img = cv2.imread(path)
        cv2.imshow("The best!!", img)
        cv2.waitKey(0)
        cv2.destroyAllWindows()


if __name__ == "__main__":
    game = Game(data_root="", num_of_round=4)
    game.start()